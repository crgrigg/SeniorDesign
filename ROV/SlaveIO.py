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
    __SlaveState = "Start"
    __FaultMessage = ""
    __FaultID = 0x00
    __SlaveSocketTCP = ""
    __SlaveSocketUDP = ""
    __SlaveTCPPort = 4000
    __SlaveUDPPort = 8000

    ################# Methods ######################
    #####PRIVATE
    #Constructor
    def __init__(self,SlaveAddr = '127.0.0.1',SlavePort = 4000, MasterAddr = '127.0.0.1'):
        self.__SlaveAddr = SlaveAddr
        self.__MasterAddr = MasterAddr
        self.__SlaveTCPort = SlavePort
    
    #Set State
    def __SetState(self, StateString)

