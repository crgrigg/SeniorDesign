# lets make the client code
import cv2, socket, pickle, struct
from tkinter import *
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




client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.253.85'
port = 9997
client_socket.connect((host_ip,port)) # a tuple

Database = MasterDB.MasterDB()
DbTimeGap = .4 #How often to update Database Data
DbTimer = time.time()

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("1080x720")


VideoLabelRow = 0
VideoLabelCol = 0


# Create a Label to capture the Video frames
Videolabel =Label(win)
Videolabel.grid(row=VideoLabelRow, column=VideoLabelCol)

#Graphs
figure = plt.figure(figsize=(4,6),dpi=100)
TempPlot = figure.add_subplot(2,1,1)
TempPlot.set_xlabel("Hello")
TempPlot.set_ylabel("Y")
TempPlot.set_title("Temperature[C]")
PressurePlot = figure.add_subplot(2,1,2)
PressurePlot.set_xlabel("Hello")
PressurePlot.set_ylabel("Y")
PressurePlot.set_title("Pressure[Pascals]")
canvas = FigureCanvasTkAgg(figure,win)
canvas.get_tk_widget().grid(row=0,column=0)

figure1 = plt.figure(figsize=(12,3),dpi=100)
USLeft = figure1.add_subplot(1,3,1)
USLeft.set_xlabel("Hello")
USLeft.set_ylabel("Y")
USLeft.set_title("Temperature[C]")
USRight = figure1.add_subplot(1,3,2)
USRight.set_xlabel("Hello")
USRight.set_ylabel("Y")
USRight.set_title("Temperature[C]")
USBottom = figure1.add_subplot(1,3,3)
USBottom.set_xlabel("Hello")
USBottom.set_ylabel("Y")
USBottom.set_title("Temperature[C]")
canvas1 = FigureCanvasTkAgg(figure1,win)
canvas1.get_tk_widget().grid(row=300,column=0)

plt.subplots_adjust(left=0.2,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)


data = b""
payload_size = struct.calcsize("Q")

x = [0.1,0.2,0.3]
y = [-0.1,-0.2,-0.3]
Xvalue = 0.4
Yvalue = -0.4

def show_graphs():
    
    global plot,canvas,canvas1,canvas2,x,y,figure,figure1,figure2,Xvalue,Yvalue
    while True:
        x.append(Xvalue)
        y.append(Yvalue)

        TempPlot.plot(x,y,color="blue",marker="x",linestyle="")
        PressurePlot.plot(x,y,color="blue",marker="x",linestyle="")
        USLeft.plot(x,y,color="blue",marker="x",linestyle="")
        USRight.plot(x,y,color="blue",marker="x",linestyle="")
        USBottom.plot(x,y,color="blue",marker="x",linestyle="")

        Xvalue += 0.1
        Yvalue -= 0.1
        canvas.draw()
        canvas1.draw()
        sleep(1)
     



def show_frames():

    #global data
    global client_socket, win, Videolabel, data, payload_size
  
     
 
        #if (time.time() - DbTimer) > DbTimeGap:
         #   Database.WriteIO()
          #  SensorData = Database.ReadIORange()
         
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