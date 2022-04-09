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


x = [0.1,0.2,0.3]
y = [-0.1,-0.2,-0.3]
Xvalue = 0.4
Yvalue = -0.4


root = Tk()
root.geometry("1080x1080")


figure = plt.figure(figsize=(4.5,6),dpi=100)
TempPlot = figure.add_subplot(2,1,1)
TempPlot.set_xlabel("Hello")
TempPlot.set_ylabel("Y")
TempPlot.set_title("Temperature[C]")
PressurePlot = figure.add_subplot(2,1,2)
PressurePlot.set_xlabel("Hello")
PressurePlot.set_ylabel("Y")
PressurePlot.set_title("Pressure[Pascals]")
canvas = FigureCanvasTkAgg(figure,root)
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
canvas1 = FigureCanvasTkAgg(figure1,root)
canvas1.get_tk_widget().grid(row=300,column=0)

plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.5,hspace=0.4)





def plottingPoints():
     
    global plot,canvas,x,y,figure,Xvalue,Yvalue
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

MyThread = threading.Thread(target=plottingPoints)
MyThread.start()




root.mainloop()