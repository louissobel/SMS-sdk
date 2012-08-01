import requests
import sys

import threading
import time
import collections

import logger

from SMS import SMS, SMSPipelineElement

DEBUG = True
VERBOSE = False

def save_error_response(response):
    """
    A function that, if DEBUG is True,
    will save the contents of response to file.
    
    Very useful for debugging HTTP error responses
    """
    if DEBUG:
        out_file = open('errresponse.html', 'w')
        out_file.write(response.content)
        out_file.close()


class WebConnector(SMSPipelineElement):
    """
    A SMSPipelineElement for communicating with a web service over HTTP
    
    Initalization creates an empty SMS queue
    
    Send sends an HTTP POST request with an SMS payload to the url specified
    
    Listen will use an internal queue and HTTP GET requests to the url
    in order to download and pass on SMSs
    """
    
    # the max queue size
    MAX_SMS = 10
    
    # seconds to wait between GET requests
    POLL_TIMEOUT = 5
    
    def __init__(self, url, key):
        """
        Initialzes the Element
        url is the url for requests.
        key is a string to include as a parameter to every request
        """
        SMSPipelineElement.__init__(self, 'django connector', 'django')
        
        self.url = url
        self.key = key        
        logger.log(self, "created with device key %s and url %s" % (key, url))
        
        # create an empty queue for SMSs
        self.sms_queue = collections.deque()
            
    def send(self, sms):
        """
        Sends an HTTP POST request to the url specified, with the following parameters,
        to_number, from_number, body, key
        """
        data_dict = {
            'to_number' : sms.to_number,
            'from_number' : sms.from_number,
            'body' : sms.body,
            'key' : self.key
        }
        
        # Make the request
        result = requests.post(self.url, data=data_dict)
        
        if result.status_code == requests.codes.ok:    
            logger.log_send(self, sms)
        else:
            logger.log_error(self, "error %d - %s posting sms to %s" %
                (result.status_code, result.error, self.url))               
            save_error_response(result)           
            return False
            
    def fill_queue(self):
        """
        Will attempt to GET enough SMSs from the URL to fill the internal queue
        back to MAX_SMS. If there are 5 in the queue, and MAX_LENGTH is 12, 7
        will be requested.
        
        Sens an HTTP GET request to the URL with the following parameters:
        max_sms, key
        
        Returns the new length of the sms_queue
        """
        current_length = len(self.sms_queue)
        desired_sms = self.MAX_SMS - current_length  
        data_dict = {
            'max_sms' : desired_sms,
            'key' : self.key
        }
        
        # Make the request
        result = requests.get(self.url, params=data_dict)      
          
        if result.status_code == requests.codes.ok: 
            for sms in result.json['sms']:
                new_sms = SMS.from_dictionary(sms)
                self.sms_queue.append(new_sms)
                
            count = result.json['sms_count']
            if VERBOSE:
                logger.log(self, "grabbed %s messages from django queue" % count)
                
            return current_length + count        
        else:
            logger.log_error(self, "error filling queue: %d - %s" % (result.status_code, result.error))
            save_error_response(result)
            return current_length
        
    def listen(self):
        """
        If there is an SMS in the queue, will pass it downstream.
        Otherwise, it will attempt to GET more SMSs. If it is unable,
        it will sleep for POLL_TIMEOUT seconds
        """
        sms_count = len(self.sms_queue)
        
        # If the queue is empty, I must try to download more
        if sms_count == 0:
            sms_count = self.fill_queue()
        
        # If it is _still_ empty...
        if sms_count == 0:
            time.sleep(self.POLL_TIMEOUT)
        else:
            received_sms = self.sms_queue.popleft()
            logger.log_receive(self, received_sms)
            self.receive_callback(received_sms)


    