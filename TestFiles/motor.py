import RPi.GPIO as GPIO
from time import sleep
import socket, pickle
import ToMicro
import pigpio
import os
import threading
import sensors, server
import Global

sent = Global.MemMap

# os.system("cd Desktop/SeniorDesign")
# os.system("./pigpio.sh")

senThread = threading.Thread(target=sensors.read_sensors)
senThread.start()

camThread = threading.Thread(target=server.read_camera)
camThread.start()

pi = pigpio.pi()

motorPinUP = 16
motorPinL = 27#13
motorPinR = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPinUP, GPIO.OUT)
GPIO.setup(motorPinL, GPIO.OUT)
GPIO.setup(motorPinR, GPIO.OUT)

lightPin = 17
GPIO.setup(lightPin, GPIO.OUT)

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
#print('HOST NAME: ',host_name, 'HOST IP: ',host_ip)
port = 8000
socket_address = (("0.0.0.0", 8000))

# Socket Bind
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# motorPinUP = 16
# motorPinL = 13
# motorPinR = 18
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(motorPinUP, GPIO.OUT)
# GPIO.setup(motorPinL, GPIO.OUT)
# GPIO.setup(motorPinR, GPIO.OUT)

# pi_pwm = GPIO.PWM(motorPin, 1000)
# sleep(3)
# 
# pi_pwm.start(50) 
# sleep(3)

# i = 1000
# while i > 667:
#         pi_pwm.ChangeFrequency(i)
#         print(i)
#         i-=1

# pi.set_servo_pulsewidth(motorPinUP, 2000)
# pi.set_servo_pulsewidth(motorPinL, 2000)
# pi.set_servo_pulsewidth(motorPinR, 2000)
# sleep(3)
# pi.set_servo_pulsewidth(motorPinUP, 1000)
# pi.set_servo_pulsewidth(motorPinL, 1000)
# pi.set_servo_pulsewidth(motorPinR, 1000)
# sleep(3)

i = 1000
while i < 1500:
    #print(i)
    pi.set_servo_pulsewidth(motorPinUP, i)
    pi.set_servo_pulsewidth(motorPinL, i)
    pi.set_servo_pulsewidth(motorPinR, i)
    i+=1
    
sleep(3)

client_socket,addr = server_socket.accept()
print('GOT CONNECTION FROM:',addr)

frequency = 0
constant = 0
state = 0
mode = 0
while True:
    if client_socket:
        frequency = client_socket.recv(8192)
        dictionary = pickle.loads(frequency)
        sending = pickle.dumps(sent)
        client_socket.sendall(sending)
        
        speed = dictionary["Stick"]["Left"]["ValueY"]
        up = dictionary["Stick"]["Right"]["ValueY"]
        #turn = dictionary["Stick"]["Left"]["ValueX"]
        trigL = dictionary["Trigger"]["Left"]
        trigR = dictionary["Trigger"]["Right"]
        cruise = dictionary["Bumper"]["Right"]
        lights = dictionary["Buttons"]["A"]
        integer = ToMicro.conversion(speed)
        depth = ToMicro.conversion(up)
        
        if integer > 1500:
            integer = integer - (2 * (integer - 1500))
        elif integer < 1500:
            integer = integer + (2 * (1500 - integer))
        
        intL = integer
        intR = integer
        if integer > 1500:
            intR = intR - (2 * (trigR  * (intR - 1500)))
            intL = intL - (2 * (trigL  * (intL - 1500)))
        if integer < 1500:
            intR = intR + (2 * (trigR  * (1500 - intR)))
            intL = intL + (2 * (trigL  * (1500 - intL)))
                
#         if integer > 1500:
#             if turn > 0:
#                 intR = intR - (turn * (intR - 1500))
#             if turn < 0:
#                 intL = intL - (abs(turn) * (intL - 1500))
#         if integer < 1500:
#             if turn > 0:
#                 intR = intR + (turn * (1500 - intR))
#             if turn < 0:
#                 intL = intL + (abs(turn) * (1500 - intL))
        
        # motors
        if state == 0 and cruise == 0:
            state = 0
        elif state == 0 and cruise == 1:
            state = 1
        elif state == 1 and cruise == 1:
            state = 1
        elif state == 1 and cruise == 0:
            state = 2
        elif state == 2 and cruise == 0:
            state = 2
        elif state == 2 and cruise == 1:
            state = 3
        elif state == 3 and cruise == 1:
            state = 3
        else:
            state = 0
        
        # lights
        if mode == 0 and lights == 0:
            mode = 0
        elif mode == 0 and lights == 1:
            mode = 1
        elif mode == 1 and lights == 1:
            mode = 1
        elif mode == 1 and lights == 0:
            mode = 2
        elif mode == 2 and lights == 0:
            mode = 2
        elif mode == 2 and lights == 1:
            mode = 3
        elif mode == 3 and lights == 1:
            mode = 3
        else:
            mode = 0
            
        if mode == 0 or mode == 3:
            GPIO.output(lightPin, 0)
        if mode == 1 or mode == 2:
            GPIO.output(lightPin, 1)
            
        if state == 0 or state == 3:
            constant = depth
            Global.MemMap["Vertical Motor"]["Lock"] = "Locked"
        else: Global.MemMap["Vertical Motor"]["Lock"] = "Unlocked"

            #print("Up: ",depth)
            #pi.set_servo_pulsewidth(motorPinUP, depth)
        #elif state == 1 pr state == 2:
            #print("Up: ",depth)
            #pi.set_servo_pulsewidth(motorPinUP, depth)
    
        #print("Up: ",constant)
        #print("Left: ",intL)
        #print("Right: ",intR)
            
        pi.set_servo_pulsewidth(motorPinUP, constant)
        pi.set_servo_pulsewidth(motorPinL, intL)
        pi.set_servo_pulsewidth(motorPinR, intR)

server_socket.close()
                                                                                            
