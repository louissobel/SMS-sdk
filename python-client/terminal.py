"""
SMS sender emulator from terminal
"""

import threading
from SMS import SMS

import os

class SMSTerminal(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)        
        self.receive_callback = None
    
    def send(self, sms):
        """
        prints the given SMS to STDOUT
        """
        
        print sms
        
        
        
        
    def receive(self, function):
        self.receive_callback = function
        
        
        
    def run(self):
        
        if self.receive_callback is None:
            raise AssertionError("Recieve callback cannot be None!")
            
        while True:
            print "Enter Your SMS:"
            sms_dict = {}
            
            sms_dict['to_number'] = raw_input("To: ")
            sms_dict['from_number'] = raw_input("From: ")
            sms_dict['body'] = raw_input("Body:\n")
            
            
            if sms_dict['to_number'] == "DO:QUIT":
                os._exit(0)
            
            print "sending..."
            
            sms = SMS.from_dictionary(sms_dict)
            
            print "here"
            
            self.receive_callback(sms)
            