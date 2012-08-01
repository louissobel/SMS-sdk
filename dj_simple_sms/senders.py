"""
This module contains the interface for an SMS sending method
as well as the default one
"""
import json

from django.http import HttpResponse
from django.conf import settings

from models import SMS

class SMSSender(object):
    """
    The interface / superclass for an SMSSender, a class
    capable of somehow sending an SMS
    """
    
    def send(self, sms):
        """
        This function will be called when the send method of an
        SMS is called and therefore must be implemented to have any
        hope of sending a message!
        """
        raise NotImplementedError
    
    
    
    def respond_to_get(self, request):
        """
        This function will be called when a GET request is received on the SMS
        url. This is to allow for senders to be used with a downstream SMS
        service that communicates with Django via polling
        
        It therefore is allowed to raise NotImplementedError
        """
        raise NotImplementedError
    
     
class SMSQueueBasedSender(SMSSender):
    """
    Puts some of the common logic for sending SMSs via a queue into one place
    """
    
    def send(self, sms):
        """Enqueues the sms"""
        self.enqueue(sms)
        
    def enqueue(self, sms):
        """Implement the Enqueueing"""
        raise NotImplementedError
        
    
    def respond_to_get(self, request):
        """
        Pulls out the max_sms from the request or settings
        calls dequeue, with the up_to parameter specifying the
        maximum SMSs that may be dequeued
        """
        # Looks up the max_sms for this request in the following order:
        # 1. max_sms get parameter
        # 2. settings.SMS_MAX_SMS_GET
        # 3. 10
        max_sms = request.GET.get('max_sms', getattr(settings, 'SMS_MAX_SMS_GET', 10))
        sms_list = self.dequeue(up_to=max_sms)
    
        count = len(sms_list)
        data_out = {'sms_count':count,'sms':sms_list}

        return HttpResponse(json.dumps(data_out))
        
    def dequeue(self, up_to=None):
        """
        Dequeues up to up_to SMSs and returns as a list of dictionaries,
        each with:
        to_number, from_number, body
        """
        raise NotImplementedError
        

class DjangoQueueSMSSender(SMSQueueBasedSender):
    """
    A SMSQueueBasedSender that uses a Django model
    (ands its backing table) as the Queue
    """   
    def enqueue(self, sms):
        """Just saves it"""
        sms.save()
        
    def dequeue(self, up_to=None):
        """
        Will get up to up_to from the table using
        the django database API, ordered by datetime
        """
        if up_to is None:
            sms_set = SMS.objects.all().order_by('datetime')
        else:
            sms_set = SMS.objects.all().order_by('datetime')[:up_to]

        sms_list = list(sms_set.values('to_number','from_number','body'))

        for sms in sms_set:
            sms.delete()
        
        return sms_list