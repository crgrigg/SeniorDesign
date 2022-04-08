# lets make the client code
import cv2, socket, pickle, struct
from tkinter import *
from PIL import Image, ImageTk
import threading
import MotorClient

myThread = threading.Thread(target = MotorClient.motor_client)
myThread.start()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '169.254.253.85'
port = 9997
client_socket.connect((host_ip,port)) # a tuple

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("640x480")

# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=0, column=0)

data = b""
payload_size = struct.calcsize("Q")

""" def computer_visual():
	print("FUCKKKKKKKKKKKKKKKKKKKKKKKKKK")
	global win

    # create socket

    #while True:
	show_frames()
	win.mainloop() """

def show_frames():

    #global data
    global client_socket, win, label, data, payload_size

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

    #cv2.imshow("RECEIVING VIDEO",frame)

    # Get the latest frame and convert into Image
    cv2image= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    label.after(1, show_frames)

#computer_visual()
show_frames()
win.mainloop()