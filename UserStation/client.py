# lets make the client code
import cv2, socket, pickle, struct
from tkinter import *
import tkinter
from PIL import Image, ImageTk
import threading
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import MotorClient
import MasterDB
import time
import XboxControllerPWM
from time import sleep
import Global
import DataSetCapture

#Enable to save dataset values
DataSetActive = Global.DataSetActive
DataCaptureTime = time.time()
DataTimeGap = .25


AutoState = 0
LightState = 0
#cascade_src = 'C:/Users/rober/OneDrive/Desktop/Images/classifier/cascade.xml'
#model_cascade = cv2.CascadeClassifier (cascade_src) #Using the cascade classifier

Paw = Image.open("C:/Users/rober/OneDrive/Desktop/BigOlFatPaw.jpg")

  
MotorThread = threading.Thread(target = MotorClient.motor_client)
MotorThread.start()

ControllerThread = threading.Thread(target = XboxControllerPWM.get_signals)
ControllerThread.start()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.253.85'
port = 9997
client_socket.connect((host_ip,port)) # a tuple


# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("1080x720")
win.attributes("-topmost", True)
win.title("Underwater Unmanned Vehicle (UUV)")
win.configure(background='orange')


# Create a Label to capture the Video frames
Videolabel =Label(win)
Videolabel.grid(row=0, column=0,rowspan = 10,columnspan=10)

Paw = Paw.resize((200,200),Image.ANTIALIAS)
PawPhoto = ImageTk.PhotoImage(Paw)
Pawlabel = Label(win)
Pawlabel.grid(row=0,column=13,rowspan=5,columnspan=4)
Pawlabel.imgtk = PawPhoto
Pawlabel.configure(image=PawPhoto)
   






ROVStatusRow = 11
ROVStatusCol = 0
RowIndex = 2
ColumnSpace = 2
SensorRow = ROVStatusRow
SensorCol = ROVStatusCol + ColumnSpace +10
SensorColSpace = 3

TitleFont = ("",18,"bold")
EntryFont = ("",11)
ValueFont =  ("",11)


ROVStatus = Label(win,bg = "orange", font=TitleFont)
ROVStatus.grid(row=ROVStatusRow,column = ROVStatusCol, columnspan=3)
ROVStatus.configure(text="UUV Status")

#Light Status
LightStatus = Label(win,bg="orange",font=EntryFont)
LightStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
LightStatus.configure(text ="Light Status")
LightStatusValue = Label(win,bg="orange", font =ValueFont)
LightStatusValue.grid(row=ROVStatusRow  + RowIndex,column=ROVStatusCol + ColumnSpace)
LightStatusValue.configure(text="")
RowIndex += 1

#Horizontal Motor Speed
HorizontalMotorSpeed = Label(win,bg="orange",font=EntryFont)
HorizontalMotorSpeed.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol)
HorizontalMotorSpeed.configure(text ="Horizontal Motor Speed")
HorizontalMotorValue = Label(win,bg="orange",font=ValueFont)
HorizontalMotorValue.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol  + ColumnSpace)
HorizontalMotorValue.configure(text ="")
RowIndex += 1

#Verticle Motor Speed
VerticleMotorSpeed = Label(win,bg="orange",font=EntryFont)
VerticleMotorSpeed.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol)
VerticleMotorSpeed.configure(text ="Vertical Motor Speed")
VerticleMotorValue = Label(win,bg="orange",font=ValueFont)
VerticleMotorValue.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol  + ColumnSpace)
VerticleMotorValue.configure(text ="")
RowIndex += 1

#Vertical Motor Status
VerticleMotorLock = Label(win,bg="orange",font=EntryFont)
VerticleMotorLock.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
VerticleMotorLock.configure(text ="Vertical Motor Status")
VerticleMotorLockValue = Label(win,bg="orange",font=ValueFont)
VerticleMotorLockValue.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol  + ColumnSpace)
VerticleMotorLockValue.configure(text ="")
RowIndex += 1

#Auto Mode
AutoModeStatus = Label(win,bg="orange",font=EntryFont)
AutoModeStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
AutoModeStatus.configure(text ="Auto Mode")
AutoModeValue = Label(win,bg="orange",font=ValueFont)
AutoModeValue.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol + ColumnSpace)
AutoModeValue.configure(text ="")
RowIndex += 1

#CPU Temperature
CPUTempStatus = Label(win,bg="orange",font=EntryFont)
CPUTempStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
CPUTempStatus.configure(text ="CPU Temp [C]")
CPUTempValue = Label(win,bg="orange",font=ValueFont)
CPUTempValue.grid(row = ROVStatusRow + RowIndex , column = ROVStatusCol + ColumnSpace)
CPUTempValue.configure(text ="")
RowIndex += 1

##ROV Error Status
#ROVErrorStatus = Label(win,bg="orange",font=EntryFont)
#ROVErrorStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
#ROVErrorStatus.configure(text ="UUV Error Status")
#ROVErrorValue = Label(win,bg="orange",font=ValueFont)
#ROVErrorValue.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol + ColumnSpace )
#ROVErrorValue.configure(text ="")
#RowIndex += 1

#Sensor Data
RowIndex = 2
SensorData = Label(win,bg = "orange",font=TitleFont)
SensorData.grid(row=SensorRow,column = SensorCol, columnspan=4)
SensorData.configure(text="SensorData")

# Temp Sensor
TempSensorStatus = Label(win,bg="orange",font=EntryFont)
TempSensorStatus.grid(row = SensorRow + RowIndex, column = SensorCol)
TempSensorStatus.configure(text ="Temperature [F]")
TempSensorValue = Label(win,bg="orange",font=ValueFont)
TempSensorValue.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
TempSensorValue.configure(text ="")
RowIndex += 1

#Pressure
PressureSensorStatus = Label(win,bg="orange",font=EntryFont)
PressureSensorStatus.grid(row = SensorRow + RowIndex, column = SensorCol)
PressureSensorStatus.configure(text ="Pressure [kPa]")
PressureSensorValue = Label(win,bg="orange",font=ValueFont)
PressureSensorValue.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
PressureSensorValue.configure(text ="")
RowIndex += 1

#Ultrasonic Sensor 1
UltrasonicSensor1Status = Label(win,bg="orange",font=EntryFont)
UltrasonicSensor1Status.grid(row = SensorRow + RowIndex, column = SensorCol)
UltrasonicSensor1Status.configure(text ="Left Distance [mm]")
UltrasonicSensor1Value = Label(win,bg="orange",font=ValueFont)
UltrasonicSensor1Value.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
UltrasonicSensor1Value.configure(text ="")
RowIndex += 1

#Ultrasonic Sensor 2
UltrasonicSensor2Status = Label(win,bg="orange",font=EntryFont)
UltrasonicSensor2Status.grid(row = SensorRow + RowIndex, column = SensorCol)
UltrasonicSensor2Status.configure(text ="Right Distance [mm]")
UltrasonicSensor2Value = Label(win,bg="orange",font=ValueFont)
UltrasonicSensor2Value.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
UltrasonicSensor2Value.configure(text ="")
RowIndex += 1

#Ultrasonic Sensor 3
UltrasonicSensor3Status = Label(win,bg="orange",font=EntryFont)
UltrasonicSensor3Status.grid(row = SensorRow + RowIndex, column = SensorCol)
UltrasonicSensor3Status.configure(text ="Bottom Distance [mm]")
UltrasonicSensor3Value = Label(win,bg="orange",font=ValueFont)
UltrasonicSensor3Value.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
UltrasonicSensor3Value.configure(text ="")
RowIndex += 1


data = b""
payload_size = struct.calcsize("Q")

Database = MasterDB.MasterDB()

def show_graphs():
   
    global plot,win
    global Videolabel,DataSetActive,AutoDetect,NoGraph
    global AutoState, LightState
    
   
    while True:
        if Global.LightState == 1 or Global.LightState == 2:
            LightStatusStr = "Enabled"
        else: LightStatusStr = "Disabled"
     
      
        #Auto Mode State Machine
       
        if Global.AutoState == 1 or Global.AutoState == 2:
            Global.AutoMode = True
        else: Global.AutoMode = False

        Global.ControllerMap["START"]["Value"] == 0 and AutoState == 0

        #if Global.ControllerMap["Bumper"]["Right"] == 1:
        #    Global.MemMap["Vertical Lock"]["Lock"] = "Locked"
        #else:
        #    Global.MemMap["Vertical Lock"]["Lock"] = "Unlocked"

       

        if Global.VertState == 1 or Global.VertState == 2:
            Global.MemMap["Vertical Motor"]["Lock"] = "Locked"
        else: 
            Global.MemMap["Vertical Motor"]["Lock"] = "Unlocked"
            saved = Global.ControllerMap["Stick"]["Right"]["ValueY"]

        #UI Section Text
        #LightStatusStr = str(Global.MemMap["Lights"]["Status"])
        HorizontalMotorStr = str(round(Global.ControllerMap["Stick"]["Left"]["ValueY"] * 100)) + '%'
        if Global.VertState == 1 or Global.VertState == 2:
            VerticalMotorStr = str(round(saved * 100)) + '%'
        else:
            VerticalMotorStr = str(round(Global.ControllerMap["Stick"]["Right"]["ValueY"] * 100)) + '%'
        VerticalMotorLockStr = Global.MemMap["Vertical Motor"]["Lock"]
       
        if Global.AutoMode: AutoModeStr = "Enabled"
        else: AutoModeStr = "Disabled"
        CPUTempStr = str(Global.MemMap["CPU"]["Temp"])
       # ROVErrStr = str(Global.MemMap["Error"]["Message"])
        TempStr = str(Global.MemMap["TempSensor"]["TempF"])
        PressureStr = str(Global.MemMap["DepthSensor"]["Depth"] * 4)
        UltraSonic1Str = str(Global.MemMap["UltraSensor1"]["Distance"])
        UltraSonic2Str = str(Global.MemMap["UltraSensor2"]["Distance"])
        UltraSonic3Str = str(Global.MemMap["UltraSensor3"]["Distance"])
        
        #ROV Status
        LightStatusValue.configure(text=LightStatusStr)
        HorizontalMotorValue.configure(text=HorizontalMotorStr)
        VerticleMotorValue.configure(text=VerticalMotorStr)
        VerticleMotorLockValue.configure(text=VerticalMotorLockStr)
        AutoModeValue.configure(text=AutoModeStr)
        CPUTempValue.configure(text=CPUTempStr)
        #ROVErrorValue.configure(text=ROVErrStr)

        #SensorData
        TempSensorValue.configure(text=TempStr)
        PressureSensorValue.configure(text=PressureStr)
        UltrasonicSensor1Value.configure(text=UltraSonic1Str)
        UltrasonicSensor2Value.configure(text=UltraSonic2Str)
        UltrasonicSensor3Value.configure(text=UltraSonic3Str)
        sleep(.001)

AutoModeTimer = 0
def show_frames():

    #global data
    global client_socket, win, Videolabel, data, payload_size, DbTimer
    global Database, DataTimeGap, DataSetActive,DataCaptureTime,AutoModeTimer
    global AutoState
    #global data
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)

 

    # Get the latest frame and convert into Image
   
    #If AutoDetecting/ in AutoMode
    if Global.AutoMode:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        model = model_cascade.detectMultiScale(gray, 1.1, 1)
        AvgCenterMassX = 0
        AvgCenterMassY = 0
        NumRect = 0
        FirstYCenter = 0
        LastYCenter = 0
        for (x, y, w, h) in model:
            if NumRect == 0:
                FirstYCenter = (y+h)/2
            LastYCenter = (y+h)/2
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            AvgCenterMassX += (x+w)/2
            AvgCenterMassY += (y+h)/2
            NumRect += 1
        if NumRect != 0:
            AvgCenterMassX = AvgCenterMassX/NumRect
            AvgCenterMassY = AvgCenterMassY/NumRect
            AutoModeTimer = 0
        elif AutoModeTimer == 0:
            AutoModeTimer = time.time()
        elif time.time() - AutoModeTimer > 1:
            AutoModeTimer = 0
            #Global.AutoMode = False
            Global.AutoState = 0
        # vertical-ish pipe
        Global.ControllerMap["Stick"]["Left"]["ValueY"] = 0.15
        TurnSpeedR = 0 + (1 - 0) * ((AvgCenterMassX - 240) / (480 - 240))
        TurnSpeedL = 0 + (1 - 0) * ((AvgCenterMassX - 0) / (240 - 0))
        if AvgCenterMassX >= 240:
            Global.ControllerMap["Trigger"]["Right"] = TurnSpeedR/2
            print("Going Right: ",TurnSpeedR)
        elif AvgCenterMassX < 240:
            Global.ControllerMap["Trigger"]["Left"] = TurnSpeedL/2
            print("Going Left: ",TurnSpeedL)

        # horizontal pipe
        #if FirstYCenter <= LastYCenter + 75 and FirstYCenter >= LastYCenter - 75 and NumRect >= 4:
        #    Global.ControllerMap["Stick"]["Left"]["ValueY"] = 0.3;
        #    Global.ControllerMap["Trigger"]["Left"] = .5;

        if Global.AutoMode == False:
            Global.ControllerMap["Stick"]["Left"]["ValueY"] = 0.0
            Global.ControllerMap["Trigger"]["Right"] = 0
            Global.ControllerMap["Trigger"]["Left"] = 0

    cv2image= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    if DataSetActive == True and time.time() - DataCaptureTime >= DataTimeGap:
        DataSetCapture.DataSetSave(cv2image)
        DataCaptureTime = time.time()
    imgtk = ImageTk.PhotoImage(image = img)
    Videolabel.imgtk = imgtk
    Videolabel.configure(image=imgtk)
   
        
    # Repeat after an interval to capture continiously
    Videolabel.after(1, show_frames)


GraphThread = threading.Thread(target=show_graphs)
GraphThread.start()

#computer_visual()
show_frames()
win.mainloop()