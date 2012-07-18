from web import WebSMSClient
from terminal import SMSTerminal
from android_connect import AndroidSMS
import logger

import os

import time

class root:
    DEVICE = 'root'

def terminal_django():
    KEY = '515503a400d24ae68242d924311cd4eb'
    URL = 'http://localhost:8000/sms/'

    webclient = WebSMSClient(URL, KEY)
    termclient = SMSTerminal()


    webclient.receive(termclient.send)
    termclient.receive(webclient.send)

    webclient.start()
    termclient.start()
    
    
def android_django():
    
    logger.log(root, "Starting SMS pipe from Django to Android")
    
    KEY = '515503a400d24ae68242d924311cd4eb'
    URL = 'http://localhost:8000/sms/'
    
    PORT = 7801

    webclient = WebSMSClient(URL, KEY)
    androidclient = AndroidSMS(PORT)

    webclient.receive(androidclient.send, source='android')
    androidclient.receive(webclient.send, source='django')

    webclient.start()
    androidclient.start()
    
    try:
        while True:
            time.sleep(100) #waiting...
    except KeyboardInterrupt:
        logger.log_error(root, "KeyboardInterrupt - shutting down")
        os._exit(0)
    
    
    
    
def terminal_android():
    
    termclient = SMSTerminal()
    androidclient = AndroidSMS(7801)
    
    
    termclient.receive(androidclient.send)
    androidclient.receive(termclient.send)
    
    androidclient.start()
    termclient.start()
    
    
if __name__ == "__main__":
    android_django()
    
    