import socket


#Autho: Charles Griggs, Jay Franko
#Date: February 18, 2022
#
#
# ROV Connection Signals
# 


class SlaveIO:

    #############Class Defined Values #######################
    #######PRIVATE
    __SlaveTCPState = "Start"  # Determines the state of the ROV Connection to the User Station
    __SlaveUDPState = "Start" 
    __FaultMessage = ""     # Shows Message associated with errors from connection
    __FaultID = 0x00        # Fault ID for the Error
    __SlaveSocketTCP = ""   # Socket object for TCP connection
    __SlaveSocketUDP = ""   #Socket object for UDP Connection
    __SlaveTCPPort = 4000   #TCP Port being used
    __SlaveUDPPort = 8000   #UDP Port being used
    __ListenCount = 0       #Number of times Listen timed out
    __SlaveConnection = ""  #Connection Object from accepting a connection

    ################# Methods ######################
    #####PRIVATE
    #Constructor
    def __init__(self,SlaveAddr = '127.0.0.1',SlavePort = 4000, MasterAddr = '127.0.0.1'):
        self.__SlaveAddr = SlaveAddr
        self.__MasterAddr = MasterAddr
        self.__SlaveTCPort = SlavePort
    #Set State
    def __SetState(self, StateString):
        self.__SlaveState = StateString
    #Set Fault
    def __SetFault(self,FaultMessage,ID):
        self.__FaultMessage = FaultMessage
        self._FaultID = ID

   #####PUBLIC

    def SlaveTCPStart(self):
        if self.SlaveTCPState == "Start":
            self.__SlaveSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            try:
                self.__SlaveSocketTCP.bind(('',self.__SlaveTCPPort))
            except socket.error:
                self.__SetFault("")
            else:
                self.__SetState("Bound")
        elif self.__ConnectAttempt == 3:
            self.__SetState("ExitwithFault")
            self.__SetFault("Failed to Make connection",0x02)

        if self.SlaveTCPState == "Bound":
             while self.__SlaveState == "Bound" and self.__ListenCount < 5:
                try:
                    self.__SlaveSocketTCP.listen(self.__ListeningTime) 
                except socket.error:
                    self.__SetFault("")
                else:
                    self.__SetState("Heard")
                finally:
                    self.__ListenCount += 1

        if self.SlaveState == "Heard":
            self.__SlaveConnection, self.__MasterAddr = self.__SlaveSocketTCP.accept()
        if self.SlaveState == "Heard":
           return 1
        else:
           return -1

  
    def SlaveUDPStart(self):
        if self.SlaveUDPState == "Start":
            self.__SlaveSocketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            return 1
        else:
            return -1