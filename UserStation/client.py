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

#figure = Figure(figsize=(2,3),dpi=100)
##plot = figure.add_subplot(1,1,1)
#plot.plot(0.5,0.3,color="red",marker="o",linestyle="")
#canvas = FigureCanvasTkAgg(figure,win)
#canvas.get_tk_widget().grid(row=0,column=200)

#figure1 = Figure(figsize=(2,3),dpi=100)
#plot1 = figure1.add_subplot(1,1,1)
#plot1.plot(0.5,0.3,color="red",marker="o",linestyle="")
#canvas1 = FigureCanvasTkAgg(figure1,win)
#canvas1.get_tk_widget().grid(row=200,column=200)

#figure2 = Figure(figsize=(2,3),dpi=100)
#plot2 = figure2.add_subplot(1,1,1)
#plot2.plot(0.5,0.3,color="red",marker="o",linestyle="")
#canvas2 = FigureCanvasTkAgg(figure2,win)
#canvas2.get_tk_widget().grid(row=200,column=0)

data = b""
payload_size = struct.calcsize("Q")

""" def computer_visual():
	print("FUCKKKKKKKKKKKKKKKKKKKKKKKKKK")
	global win

    # create socket

    #while True:
	show_frames()
	win.mainloop() """

x = [0.1,0.2,0.3]
y = [-0.1,-0.2,-0.3]
Xvalue = 0.4
Yvalue = -0.4

def show_frames():

    #global data
    global client_socket, win, Videolabel, data, payload_size
    global Database,DbTimeGap,DbTimer
    global canvas,canvas1,canvas2
    global x,y
    global Xvalue,Yvalue
     
    while True:
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

#ActiveThread = threading.Thread(target = show_frames)
#ActiveThread.start()

#computer_visual()
show_frames()
win.mainloop()