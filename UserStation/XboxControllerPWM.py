import XInput as X
import socket
from time import sleep
import Global
import pickle
import MasterDB
d = Global.ControllerMap

def get_signals():
    global ControllerMap
    
    while X.get_connected()[0] == True:
        ControllerEvents = X.get_events()
        for event in ControllerEvents:
            if event.user_index == 0:
                if event.type == X.EVENT_CONNECTED:
                    continue

                elif event.type == X.EVENT_BUTTON_PRESSED:
                    if event.button == 'A':
                        d["Buttons"]["A"] = 1
                    elif event.button == 'B':
                        d["Buttons"]["B"] = 1
                    elif event.button == 'X':
                        d["Buttons"]["X"] = 1
                        Global.DataSetActive = True
                    elif event.button == 'Y':
                        d["Buttons"]["Y"] = 1
                    elif event.button == 'DPAD_UP':
                        d["D_Pad"]["Up"] = 1
                    elif event.button == 'DPAD_DOWN':
                        d["D_Pad"]["Down"] = 1
                    elif event.button == 'DPAD_LEFT':
                        d["D_Pad"]["Left"] = 1
                    elif event.button == 'DPAD_RIGHT':
                        d["D_Pad"]["Right"] = 1
                    elif event.button == 'START':
                        d["START"]["Value"] = 1
                    elif event.button == 'BACK':
                        print(event.button)
                    elif event.button == 'LEFT_THUMB':
                        print(event.button)
                    elif event.button == 'RIGHT_THUMB':
                        print(event.button)
                    elif event.button == 'LEFT_SHOULDER':
                        d["Bumper"]["Left"] = 1
                    elif event.button == 'RIGHT_SHOULDER':
                        d["Bumper"]["Right"] = 1
                        print(d["Bumper"]["Right"])
             
                elif event.type == X.EVENT_BUTTON_RELEASED:
                    if event.button == 'A':
                        d["Buttons"]["A"] = 0
                    elif event.button == 'B':
                        d["Buttons"]["B"] = 0
                    elif event.button == 'X':
                        d["Buttons"]["X"] = 0
                        Global.DataSetActive = False
                    elif event.button == 'Y':
                        d["Buttons"]["Y"] = 0
                    elif event.button == 'DPAD_UP':
                        d["D_Pad"]["Up"] = 0
                    elif event.button == 'DPAD_DOWN':
                        d["D_Pad"]["Down"] = 0
                    elif event.button == 'DPAD_LEFT':
                        d["D_Pad"]["Left"] = 0
                    elif event.button == 'DPAD_RIGHT':
                        d["D_Pad"]["Right"] = 0
                    elif event.button == 'START':
                        d["START"]["Value"] = 0
                    elif event.button == 'BACK':
                        print(event.button)
                    elif event.button == 'LEFT_THUMB':
                        print(event.button)
                    elif event.button == 'RIGHT_THUMB':
                        print(event.button)
                    elif event.button == 'LEFT_SHOULDER':
                        d["Bumper"]["Left"] = event.button
                        print(d["Bumper"]["Left"])
                    elif event.button == 'RIGHT_SHOULDER':
                        d["Bumper"]["Right"] = 0
                        print(d["Bumper"]["Right"])
                     

                elif event.type == X.EVENT_TRIGGER_MOVED:
                    if event.trigger == X.LEFT:
                        Global.ControllerMap["Trigger"]["Left"] = event.value
                        print(event.trigger)
                        print(event.value)
                    elif event.trigger == X.RIGHT:
                        Global.ControllerMap["Trigger"]["Right"] = event.value
                        print(event.trigger)
                        print(event.value)
                elif event.type == X.EVENT_STICK_MOVED:
                    if event.stick == X.LEFT:
                        d["Stick"]["Left"]["ValueX"] = event.x
                        d["Stick"]["Left"]["ValueY"] = event.y
                        print(event.x)
                        print(event.y)
                        print(event.value)
                        print(event.dir)
                    elif event.stick == X.RIGHT:
                        Global.ControllerMap["Stick"]["Right"]["ValueX"] = event.x
                        Global.ControllerMap["Stick"]["Right"]["ValueY"] = event.y
                        print(Global.ControllerMap["Stick"]["Right"]["ValueX"])
                        print(Global.ControllerMap["Stick"]["Right"]["ValueY"])
                        print(event.value)
                        print(event.dir)
   