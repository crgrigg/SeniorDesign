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
DataSetActive = False
DataCaptureTime = time.time()
DataTimeGap = .25

AutoDetect = False
cascade_src = 'C:/Users/rober/OneDrive/Desktop/Images/Models/full_lbp_classifier/cascade.xml'
model_cascade = cv2.CascadeClassifier (cascade_src) #Using the cascade classifier

MotorThread = threading.Thread(target = MotorClient.motor_client)
MotorThread.start()

ControllerThread = threading.Thread(target = XboxControllerPWM.get_signals)
ControllerThread.start()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.253.85'
port = 9997
client_socket.connect((host_ip,port)) # a tuple

ListSize = 50
TempValue = []
PressureValue = []
ULValue = []
URValue = []
UBValue = []

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
#win.geometry("1920x1080")
win.attributes("-topmost", True)
win.title("Underwater ROV")
win.configure(background='orange')


VideoLabelRow = 0
VideoLabelCol = 0


# Create a Label to capture the Video frames
Videolabel =Label(win)
Videolabel.grid(row=VideoLabelRow, column=VideoLabelCol)

#Graphs
figure = plt.figure(figsize=(5.5,6),dpi=100)
TempPlot = figure.add_subplot(2,1,1)
TempPlot.set_xlabel("time [s]")
TempPlot.set_ylabel("Temperature [C]")
TempPlot.set_title("Temperature", fontweight='bold')
TempPlot.set_facecolor('orange')
TempPlot.set_ylim(10,30)
PressurePlot = figure.add_subplot(2,1,2)
PressurePlot.set_xlabel("time[s]")
PressurePlot.set_ylabel("Pressure [kPa]")
PressurePlot.set_title("Pressure", fontweight='bold')
PressurePlot.set_facecolor('orange')
PressurePlot.set_ylim(10,30)
figure.set_facecolor('orange')
canvas = FigureCanvasTkAgg(figure,win)
canvas.get_tk_widget().grid(row=0,column=100)

figure1 = plt.figure(figsize=(12,4),dpi=100)
USLeft = figure1.add_subplot(1,3,1)
USLeft.set_xlabel("time [s]")
USLeft.set_ylabel("Distance [mm]")
USLeft.set_title("Left Ultrasonic", fontweight='bold')
USLeft.set_facecolor('orange')
USRight = figure1.add_subplot(1,3,2)
USRight.set_xlabel("time [s]")
USRight.set_ylabel("Distance [mm]")
USRight.set_title("Right Ultrasonic", fontweight='bold')
USRight.set_facecolor('orange')
USBottom = figure1.add_subplot(1,3,3)
USBottom.set_xlabel("time [s]")
USBottom.set_ylabel("Distance [mm]")
USBottom.set_title("Bottom Ultrasonic", fontweight='bold')
USBottom.set_facecolor('orange')
figure1.set_facecolor('orange')
canvas1 = FigureCanvasTkAgg(figure1,win)
canvas1.get_tk_widget().grid(row=300,column=0)

plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)

data = b""
payload_size = struct.calcsize("Q")

Database = MasterDB.MasterDB()


NoGraph = False


def show_graphs():
   
    global plot,canvas,canvas1,figure,figure1,win
    global TempValue,PressureValue,ULValue,URValue,UBValue,ListSize,TempLine
    global Videolabel,DataSetActive,AutoDetect,NoGraph
    
    if DataSetActive == False and NoGraph == False:
        while True:
           # print(Global.MemMap["UltraSensor1"]["Distance"])
            print(Global.MemMap["UltraSensor2"]["Distance"])
            #print( Global.MemMap["UltraSensor3"]["Distance"])
            TempValue.append(Global.MemMap["TempSensor"]["TempC"])
            PressureValue.append(Global.MemMap["DepthSensor"]["Depth"])
            ULValue.append(Global.MemMap["UltraSensor1"]["Distance"])
            URValue.append(Global.MemMap["UltraSensor2"]["Distance"])
            UBValue.append(Global.MemMap["UltraSensor3"]["Distance"])

            if len(TempValue) > ListSize:
                TempValue.pop(0)
                PressureValue.pop(0)
                ULValue.pop(0)
                URValue.pop(0)
                UBValue.pop(0)
    
                TempPlot.clear()
                TempPlot.set_xlabel("time [s]")
                TempPlot.set_ylabel("Temperature [C]")
                TempPlot.set_title("Temperature", fontweight='bold')
                TempPlot.set_facecolor('orange')
        
                #PressurePlot.clear()
                #PressurePlot.set_xlabel("time[s]")
                #PressurePlot.set_ylabel("Pressure [kPa]")
                #PressurePlot.set_title("Pressure", fontweight='bold')
                #PressurePlot.set_facecolor('orange')

                #USLeft.clear()
                #USRight.set_xlabel("time [s]")
                #USRight.set_ylabel("Distance [mm]")
                #USRight.set_title("Right Ultrasonic", fontweight='bold')
                #USRight.set_facecolor('orange')

                #USRight.clear()
                #USRight.set_xlabel("time [s]")
                #USRight.set_ylabel("Distance [mm]")
                #USRight.set_title("Right Ultrasonic", fontweight='bold')
                #USRight.set_facecolor('orange')

                #USBottom.clear()
                #USRight.set_xlabel("time [s]")
                #USRight.set_ylabel("Distance [mm]")
                #USRight.set_title("Right Ultrasonic", fontweight='bold')
                #USRight.set_facecolor('orange')

            TempPlot.plot(TempValue,color="black",marker="x",linestyle="-")
            #PressurePlot.plot(PressureValue,color="black",marker="",linestyle="-")
            #USLeft.plot(ULValue,color="black",marker="",linestyle="-")
            #USRight.plot(URValue,color="black",marker="",linestyle="-")
            #USBottom.plot(UBValue,color="black",marker="",linestyle="-")

            canvas.draw()
            #canvas1.draw()
            sleep(1)
   


def show_frames():

    #global data
    global client_socket, win, Videolabel, data, payload_size, DbTimer
    global Database, DataTimeGap, DataSetActive,DataCaptureTime
    
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

    #cv2.imshow("RECEIVING VIDEO",frame)s

    # Get the latest frame and convert into Image
   
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #model = model_cascade.detectMultiScale(gray, 1.1, 1)

    #for (x, y, w, h) in model:
    #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
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