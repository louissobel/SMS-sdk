from sms.models import SMS

def sample_sms_handler(sms):
    print sms.to_message()
    
    
    
def echo_sms_handler(sms):
    foobar = sms.send()
    
    