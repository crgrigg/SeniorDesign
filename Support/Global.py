

#Describes Current Data of the system for the purpose of communication with the
# Global Data Shared by threads
MemMap = {
                     "MotorX1": {"ObjectID": 1,"MotorID": 1,"Speed":  1234},
                     "MotorX2": {"ObjectID": 1,"MotorID": 2,"Speed":  1234},
                     "MotorY1": {"ObjectID": 1,"MotorID": 3,"Speed":  1234},
                    
                     "DepthSensor": {"ObjectID": 2,"Depth": 1234}, 
                     "TempSensor": {"ObjectID": 3,"Temp":0},
                     "UltraSensor1":{"ObjectID": 4,"SensorID": 1,"Distance": 0},
                     "UltraSensor2":{"ObjectID": 4,"SensorID": 1,"Distance": 0},
                     "UltraSensor3":{"ObjectID": 4,"SensorID": 1,"Distance": 0},
                     "UltraSensor4":{"ObjectID": 4,"SensorID": 1,"Distance": 0},
                      "Camera" : {"ObjectID": 5, "Enable": 0, "Resolution":""}
           }

# Global Memory to Map Xbox Controller Inputs to other Threads
ControllerMap = {
                    "Buttons":{"A":0,"B":0,"X":0,"Y":0,"Start":0,"Back":0},
                    "Trigger":{"Left":0,"Right":0},
                    "Bumper":{"Left":0,"Right":0},
                    "D_Pad":{"Up":0,"Down":0,"Left":0,"Right":0},
                    "Stick":{"Left":{"ValueX":0,"ValueY":0},"Right":{"ValueX":0,"ValueY":0}
                }

#Contains Video Data Gathered over UDP connections
 VideoMap = ''
 
