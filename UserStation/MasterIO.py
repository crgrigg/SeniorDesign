
import socket
import threading
import pickle
import queue


#Author: Charles Griggs, Jay Franko
#Date:  February 18, 2022
#
#

# 
class MasterIO:

    ###############Class Defined Values #####################
    ######PRIVATE
   
  
    ###

    #################  Methods ###################
    #####CONSTRUCTOR
    def __init__(self,MasterAddr = '127.0.0.1',MasterPort = 4000, MasterStreamPort = 8000,SlaveAddr = '127.0.0.1'):
           
           self.__MasterState = "Start" #Defines current status of Master Connection System
           self.__ConnectAttempt = 0
           self.__FaultMessage = ""     #Allows user to read fault messages from Master Connection
           self.__FaultID = 0x00        # Used to identify the fault detected
           

           self.__MasterAddr = MasterAddr
           self.__SlaveAddr = SlaveAddr
           self.__MasterTCPPort = MasterPort
           self.__MasterUDPPort = MasterStreamPort
           #Client TCP Socket to be used by the program 
           self.__MasterSocketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
           #Client Socket used by Master to gather streaming data
           self. __MasterSocketUDP = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
           
           # User Connection Signals
           #  The first byte of communication will be a control command
           # INIT  -   b'\x10'   Initialize on board data and send to user. Master will then intialize data based on this input
           #           -Formatted Set of all data
           # UPDATE - b'\x20' Update output signals from Master to Slave
           # GET   -  b'\x30'  Retrieve Inputs Data from Slave and send to Master
           # ESTOP -  b'\xFF'   Emergency Stop all process  ## Can you Stop process?
           # CLOSE -  b'\xA0'   End Communication
           self.__CommandID = queue.PriorityQueue() #Emergency Commmand Takes Priority
           self.__ReturnID = b''
           self.__SendMessage = ''
           self.__RecieveMessage = ''


           #Thread Management Values
           self.__MasterThreadFlag = false #Control Threads for Asychronous execution
           self.__MasterTCPThread = threading.Thread(target=self.__MasterTCPCommunication)
           self.__MasterUDPThread = threading.Thread(target=self.__MasterUDPCommunication)
           

        
   
    #######PUBLIC
    #
    def MasterConnect(self):
         ##Create Socket and Attempt Connection
        if self.MasterState == "Start" and self.__ConnectAttempt != 3: 
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
            self.__MasterTCPThread.start()
            self.__MasterUDPThread.start()
      
    
    #Initialize Input and Output Data Between the User Station and the ROV.
    #User Station Sends Initial User Data (Output Data)
    #ROV Station Return Initial ROV Data (Input Data)
    #Camera Streaming started over UDP
    def INIT(self):    
        if self.__MasterState == "Connected":
            self.__CommandID.
            self.__SetState("Intialized")
    
    #Gather Input Sensor Data from ROV
    def GET(self):
        if self.__MasterState == "Initialized":
            self.__CommandID = b'\x20'
           
    #Update Output Data from User Station
    def UPDATE(self):
        if self.__MasterState == "Initialized":
            self.__CommandID =b'\x30'

    #Emergency Stop
    def ESTOP(self):
        self.__SetState("EmergencyStop")
        self.__SetFault("EmergencyStop",0x00)
        self.__CommandID = 0x00
   
     #Set State  (don't know why i did this)
    def __SetState(self, StateString):
        self.__MasterState = StateString
    #Set Fault
    def __SetFault(self,FaultMessage,ID):
        self.__Faul
        tMessage = FaultMessage
        self._FaultID = ID

    #Executed by Master TCP Thread Continuously
    def __MasterTCPCommunication(self):

        while(self.__MasterThreadFlag == false):

          self.__SendMessage.append(CommandID)


    #Executed by Master UDP Thread
    def __MasterUDPCommunication(self):
        
        while(self.__MasterThreadFlag == false):
            #Add UDP Communication Information
            self.__UDPData = self.__MasterSocketUDP.recvfrom()