import util
import senders

from django.conf import settings

# here I should get the sender from settings
_sms_sender_path = getattr(settings, 'SMS_SENDER_CLASS', None)
if _sms_sender_path is None:
    # default to senders.DjangoQueueSMSSender
    SMS_SENDER = senders.DjangoQueueSMSSender()
else:
    SMS_SENDER = util.get_class(_sms_sender_path)
    
import urls
import models

def sample_sms_handler(sms):
    """
    This is an example of the signature that a SMS handler should have
    """
    print "--------------"
    print "SMS RECEIVED:"
    print sms.to_message()
    print "--------------"
