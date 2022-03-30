import XInput as X
import time


def get_signals():
    while X.get_connected()[0] == True:
        ControllerEvents = X.get_events()
        for event in ControllerEvents:
            if event.user_index == 0:
                if event.type == X.EVENT_CONNECTED:
                    continue
                elif event.type == X.EVENT_BUTTON_PRESSED:
                     if event.button == 'A':
                        print(event.button)
                elif event.button == 'B':
                    print(event.button)
                elif event.button == 'X':
                    print(event.button)
                elif event.button == 'Y':
                    print(event.button)
                elif event.button == 'DPAD_UP':
                    print(event.button)
                elif event.button == 'DPAD_DOWN':
                    print(event.button)
                elif event.button == 'DPAD_LEFT':
                    print(event.button)
                elif event.button == 'DPAD_RIGHT':
                    print(event.button)
                elif event.button == 'START':
                    print(event.button)
                elif event.button == 'BACK':
                    print(event.button)
                elif event.button == 'LEFT_THUMB':
                    print(event.button)
                elif event.button == 'RIGHT_THUMB':
                    print(event.button)
                elif event.button == 'LEFT_SHOULDER':
                    print(event.button)
                elif event.button == 'RIGHT_SHOULDER':
                    print(event.button)
            elif event.type == X.EVENT_BUTTON_RELEASED:
                if event.button == 'A':
                    print(event.button)
                elif event.button == 'B':
                    print(event.button)
                elif event.button == 'X':
                    print(event.button)
                elif event.button == 'Y':
                    print(event.button)
                elif event.button == 'DPAD_UP':
                    print(event.button)
                elif event.button == 'DPAD_DOWN':
                    print(event.button)
                elif event.button == 'DPAD_LEFT':
                    print(event.button)
                elif event.button == 'DPAD_RIGHT':
                    print(event.button)
                elif event.button == 'START':
                    print(event.button)
                elif event.button == 'BACK':
                    print(event.button)
                elif event.button == 'LEFT_THUMB':
                    print(event.button)
                elif event.button == 'RIGHT_THUMB':
                    print(event.button)
                elif event.button == 'LEFT_SHOULDER':
                    print(event.button)
                elif event.button == 'RIGHT_SHOULDER':
                    print(event.button)

            elif event.type == X.EVENT_TRIGGER_MOVED:
                if event.trigger == X.LEFT:
                    print(event.trigger)
                    print(event.value)
                elif event.trigger == X.RIGHT:
                    print(event.trigger)
                    print(event.value)
            elif event.type == X.EVENT_STICK_MOVED:
                if event.stick == X.LEFT:
                    print(event.x)
                    print(event.y)
                    print(event.value)
                    print(event.dir)
                elif event.stick == X.RIGHT:
                    print(event.x)
                    print(event.y)
                    print(event.value)
                    print(event.dir)
        sleep(2)
        data = pickle.dumps(Global.ControllerMap)
        print(data)
        client_socket.sendall(data)


get_signals()

   