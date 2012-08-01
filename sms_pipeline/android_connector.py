import sys
import socket
import re
import threading
import StringIO

import logger
from SMS import SMS, SMSPipelineElement

class AndroidConnector(SMSPipelineElement):
    """
    A pipeline element that communicates with an Android device
    (Probably running the SMSToolkit application) using a socket
    and a serialization of a text message.
    
    In initialzation, this element opens the socket, and creates
    a TextParser instance, a state machine responsible for parsing
    text messages from the socket.
    
    To send an SMS upstream, this element writes the SMS to the socket.
    
    To listen on its downstream element, this element reads from the socket,
    using the TextParser to obtain an SMS
    
    To cleanup, this element shuts its socket and associated files
    """
        
    
    def __init__(self, host, port):
        """
        Initializes the element by opening a socket to the android SMSServer
        Does not do any exception handling.
        
        host is the host on which the android SMS server is listening
        port is the port on which the android SMS server is listening
        """
        SMSPipelineElement.__init__(self, 'android connector', 'android device')
        
        self.port = port
        self.host  = host
        
        # Making the connection
        # We don't catch the error here, we
        # leave that as an exercise to the caller
        android_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        android_socket.connect((self.host, self.port))      
        logger.log(self, "connected to android device on on host %s port %d" % (host, port))
        
        # Obtain mock file objects for the socket
        # And the TextParser to parse the text message
        self.out_ = android_socket.makefile(mode = 'w')
        self.in_ = android_socket.makefile()
        self.socket_ = android_socket
        self.text_parser = TextParser(self.in_)
        
        # Used to avoid double closing
        self.closed = False       
    
    def send(self, sms):
        """
        Writes the given SMS
        to the socket out. Serialization
        is handled by the __str__ method
        of the SMS object
        """      
        try:
            self.out_.write(str(sms))
            self.out_.flush()
        except socket.error as e:
            logger.log_error(self, "Error writing to android socket")
        else:
            logger.log_send(self, sms)
    
    def listen(self):
        """
        Obtains one SMS from the TextParser.
        It handles parse errors (RuntimeError), but does
        handle socket errors that may appear.
        
        If the sms received from the parser is None, it will
        assume a broken connection, and, making no value judgements about it,
        quit, calling cleanup() in the process.
        """ 
        try:
            sms = self.text_parser.one()
        except RuntimeError as e:
            logger.log_error(self, e.message)
            return False
                    
        if sms is None:
            logger.log_error(self, "Connection to android device is broken")
            logger.log_error(self, "Exiting read loop, closing socket")
            self.cleanup()
            return False
        
        logger.log_receive(self, sms)
        self.receive_callback(sms)
        
    def cleanup(self):
        """
        If the socket has not already been closed, shuts it.
        
        Vulnerable to a tiny race condition.
        """
        if not self.closed:
            # Race!
            self.closed = True
            self.socket_.shutdown(socket.SHUT_RDWR)
            self.socket_.close()
            
            
class TextParser:
    """
    A class that wraps a file like object in order to read SMSs from it.
    It uses a state machine to parses SMSs according to the spec described
    in the documentation, throwing a RuntimeError if the parse is not correct
    """
    
    # The RE for the parser
    # Compile it here so we don't have to later
    HEADER_RE = re.compile(r"(TO|FROM|LENGTH):(.*)")
    
    def __init__(self, file_):
        """
        Creates the TextParser using the file-like object file_ as input
        """
        self.file_ = file_
    

    def one(self):
        """
        Called to read an SMS from file_
        
        Three states:
            - waiting
            - headers
            - body        
        """
                

        
        # Will be the values for the SMS
        to_ = ""
        from_ = ""
        body = ""
        
        # extra for the body line counting
        length = 0;
        bodyLinesRemaining = 0;
        
        # initial state
        state = "waiting"
        
        while True:           
            # get one line from file_
            try:
                line = self.file_.readline()
            except IOError as e: # in socket closed
                return None

            if line == "": # EOF
                return None
                        
            # Now we strip the newline, because if we had
            # done it before the EOF check, there would
            # have been false EOFs
            line = line.strip()

            # waiting state
            if state == "waiting":
                if line == "TEXT":
                    state = "headers"
                else:
                    raise RuntimeError("Invalid line while waiting for text: %s" % line);
                
            # header state
            elif state == "headers":
                headerMatch = self.HEADER_RE.match(line)
                if headerMatch:
                    key = headerMatch.group(1)
                    value = headerMatch.group(2)

                    if key == "LENGTH":
                        try:
                            length = int(value)
                        except ValueError:
                            raise RuntimeError("LENGTH value must be integer")
                    elif key == "TO":
                        to_ = value
                    else:
                        from_ = value
                    
                elif line == "":
                    # Headers are finished
                    state = "body"
                    bodyLinesRemaining = length        
                else:
                    raise RuntimeError("Invalid line while parsing headers: %s" % line)
            
            # body state    
            elif state == "body":
                body += line + "\n" # undo the line.strip()
                bodyLinesRemaining -= 1

                if bodyLinesRemaining == 0:
                    # We have slurped up all the body that we need to
                    out = SMS(to_, from_, body)
                    out.trim() # remove the last \n as described by the spec
                    return out
            
            # unknown state?
            else:
                raise RuntimeError("Invalid state in message parser: %s" % state)
    