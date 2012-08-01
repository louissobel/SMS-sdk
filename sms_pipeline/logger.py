from termstyle import termstyle
import datetime

_color_order = [
    'blue',
    'green',
    'cyan',
    'yellow',
]

_device_stylehash = {
    'root' : termstyle.magenta,
}

def timestamp():
    """Returns a timestamp"""
    return datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S")
    
def get_device_style(device):
    """
    Used to have a consistent color per device
    Mutates the module globals _color_order
    and _device_stylehash.    
    """
    
    if device.DEVICE in _device_stylehash:
        style = _device_stylehash[device.DEVICE]    
    else:
        if _color_order:
            new_color = _color_order.pop(0)
        else:
            raise RuntimeError("Logger out of colors!")
        style = getattr(termstyle, new_color)
        _device_stylehash[device.DEVICE] = style
        
    return style
    
def get_source(device):
    """
    Common code for getting the 'source' attribute
    of a SMSPipelineElement device
    """
    source = getattr(device, 'source')
    return 'from %s' % source if source else ''
    
def log(device, message):
    """Outputs the message with the logger style"""
    style = get_device_style(device)        
    print "[%s] - [%s]: %s" % (timestamp(), style(device.DEVICE), message)
        
def log_send(device, sms):
    """Turns a sent sms into a logmessage and logs it"""
    message = "Sent %s %s to %s" % (repr(sms), get_source(device), device.sink)
    log(device, message)
    
def log_receive(device, sms):
    """Turns a received sms into a logmessage and logs it"""
    message = "Received %s from %s" % (repr(sms), device.sink)
    log(device, message)
    
def log_error(device, message):
    """Styles a error message and logs it"""
    message = "!! -- %s" % message
    message = termstyle.red.bold(message)
    log(device, message)
    
def log_highlight(device, message):
    """Styles a highlight message and logs it"""
    message = termstyle.underlined.cyan.bold(message)
    log(device, message)