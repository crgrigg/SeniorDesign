# lets make the client code
import cv2, socket, pickle, struct
from tkinter import *
import tkinter
from PIL import Image, ImageTk
import threading
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import MotorClient
import MasterDB
import time
import XboxControllerPWM
from time import sleep

MotorThread = threading.Thread(target = MotorClient.motor_client)
MotorThread.start()

ControllerThread = threading.Thread(target = XboxControllerPWM.get_signals)
ControllerThread.start()

  
Database = MasterDB.MasterDB()
DbTimeGap = .4 #How often to update Database Data
DbTimer = time.time()



client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.253.85'
port = 9997
client_socket.connect((host_ip,port)) # a tuple


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
PressurePlot = figure.add_subplot(2,1,2)
PressurePlot.set_xlabel("time[s]")
PressurePlot.set_ylabel("Pressure [kPa]")
PressurePlot.set_title("Pressure", fontweight='bold')
PressurePlot.set_facecolor('orange')
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

x = [0.1,0.2,0.3]
y = [-0.1,-0.2,-0.3]
Xvalue = 0.4
Yvalue = -0.4

def show_graphs():
    
    global plot,canvas,canvas1,canvas2,x,y,figure,figure1,figure2,Xvalue,Yvalue
    global Database
    while True:
        x.append(Xvalue)
        y.append(Yvalue)

       
        TempPlot.plot(Database.TempValue,Database.TimeValue,color="black",marker="x",linestyle="-")
        PressurePlot.plot(Database.PressureValue,Database.TimeValue,color="black",marker="x",linestyle="-")
        USLeft.plot(Database.ULValue,Database.TimeValue,color="black",marker="x",linestyle="-")
        USRight.plot(Database.URValue,Database.TimeValue,color="black",marker="x",linestyle="-")
        USBottom.plot(Database.UBValue,Database.TimeValue,color="black",marker="x",linestyle="-")

        Xvalue += 0.1
        Yvalue -= 0.1
        canvas.draw()
        canvas1.draw()
        sleep(1)
     

DbTimer = time.time()

def show_frames():

    #global data
    global client_socket, win, Videolabel, data, payload_size, DbTimer
    global Database
    Database = MasterDB.MasterDB()
    DbTimeGap = .4 #How often to update Database Data
    #DbTimer = time.time()
     
 
    if (time.time() - DbTimer) > DbTimeGap:
        #Database.WriteIO()
        DbTimer = time.time()
         
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
    cv2image= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    Videolabel.imgtk = imgtk
    Videolabel.configure(image=imgtk)
    
        
    # Repeat after an interval to capture continiously
    Videolabel.after(1, show_frames)

ActiveThread = threading.Thread(target = show_graphs)
ActiveThread.start()

#computer_visual()
show_frames()
win.mainloop()