import RPi.GPIO as GPIO
from time import sleep

motorPin = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorPin, GPIO.OUT)

pi_pwm = GPIO.PWM(motorPin, 4725)
pi_pwm.start(100) #need this line
pi_pwm.ChangeDutyCycle(50)
sleep(3)
#
pi_pwm.ChangeDutyCycle(0)
sleep(3)
#  
pi_pwm.ChangeDutyCycle(100)
sleep(3)

while True:
    i = 0
    while i<100:
        print(i)
        
        pi_pwm.ChangeDutyCycle(i)
        
        sleep(5)
        i += 7