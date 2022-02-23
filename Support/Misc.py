  # Used by Master and Slave to Translate Protocol Data 
    #
    #
    def __TranslateObj(self, MyMsg):

        if ObjectID == 0x0: # ROV Status
            Message = TranslateAtt();
        elif ObjectID == 0xFF: # ROV Faults Detected
            MyMsg = TranslateAtt();
        elif ObjectID == 0x0A: # Motor Control
            MyMsg = TranslateAtt();
        elif ObjectID == 0x0B: # Cameral Control Object
            MyMsg = TranslateAtt();
        elif ObjectID == 0x11: #Ultrasonic Sensor
            MyMsg = TranslateAtt();
        elif ObjectID == 0x12: #Depth Sensor
            MyMsg = TranslateAtt();
        elif ObjectID == 0x13: #Temperature Sensor
            MyMsg = TranslateAtt();
        return Message


    # Used to Translate Attributes into the Protocol format to send of TCP
    #
    #
    def __TranslateAtt(self):

        return Message

    # Used to wrap
