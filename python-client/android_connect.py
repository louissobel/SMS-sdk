import sys
import socket
import re
import threading
import asyncore
import asynchat
import StringIO

import logger
from SMS import SMS

class AndroidSMS(threading.Thread):
    
    DEVICE = 'android connector'
    
    HOST = 'localhost'
    
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.receive_callback = None
        
        #lets try to connect
        android_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        android_socket.connect((self.HOST,port))
        
        logger.log(self, "connected to android device on port %d" % port)
        self.source = None
        self.sink = 'android device'
        
        self.out_ = android_socket.makefile(mode = 'w')
        self.in_ = android_socket.makefile()
        self.socket_ = android_socket       
    
    def send(self, sms):
        logger.log_send(self, sms)
        
        self.out_.write(str(sms))
        self.out_.flush()        
        
    def receive(self, function, source=None):
        self.receive_callback = function
        self.source = source
        return self
    
    def run(self):
        if self.receive_callback is None:
            # then im not part of an upstream pipeline
            return
            
        #ok! so I listen for a message
        text_parser = TextParser(self.in_)
        
        while True:
            
            try:
                sms = text_parser.one()
            except RuntimeError as e:
                logger.log_error(self, e.message)
                return
                
            
            if sms is None:
                break
            
            logger.log_receive(self, sms)
            self.receive_callback(sms)
            
            
class TextParser:
    
    headerParser = re.compile(r"(TO|FROM|LENGTH):(.*)")
    
    def __init__(self, file_):
        
        self.file_ = file_
    

    def one(self):
        """
        copied from java :/
        """
        state = "waiting"

        length = 0;

        bodyLinesRemaining = 0;

        to_ = ""
        from_ = ""
        body = ""

        while True: 
                
            try:
                line = self.file_.readline()
            except IOError as e:
                # in socket closed, so return null
                return None

            if line == "": #EOF
                return None
                        
            # ok we did our end of file check, so
            # lets strip off the new line
            line = line.strip()

            # waiting mode
            if state == "waiting":
                
                if line == "TEXT":
                    state = "headers"
                else:
                    # then this was an invalid input for waiting mode!
                    raise RuntimeError("Invalid line while waiting for text: %s" % line);
                
            # HEADER MODE
            elif state == "headers":

                headerMatch = self.headerParser.match(line)

                if headerMatch:
                    key = headerMatch.group(1)
                    value = headerMatch.group(2)

                    if key == "LENGTH":
                        length = int(value)
                    elif key == "TO":
                        to_ = value
                    else:
                        from_ = value
                    
                elif line == "":
                    # then we are done with headers!
                    if length == 0:
                        return SMS(to_, from_, body)
                    else:
                        state = "body";
                        bodyLinesRemaining = length
                
                else:
                    # then this was in invalid line for header mode
                    raise RuntimeError("Invalid line while parsing headers: %s" % line)
                
            elif state == "body":
                body += line + "\n"
                bodyLinesRemaining -= 1

                if bodyLinesRemaining == 0:
                    # then we have slurped up all the body that we need to
                    return SMS(to_, from_, body);
            

            else:
                raise RuntimeError("Invalid state in message parser: %s" % state)
    