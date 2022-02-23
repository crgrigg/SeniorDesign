import socket
import threading

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


    __SlaveThreadFlag = false #Control Threads for Asychronous execution
    __SlaveTCPThread = ""     #Thread to control TCP Connection
    __SlaveUDPThread = ""     #Thread to control UDP Connection

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
            self.__SetState("Ready")
        if self.SlaveState == "Heard":
           return 1
        else:
           return -1

  
  

    def __SlaveTCPCommunication(self):
       
       #Recieve data from User Station
       self.__SlaveSocketTCP.recv(1024)


       #####Interperate Command########
       if self.__CommandID == 0x10: ##INIT
            #Establish UDP Communication
            if (self.__SlaveState == "Ready"):
                self.__SlaveSocketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
                self.__SlaveUDPThread = threading.Thread(target=self.__SlaveUDPCommunication)
                self.__SlaveUDPThread.start()
               

            #Initialize Input Data from User Station

            #Update CommandID and send Initial ROV Data
                
            #Update State
                self.__SetState("Initialized")

    def __SlaveUDPCommunication(self):


            