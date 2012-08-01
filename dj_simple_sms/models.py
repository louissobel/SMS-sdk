"""
Models

Defines SMS, and Device
"""
from django.db import models
from django.contrib import admin
import dj_simple_sms
import uuid

class SMS(models.Model):
    """
    A model representing an SMS
    """
    to_number = models.CharField(max_length=64)
    from_number = models.CharField(max_length=64)
    body = models.CharField(max_length=160)
    datetime = models.DateTimeField(auto_now_add=True)

    def send(self):
        """
        Passes this message to the send method of the current SENDER
        """
        dj_simple.sms.SMS_SENDER.send(self)
              
    def to_message(self):
        return "To: %s\nFrom: %s\nBody:\n%s" % (self.to_number, self.from_number, self.body)
    
  
class Device(models.Model):
    """
    A model representing a device that is allowed to post or download text messages.
    Identified by a random string (uuid)
    """
    
    name = models.CharField(max_length=64)
    
    def generate_key():  
        return uuid.uuid4().hex
    key = models.CharField(max_length=32,default=generate_key,db_index=True,editable=False)
    

class SMSAdmin(admin.ModelAdmin):
    list_display = ('to_number','from_number','body')
    ordering = ('datetime',)
    
class DeviceAdmin(admin.ModelAdmin):
    
    list_display= ('name','key')
    
    
admin.site.register(SMS, SMSAdmin)
admin.site.register(Device, DeviceAdmin)