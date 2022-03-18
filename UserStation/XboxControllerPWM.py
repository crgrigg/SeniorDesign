import XInput as X
from time import sleep
import Global

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
                        d["Buttons"]["A"] = event.button
                        print(d["Buttons"]["A"])
                        #print(event.button)
                    elif event.button == 'B':
                        d["Buttons"]["B"] = event.button
                        print(d["Buttons"]["B"])
                        #print(event.button)
                    elif event.button == 'X':
                        d["Buttons"]["X"] = event.button
                        print(d["Buttons"]["X"])
                        #print(event.button)
                    elif event.button == 'Y':
                        d["Buttons"]["Y"] = event.button
                        print(d["Buttons"]["Y"])
                        #print(event.button)
                    elif event.button == 'DPAD_UP':
                        d["D_Pad"]["Up"] = event.button
                        print(d["D_Pad"]["Up"])
                        #print(event.button)
                    elif event.button == 'DPAD_DOWN':
                        d["D_Pad"]["Down"] = event.button
                        print(d["D_Pad"]["Down"])
                        #print(event.button)
                    elif event.button == 'DPAD_LEFT':
                        d["D_Pad"]["Left"] = event.button
                        print(d["D_Pad"]["Left"])
                        #print(event.button)
                    elif event.button == 'DPAD_RIGHT':
                        d["D_Pad"]["Right"] = event.button
                        print(d["D_Pad"]["Right"])
                        #print(event.button)
                    elif event.button == 'START':
                        print(event.button)
                    elif event.button == 'BACK':
                        print(event.button)
                    elif event.button == 'LEFT_THUMB':
                        print(event.button)
                    elif event.button == 'RIGHT_THUMB':
                        print(event.button)
                    elif event.button == 'LEFT_SHOULDER':
                        d["Bumper"]["Left"] = event.button
                        print(d["Bumper"]["Left"])
                        #print(event.button)
                    elif event.button == 'RIGHT_SHOULDER':
                        d["Bumper"]["Right"] = event.button
                        print(d["Bumper"]["Right"])
                        #print(event.button)

                elif event.type == X.EVENT_BUTTON_RELEASED:
                    if event.button == 'A':
                        d["Buttons"]["A"] = event.button
                        print(d["Buttons"]["A"])
                        #print(event.button)
                    elif event.button == 'B':
                        d["Buttons"]["B"] = event.button
                        print(d["Buttons"]["B"])
                        #print(event.button)
                    elif event.button == 'X':
                        d["Buttons"]["X"] = event.button
                        print(d["Buttons"]["X"])
                        #print(event.button)
                    elif event.button == 'Y':
                        d["Buttons"]["Y"] = event.button
                        print(d["Buttons"]["Y"])
                        #print(event.button)
                    elif event.button == 'DPAD_UP':
                        d["D_Pad"]["Up"] = event.button
                        print(d["D_Pad"]["Up"])
                        #print(event.button)
                    elif event.button == 'DPAD_DOWN':
                        d["D_Pad"]["Down"] = event.button
                        print(d["D_Pad"]["Down"])
                        #print(event.button)
                    elif event.button == 'DPAD_LEFT':
                        d["D_Pad"]["Left"] = event.button
                        print(d["D_Pad"]["Left"])
                        #print(event.button)
                    elif event.button == 'DPAD_RIGHT':
                        d["D_Pad"]["Right"] = event.button
                        print(d["D_Pad"]["Right"])
                        #print(event.button)
                    elif event.button == 'START':
                        print(event.button)
                    elif event.button == 'BACK':
                        print(event.button)
                    elif event.button == 'LEFT_THUMB':
                        print(event.button)
                    elif event.button == 'RIGHT_THUMB':
                        print(event.button)
                    elif event.button == 'LEFT_SHOULDER':
                        d["Bumper"]["Left"] = event.button
                        print(d["Bumper"]["Left"])
                        #print(event.button)
                    elif event.button == 'RIGHT_SHOULDER':
                        d["Bumper"]["Right"] = event.button
                        print(d["Bumper"]["Right"])
                        #print(event.button)

                elif event.type == X.EVENT_TRIGGER_MOVED:
                    if event.trigger == X.LEFT:
                        print(event.trigger)
                        print(event.value)
                    elif event.trigger == X.RIGHT:
                        print(event.trigger)
                        print(event.value)
                elif event.type == X.EVENT_STICK_MOVED:
                    if event.stick == X.LEFT:
                        d["Stick"]["Left"]["ValueX"] = 5
                        d["Stick"]["Left"]["ValueY"] = 4
                        print(event.x)
                        print(event.y)
                        print(event.value)
                        print(event.dir)
                    elif event.stick == X.RIGHT:
                        Global.ControllerMap["Stick"]["Right"]["ValueX"] = 3
                        Global.ControllerMap["Stick"]["Right"]["ValueY"] = 2
                        print(Global.ControllerMap["Stick"]["Right"]["ValueX"])
                        print(Global.ControllerMap["Stick"]["Right"]["ValueY"])
                        print(event.value)
                        print(event.dir)