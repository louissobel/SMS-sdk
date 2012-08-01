# Create your views here.

from django.http import *
from django.views.decorators.csrf import csrf_exempt

from models import SMS, Device
from util import authorize, get_callable

import json

from django.conf import settings

import dj_simple_sms


@csrf_exempt
def sms(request):
    """
    Handles both the GET and the POST
    
    first thing is checks to make sure that the incoming message
    has the right secret device key
    
    POST:
    use the post data to create a SMS, and add it to the database
    will return empty 200 if success, or 500/400 with an {'error': <error message>} json body
    
    GET:
    gets up to max_sms sms, and returns them in a json list
    as well as a sms_count
    """   
    
    attrs = ('to_number','from_number','body')
    
    if request.method == "POST":
        
        device = authorize(request.POST.get('key'))
        if device is None:
            return HttpResponseForbidden()
        
        sms_dict = {}
        for attr in attrs:
            
            post_val = request.POST.get(attr)
            if post_val is None:
                return HttpResponseBadRequest("POST must have attribute %s" % attr)
            
            sms_dict[attr] = post_val
        
        new_sms = SMS(**sms_dict)
        
        sms_handlers = []
        sms_handler_tuple = getattr(settings,'SMS_HANDLERS',[])
        for sms_handler_string in sms_handler_tuple:
            sms_handlers.append(get_callable(sms_handler_string))
        
        # call the handlers? is this the best way?
        for sms_handler in sms_handlers:
            retval = sms_handler(new_sms)
            if retval is False:
                break
                
        return HttpResponse()
        
    elif request.method == "GET":
        """
        Remove this section if you will not be using
        The database as a queue for SMS sending-consumers
        """        
        device = authorize(request.GET.get('key'))
        if device is None:
            return HttpResponseForbidden(str(device))
        
        try:
            return dj_simple_sms.SMS_SENDER.respond_to_get(request)
        except NotImplementedError:
            return HttpResponseNotAllowed('GET')
        
        
        

        
        
        