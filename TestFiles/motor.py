import RPi.GPIO as GPIO
from time import sleep
import socket, pickle
import ToMicro
import pigpio

pi = pigpio.pi()

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
#print('HOST IP:',host_ip)
port = 8000
socket_address = (("169.254.146.18", 8000))

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)


motorPinL = 18
motorPinR = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPinL, GPIO.OUT)
GPIO.setup(motorPinR, GPIO.OUT)

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

pi.set_servo_pulsewidth(motorPinL, 2000)
pi.set_servo_pulsewidth(motorPinR, 2000)
sleep(3)
pi.set_servo_pulsewidth(motorPinL, 1000)
pi.set_servo_pulsewidth(motorPinR, 1000)
sleep(3)

i = 1000
while i < 1500:
    print(i)
    pi.set_servo_pulsewidth(motorPinL, i)
    pi.set_servo_pulsewidth(motorPinR, i)
    i+=1
    
sleep(3)

client_socket,addr = server_socket.accept()
print('GOT CONNECTION FROM:',addr)

frequency = 0
while True:
    if client_socket:
        frequency = client_socket.recv(4096)
        dictionary = pickle.loads(frequency)
        speed = dictionary["Stick"]["Left"]["ValueY"]
        #turn = dictionary["Stick"]["Left"]["ValueX"]
        trigL = dictionary["Trigger"]["Left"]
        trigR = dictionary["Trigger"]["Right"]
        integer = ToMicro.conversion(speed)
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
        print("Left: ",intL)
        print("Right: ",intR)
        pi.set_servo_pulsewidth(motorPinL, intL)
        pi.set_servo_pulsewidth(motorPinR, intR)

server_socket.close()