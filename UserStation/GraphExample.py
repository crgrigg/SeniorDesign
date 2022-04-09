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
from time import sleep
import XboxControllerPWM





root = Tk()

figure = Figure(figsize=(5,4),dpi=100)
plot = figure.add_subplot(1,1,1)
plot.plot(0.5,0.3,color="red",marker="o",linestyle="")
canvas = FigureCanvasTkAgg(figure,root)
canvas.get_tk_widget().grid(row=0,column=0)
x = [0.1,0.2,0.3]
y = [-0.1,-0.2,-0.3]
Xvalue = 0.4
Yvalue = -0.4

def plottingPoints():
    
    global plot,canvas,x,y,figure,Xvalue,Yvalue
    while True:
        x.append(Xvalue)
        y.append(Yvalue)
        plot.plot(x,y,color="blue",marker="x",linestyle="")
        Xvalue += 0.1
        Yvalue -= 0.1
        sleep(2)
        canvas.draw()
        

MyThread = threading.Thread(target=plottingPoints)
MyThread.start()




root.mainloop()