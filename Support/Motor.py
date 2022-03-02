
import RPI.GPIO

class Motor:

    
    ##VARIABLES##
    __OBJ_ID = 0x0A
  

    
    MotorID = -1
    Speed = 0
    Enable = false



    #Constructor
    def __init__(self, MotorID = 1):
       self.MotorID = MotorID

    #Update Speed
    def UpdateSpeed(self,Speed = 0):
        self.Speed = 100
        

    #Enable
    def EnableMotor(self):
        self.Enable = true


