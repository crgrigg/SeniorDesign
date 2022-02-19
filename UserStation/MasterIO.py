import socket


#Author: Charles Griggs, Jay Franko
#Date:  February 18, 2022
#
#
# User Connection Signals
#  The first byte of communication will be a control command
# INIT - 0x01   Initialize on board data and send to user. Master will then intialize data based on this input
#           -Formatted Set of all data
# UPDATE - 0x02 Update output signals from Master to Slave
# GET   - 0x03  Retrieve Inputs Data from Slave and send to Master
# ESTOP - 0x0   Emergency Stop all process  ## Can you Stop process?
# 
class MasterIO:

    ###############Class Defined Values #####################
    ######PRIVATE
    __MasterState = "Start" #Defines current status of Master Connection System
    __ConnectAttempt = 0
    __FaultMessage = ""     #Allows user to read fault messages from Master Connection
    __FaultID = 0x00        # Used to identify the fault detected
    __MasterSocketTCP = ""  #Client TCP Socket to be used by the program 
    __MasterSocketUDP = ""  #Client Socket used by Master to gather streaming data
    __MasterTCPPort = 4000  #Port Number Used to Define
    __MasterUDPPort = 8000  # Class Initializes 

    #################  Methods ###################
    ######PRIVATE
    #Constructor
    def __init__(self,MasterAddr = '127.0.0.1',MasterPort = 4000, MasterStreamPort = 8000,SlaveAddr = '127.0.0.1'):
           self.__MasterAddr = MasterAddr
           self.__SlaveAddr = SlaveAddr
           self.__MasterPort = MasterPort
           self.__MasterUDPPort = MasterStreamPort
    #Set State
    def __SetState(self, StateString):
        self.__MasterState = StateString
    #Set Fault
    def __SetFault(self,FaultMessage,ID):
        self.__FaultMessage = FaultMessage
        self._FaultID = ID

    #######PUBLIC
    #
    def MasterConnect(self):
         ##Create Socket and Attempt Connect
        if self.MasterState == "Start" and self.__ConnectAttempt != 3:
            self.__MasterSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.__MasterSocketTCP.connect((self.__SlaveAddr,self.__MasterPort))
            except socket.error:
                self.__SetFault("TCP Socket.connect failed. Verify IP Address and Port.",0x01)
            else:
                self.__SetState("Connected")
            finally:
                self.__ConnectAttempt += 1
        elif self.__ConnectAttempt == 3:
            self.__SetState("ExitwithFault")
            self.__SetFault("Failed to Make connection",0x02)
    
    #
    def INIT(self):
        
        if self.__MasterState == "Connected":
              
    #
    def GET(self):

    #
    def UPDATE(self):

    #
    def ESTOP(self):
          



        
           

