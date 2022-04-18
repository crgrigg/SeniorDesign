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



 # Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("1080x1080")
win.attributes("-topmost", True)
win.title("Underwater ROV")
win.configure(background='orange')

# Create a Label to capture the Video frames
Videolabel =Label(win)
Videolabel.grid(row=0, column=0,rowspan = 10,columnspan=10)

ROVStatusRow = 11
ROVStatusCol = 0
RowIndex = 2
ColumnSpace = 4
SensorRow = 0
SensorCol = ROVStatusCol + ColumnSpace +100
SensorColSpace = 4

ROVStatus = Label(win,bg = "orange",font="bold")
ROVStatus.grid(row=ROVStatusRow,column = ROVStatusCol, columnspan=2)
ROVStatus.configure(text="UUV Status")

#Light Status
LightStatus = Label(win,bg="orange")
LightStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
LightStatus.configure(text ="Light Status")
LightStatusValue = Label(win,bg="orange")
LightStatusValue.grid(row=ROVStatusRow  + RowIndex,column=ROVStatusCol + ColumnSpace)
LightStatusValue.configure(text="")
RowIndex += 1

#Verticle Motor Status
VerticleMotorLock = Label(win,bg="orange")
VerticleMotorLock.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol)
VerticleMotorLock.configure(text ="Vertical Motor Lock")
VerticleMotorValue = Label(win,bg="orange")
VerticleMotorValue.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol  + ColumnSpace)
VerticleMotorValue.configure(text ="")
RowIndex += 1

#Left Motor Speed
LeftMotorSpeed = Label(win,bg="orange")
LeftMotorSpeed.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol)
LeftMotorSpeed.configure(text ="Left Motor Speed")
LeftMotorValue = Label(win,bg="orange")
LeftMotorValue.grid(row = ROVStatusRow  + RowIndex, column = ROVStatusCol  + ColumnSpace)
LeftMotorValue.configure(text ="")
RowIndex += 1

#Right Motor Speed
RightMotorSpeed = Label(win,bg="orange")
RightMotorSpeed.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
RightMotorSpeed.configure(text ="Right Motor Speed")
RightMotorValue = Label(win,bg="orange")
RightMotorValue.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol  + ColumnSpace)
RightMotorValue.configure(text ="")
RowIndex += 1

#Vertical Motor Speed
VerticleMotorLock = Label(win,bg="orange")
VerticleMotorLock.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
VerticleMotorLock.configure(text ="Vertical Motor Speed")
VerticleMotorValue = Label(win,bg="orange")
VerticleMotorValue.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol  + ColumnSpace)
VerticleMotorValue.configure(text ="")
RowIndex += 1

#Auto Mode
AutoModeStatus = Label(win,bg="orange")
AutoModeStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
AutoModeStatus.configure(text ="Auto Mode")
AutoModeValue = Label(win,bg="orange")
AutoModeValue.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol + ColumnSpace)
AutoModeValue.configure(text ="")
RowIndex += 1

#CPU Temperature
CPUTempStatus = Label(win,bg="orange")
CPUTempStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
CPUTempStatus.configure(text ="CPU Temp")
CPUTempValue = Label(win,bg="orange")
CPUTempValue.grid(row = ROVStatusRow + RowIndex , column = ROVStatusCol + ColumnSpace)
CPUTempValue.configure(text ="")
RowIndex += 1

#ROV Error Status
ROVErrorStatus = Label(win,bg="orange")
ROVErrorStatus.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol)
ROVErrorStatus.configure(text ="UUV Error Status")
ROVErrorValue = Label(win,bg="orange")
ROVErrorValue.grid(row = ROVStatusRow + RowIndex, column = ROVStatusCol + ColumnSpace )
ROVErrorValue.configure(text ="")
RowIndex += 1

#Sensor Data
RowIndex = 2
SensorData = Label(win,bg = "orange",font="bold")
SensorData.grid(row=SensorRow,column = SensorCol, columnspan=2)
SensorData.configure(text="SensorData")

# Temp Sensor
TempSensorStatus = Label(win,bg="orange")
TempSensorStatus.grid(row = SensorRow + RowIndex, column = SensorCol)
TempSensorStatus.configure(text ="Temperature [Ferenheit]")
TempSensorValue = Label(win,bg="orange")
TempSensorValue.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
TempSensorValue.configure(text ="")
RowIndex += 1

#Pressure
PressureSensorStatus = Label(win,bg="orange")
PressureSensorStatus.grid(row = SensorRow + RowIndex, column = SensorCol)
PressureSensorStatus.configure(text ="Pressure [Pa]")
PressureSensorValue = Label(win,bg="orange")
PressureSensorValue.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
PressureSensorValue.configure(text ="")
RowIndex += 1

#Ultrasonic Sensor 1
UltrasonicSensor1Status = Label(win,bg="orange")
UltrasonicSensor1Status.grid(row = SensorRow + RowIndex, column = SensorCol)
UltrasonicSensor1Status.configure(text ="Left Distance[mm]")
UltrasonicSensor1Value = Label(win,bg="orange")
UltrasonicSensor1Value.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
UltrasonicSensor1Value.configure(text ="")
RowIndex += 1

#Ultrasonic Sensor 2
UltrasonicSensor2Status = Label(win,bg="orange")
UltrasonicSensor2Status.grid(row = SensorRow + RowIndex, column = SensorCol)
UltrasonicSensor2Status.configure(text ="Right Distance [mm]")
UltrasonicSensor2Value = Label(win,bg="orange")
UltrasonicSensor2Value.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
UltrasonicSensor2Value.configure(text ="")
RowIndex += 1

#Ultrasonic Sensor 3
UltrasonicSensor3Status = Label(win,bg="orange")
UltrasonicSensor3Status.grid(row = SensorRow + RowIndex, column = SensorCol)
UltrasonicSensor3Status.configure(text ="Bottom Distance [mm]")
UltrasonicSensor3Value = Label(win,bg="orange")
UltrasonicSensor3Value.grid(row = SensorRow + RowIndex, column = SensorCol + SensorColSpace )
UltrasonicSensor3Value.configure(text ="")
RowIndex += 1

def Update_Data():

    #ROV Status
    LeftMotorValue.configure(text ="")
    RightMotorValue.configure(text ="")
    VerticleMotorValue.configure(text ="")
    AutoModeValue.configure(text ="")
    CPUTempValue.configure(text ="")
    ROVErrorValue.configure("")

    #SensorData
    TempSensorValue.configure(text ="")
    PressureSensorValue.configure(text ="")
    UltrasonicSensor1Value.configure(text ="")
    UltrasonicSensor2Value.configure(text ="")
    UltrasonicSensor3Value.configure(text ="")



win.mainloop()