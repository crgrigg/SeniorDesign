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
                         #Lights State Machine
                        if Global.LightState == 0: Global.LightState = 1
                        elif Global.LightState == 2: Global.LightState = 3

                       
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
                        if Global.AutoState == 0: Global.AutoState = 1
                        elif  Global.AutoState == 2: Global.AutoState = 3
             
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
                        if Global.VertState == 0: Global.VertState = 1
                        elif Global.VertState == 2: Global.VertState = 3
                        
                elif event.type == X.EVENT_BUTTON_RELEASED:
                    if event.button == 'A':
                        d["Buttons"]["A"] = 0
                        if Global.LightState == 1: Global.LightState = 2
                        elif Global.LightState == 3: Global.LightState = 0
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
                        if Global.AutoState == 3: 
                            Global.AutoState = 0
                            Global.ControllerMap["Stick"]["Left"]["ValueY"] = 0
                            Global.ControllerMap["Trigger"]["Right"] = 0
                            Global.ControllerMap["Trigger"]["Left"] = 0
                        elif  Global.AutoState == 1: Global.AutoState = 2
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
                        if Global.VertState == 1: Global.VertState = 2
                        elif Global.VertState == 3: Global.VertState = 0
                        print(d["Bumper"]["Right"])
                       
                     

                elif event.type == X.EVENT_TRIGGER_MOVED:
                    if event.trigger == X.LEFT and Global.AutoMode == False:
                        Global.ControllerMap["Trigger"]["Left"] = event.value
                        #print(event.trigger)
                        #print(event.value)
                    elif event.trigger == X.RIGHT and Global.AutoMode == False:
                        Global.ControllerMap["Trigger"]["Right"] = event.value
                        #print(event.trigger)
                        #print(event.value)
                elif event.type == X.EVENT_STICK_MOVED:
                    if event.stick == X.LEFT and Global.AutoMode == False:
                        d["Stick"]["Left"]["ValueX"] = event.x
                        d["Stick"]["Left"]["ValueY"] = event.y
                        #print(event.x)
                        #print(event.y)
                        #print(event.value)
                        #print(event.dir)
                    elif event.stick == X.RIGHT:
                        #constant = Global.ControllerMap["Stick"]["Right"]["ValueY"]
                        if Global.AutoState == 0 or Global.AutoState == 3:
                            constant = Global.ControllerMap["Stick"]["Right"]["ValueY"]
                            Global.ControllerMap["Stick"]["Right"]["ValueY"] = event.y
                        else: Global.ControllerMap["Stick"]["Right"]["ValueY"] = constant

                        #vert = 0
                        #if Global.MemMap["Vertical Motor"]["Lock"] == "Unlocked":
                        #    vert = Global.ControllerMap["Stick"]["Right"]["ValueY"]

                        #if Global.MemMap["Vertical Motor"]["Lock"] == "Locked":
                        #    Global.ControllerMap["Stick"]["Right"]["ValueY"] = vert
                        #else:
                        #    Global.ControllerMap["Stick"]["Right"]["ValueY"] = event.y


                        Global.ControllerMap["Stick"]["Right"]["ValueX"] = event.x
                        print(Global.ControllerMap["Stick"]["Right"]["ValueX"])
                        print(Global.ControllerMap["Stick"]["Right"]["ValueY"])
                        print(event.value)
                        print(event.dir)
   