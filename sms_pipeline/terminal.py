"""
SMS sender emulator from terminal
"""

import threading
from SMS import SMS, SMSPipelineElement

import os
import logger

class Terminal(SMSPipelineElement):
    """
    A class that uses STDIN and STDOUT to send and receive SMSs
    
    Initalization does nothing.
    
    Send simply prints the SMS to stdout
    
    Listen waits on STDIN for user input for one text message
    """
    
    def __init__(self):
        """Initalizes the Element"""
        SMSPipelineElement.__init__(self, 'terminal', 'terminal')
        logger.log(self, "terminal SMS device initialized. exit by writing DO:QUIT after 'To:'")
    
    def send(self, sms):
        """
        prints the given SMS to STDOUT
        """
        logger.log_send(self, sms)
        
        print '-------------\n'+str(sms)+'-------------'
                
    def listen(self):
        """
        Used STDIN and STDOUT to get string values for the to,
        from, and body attributes of the sms to build.
        
        Will return False if the To parameter is 'DO:QUIT'
        """
        print "Enter Your SMS:"
        sms_dict = {}
        
        sms_dict['to_number'] = raw_input("To: ")
        sms_dict['from_number'] = raw_input("From: ")
        sms_dict['body'] = raw_input("Body:\n")
        
        
        if sms_dict['to_number'] == "DO:QUIT":
            return False
                    
        sms = SMS.from_dictionary(sms_dict)
        
        logger.log_receive(self, sms)
        self.receive_callback(sms)
            