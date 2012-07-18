import requests
import sys

import threading
import time
import collections

import logger

from SMS import SMS

class WebSMSClient(threading.Thread):
    
    DEVICE = 'django connector'
    
    MAX_SMS = 10
    POLL_TIMEOUT = 5
    
    def __init__(self, url, key):
        threading.Thread.__init__(self)
        self.url = url
        self.key = key
        
        self.receive_callback = None
        
        logger.log(self, "created with device key %s and url %s" % (key, url))
        self.source = None
        self.sink = 'django'
        
        self.sms_queue = collections.deque()
        
        
    def send(self, sms):
    
        
        data_dict = {
            'to_number' : sms.to_number,
            'from_number' : sms.from_number,
            'body' : sms.body,
            'key' : self.key
        }
        
        result = requests.post(self.url, data=data_dict)
        
        # not much i really want to do with the result...
        # I guess report that it failed
        
        if not result.status_code == requests.codes.ok:
            
            
            
            
            errstring = ""
            for k,v in data_dict.items():
                errstring += "%s : %s\n" % (k, str(v))
            
            logger.log_error(self, "error %d - %s posting sms to %s" %
                (result.status_code, result.error, self.url))
            
            return False
        
        else:
            logger.log_send(self, sms)
            return True
            
    
    def receive(self, function, source=None):
        self.receive_callback = function
        self.source = source
        return self
        
    
    def fill_queue(self):
        """
        will fill the queue back up to however many it can
        will only try once
        """
        
        desired_sms = self.MAX_SMS - len(self.sms_queue)
        
        data_dict = {
            'max_sms' : desired_sms,
            'key' : self.key
        }
        
        result = requests.get(self.url, params=data_dict)
        
        if not result.status_code == requests.codes.ok:
            logger.log_error(self, "error filling queue: %d - %s" % (result.status_code, result.error))
        
        count = result.json['sms_count']
        
        for sms in result.json['sms']:
            new_sms = SMS.from_dictionary(sms)
            self.sms_queue.append(new_sms)
        
        logger.log(self, "grabbed %s messages from django queue" % count)
        
        return len(self.sms_queue)
        
        
        
    def run(self):
        # this is where i repeatedly poll the site for SMSs
        
        if self.receive_callback is None:
            return # i must not be part of an upstream pipeline
        
        # This variable sets the number of SMSs that i request at a go
    
        # now i start loop!
        while True:
            
            # if i'm out of things, i need to get some more!
            sms_count = len(self.sms_queue)
            if sms_count == 0:
                sms_count = self.fill_queue()
                
            if sms_count == 0:
                time.sleep(self.POLL_TIMEOUT)
            
            else:
                received_sms = self.sms_queue.popleft()
                
                logger.log_receive(self, received_sms)
                self.receive_callback(received_sms)
                time.sleep(.1) #do i need this? ja
                    
                
        
    
    