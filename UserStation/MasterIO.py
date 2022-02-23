
import socket
import threading
from bitarray import bitarray

#Author: Charles Griggs, Jay Franko
#Date:  February 18, 2022
#
#

# 
class MasterIO:

    ###############Class Defined Values #####################
    ######PRIVATE
   
    __ConnectAttempt = 0
    __FaultMessage = ""     #Allows user to read fault messages from Master Connection
    __FaultID = 0x00        # Used to identify the fault detected
    __MasterState = "Start" #Defines current status of Master Connection System
    __MasterSocketTCP = ""  #Client TCP Socket to be used by the program 
    __MasterSocketUDP = ""  #Client Socket used by Master to gather streaming data
    __MasterTCPPort = 4000  #Port Number Used to Define
    __MasterUDPPort = 8000  # Class Initializes 
    __ObjectID = 0xFF       #ID of object 
    __ObjectOffset = 0      #



    __MasterThreadFlag = false #Control Threads for Asychronous execution
    __MasterTCPThread = ""     #Thread to control TCP Connection
    __MasterUDPThread = ""     #Thread to control UDP Connection

    # User Connection Signals
    #  The first byte of communication will be a control command
    # INIT - 0x10   Initialize on board data and send to user. Master will then intialize data based on this input
    #           -Formatted Set of all data
    # UPDATE - 0x20 Update output signals from Master to Slave
    # GET   - 0x30  Retrieve Inputs Data from Slave and send to Master
    # ESTOP - 0x00   Emergency Stop all process  ## Can you Stop process?
    # CLOSE - 0xF0   End Communication
    __CommandID = 0xFF 


    __UDPData = 0 # Holds the data recieved over UDP
    __TCPData = 0 # Holds the data recieved over TCP

    ###

    #################  Methods ###################
    #####CONSTRUCTOR
    def __init__(self,MasterAddr = '127.0.0.1',MasterPort = 4000, MasterStreamPort = 8000,SlaveAddr = '127.0.0.1'):
           self.__MasterAddr = MasterAddr
           self.__SlaveAddr = SlaveAddr
           self.__MasterTCPPort = MasterPort
           self.__MasterUDPPort = MasterStreamPort
    #Set State  (don't know why i did this)
    def __SetState(self, StateString):
        self.__MasterState = StateString
    #Set Fault
    def __SetFault(self,FaultMessage,ID):
        self.__Faul
        tMessage = FaultMessage
        self._FaultID = ID

    #######PUBLIC
    #
    def MasterConnect(self):
         ##Create Socket and Attempt Connection
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
        
        ## Begin Communication Threads
        if self.MasterState == "Connected":
            self.__MasterTCPThread = threading.Thread(target=self.__MasterTCPCommunication)
            self.__MasterUDPThread = threading.Thread(target=self.__MasterUDPCommunication)
            self.__MasterTCPThread.start()
            self.__MasterUDPThread.start()
      
    
    #Initialize Input and Output Data Between the User Station and the ROV.
    #User Station Sends Initial User Data (Output Data)
    #ROV Station Return Initial ROV Data (Input Data)
    #Camera Streaming started over UDP
    def INIT(self):    
        if self.__MasterState == "Connected":
            self.__CommandID = 0x10
            self.__SetState("Intialized")
    
    #Gather Input Sensor Data from ROV
    def GET(self):
        if self.__MasterState == "Initialized":
            self.__CommandID = 0x20
           
    #Update Output Data from User Station
    def UPDATE(self):
        if self.__MasterState == "Initialized":
            self.__CommandID = 0x30

    #Emergency Stop
    def ESTOP(self):
        self.__SetState("EmergencyStop")
        self.__SetFault("EmergencyStop",0x00)
        self.__CommandID = 0x00
   
        

    #Executed by Master TCP Thread Continuously
    def __MasterTCPCommunication(self):

        while(self.__MasterThreadFlag == false):
            if self.__CommandID == 0x10: ##INIT
                self.__MasterSocketTCP.send("")
               

            elif self.__CommandID == 0x20: ## GET
                self.__MasterSocketTCP.send("")

            elif self.__CommandID == 0x30: ##UPDATE
                self.___MasterSocketTCP.send("")

            if self.__CommandID != 0xFF: ## if Initiated
                 self.__MasterSocketTCP.recv(1024)


    #Executed by Master UDP Thread
    def __MasterUDPCommunication(self):
        
        while(self.__MasterThreadFlag == false):
            #Add UDP Communication Information
            self.__UDPData = self.__MasterSocketUDP.recvfrom()