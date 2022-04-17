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
import Global
import random 


root = Tk()
root.geometry("1080x1080")

TempValue = [1,1,1]
i = 0

Database =  MasterDB.MasterDB()


figure = plt.figure(figsize=(4.5,6),dpi=100)
TempPlot = figure.add_subplot(2,1,1)

TempPlot.set_xlabel("Hello")
TempPlot.set_ylabel("Y")
TempPlot.set_title("Temperature[C]")
TempPlot.set_ylim(-5,40)
lines = TempPlot.plot([],[])[0]
canvas = FigureCanvasTkAgg(figure,master=root)
canvas.get_tk_widget().grid(row=0,column=0)

def plottingPoints(): 
    global canvas, TempPlot,TempValue,lines,i,figure
    TempPlot.plot(TempValue,color="black",marker="x",linestyle="-")      
    canvas.draw()
    
    print("I am running!")
    root.after(1000,plottingPoints)

def MakeData():
    global Database,TempValue,i
    Database.WriteIO()
    Value = Database.ReadIORange()
    print(len(Value.Temp.values.tolist()))
    #print(Value.Temp.values.tolist())
    TempValue.append()
    print(len(TempValue))
    i += 1
    root.after(20,MakeData)
MakeData()
plottingPoints()
root.mainloop()
