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

figure = Figure(figsize=(3,4),dpi=100)
plot = figure.add_subplot(1,1,1)
plot.plot(0.5,0.3,color="red",marker="o",linestyle="")
canvas = FigureCanvasTkAgg(figure,root)
canvas.get_tk_widget().grid(row=0,column=200)

figure1 = Figure(figsize=(3,4),dpi=100)
plot1 = figure1.add_subplot(1,1,1)
plot1.plot(0.5,0.3,color="red",marker="o",linestyle="")
canvas1 = FigureCanvasTkAgg(figure1,root)
canvas1.get_tk_widget().grid(row=200,column=200)

figure2 = Figure(figsize=(3,4),dpi=100)
plot2 = figure2.add_subplot(1,1,1)
plot2.plot(0.5,0.3,color="red",marker="o",linestyle="")
canvas2 = FigureCanvasTkAgg(figure1,root)
canvas2.get_tk_widget().grid(row=200,column=0)



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
        plot1.plot(x,y,color="blue",marker="x",linestyle="")
        plot2.plot(x,y,color="blue",marker="x",linestyle="")
        Xvalue += 0.1
        Yvalue -= 0.1
        sleep(2)
        canvas.draw()
        canvas1.draw()
        canvas2.draw()


        

MyThread = threading.Thread(target=plottingPoints)
MyThread.start()




root.mainloop()