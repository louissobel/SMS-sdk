import threading

class SMS:
    """
    A class representing an SMS
    Importantly, it implements the serialization to the SMS protocol correctly
    using the __str__ method
    """
    
    @classmethod
    def from_dictionary(cls, sms_dict):
        """
        Creates and SMS using a dictionary with at least three keys:
        to_number, from_number, body
        """
        return cls(
            sms_dict['to_number'],
            sms_dict['from_number'],
            sms_dict['body'],
        )
    
    def __init__(self, to_number, from_number, body):
        """
        Initialization
        """
        self.to_number = to_number
        self.from_number = from_number
        self.body = body
        
    def trim(self):
        """
        Removes the last character.
        Used by parsers the remove extra newline
        """
        self.body = self.body[:-1]
        
        
    def short_body(self, max_length=15):
        """
        Returns a preview of the body that will not be longer
        than max_length
        """
        if len(self.body) > max_length - 3:
            return self.body[:max_length-3] + '...'
        else:
            return self.body
            
    def __repr__(self):
        return "<SMS to:%s|from:%s|body:%s>" % (self.to_number, self.from_number, repr(self.short_body()))
        
    def __str__(self):
        """
        Implements a serialization of the SMS according to the protocol
        described in the documentation.
        """
        out_body = self.body + '\n'
        
        # Count newlines
        length = reduce(lambda s,c : s + (c == '\n'), out_body, 0)
                     
        out = ""
        out += "TEXT\n"
        out += "LENGTH:%d\n" % length
        out += "TO:%s\n" % self.to_number
        out += "FROM:%s\n" % self.from_number
        out += "\n" # end headers
        out += "%s" % out_body
        return out
        
        
class SMSPipelineElement(threading.Thread):
    """
    A super class for elements of an SMS Pipeline
    Subclasses must override the send and listen methods
    
    Is a threading.Thread.
    """

    def __init__(self,device,sink):
        """
        Initializes the element with string identifyers
        device and sink. Device is the what this element
        represents, and sink is the place that to which
        it sends an SMS
        """
        threading.Thread.__init__(self)
        self.DEVICE = device
        self.source = None
        self.sink = sink
        self.receive_callback = None
        self.upstream = False

    def send(self, sms):
        """
        Send an SMS downstream
        """
        raise NotImplementedError

    def listen(self):
        """
        If this is part of an upstream pipeline, this method
        will be repeatedly called as the element runs.
        
        It should somehow obtain an SMS from downstream, then
        call self.receive_callback on that SMS.
        
        If the method returns False, the pipeline element will shutdown.
        """
        raise NotImplementedError

    def receive(self, function, source=None):
        """
        Called to register a function as the receive_callback - 
        the function used to pass an SMS upstream. Calling this function
        sets the upstream flag of this element to True.
        """
        self.receive_callback = function
        self.source = source
        self.upstream = True
        return self

    def run(self):
        """
        If this element is part of an upstream pipeline
        (if it has a receive callback), this method will
        call listen() until it returns False.
        """
        if not self.upstream:
            # then i'm not part of an upstream pipeline
            return

        while True:
            retval = self.listen()  
            if retval is False:
                break
                
    def cleanup(self):
        """
        Will be called on pipeline shutdown, override it to add any cleanup
        behavior necessary
        """
        pass