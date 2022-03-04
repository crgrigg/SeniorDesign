#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import gpiozero

from xbox import Joystick

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

# Misc pin assingments
Buzzer = 8

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

#Motor pin initialization operation
def motor_init():
    global pwm_ENA
    global pwm_ENB
    global pwm_ENX
    global pwm_ENY
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

def servo_init():
    global pX
    global pY
    global runningAngleX
    global runningAngleY
    GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(9, GPIO.OUT, initial=GPIO.LOW)
    pX = GPIO.PWM(11, 50) # GPIO 9 for PWM with 50Hz
    pY = GPIO.PWM(9, 50)
    pX.start(50) # Initialization (3.75 = 0 deg, 2.5 = -90, 5 = 90)
    pY.start(50)

def peripheralInit():
    GPIO.setup(Buzzer, GPIO.OUT, initial=GPIO.HIGH)

#advance
def run(delaytime, LeftPWM, RightPWM):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(RightPWM)
    pwm_ENB.ChangeDutyCycle(LeftPWM)
    time.sleep(delaytime)

#back
def back(delaytime, LeftPWM, RightPWM):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(RightPWM)
    pwm_ENB.ChangeDutyCycle(LeftPWM)
    time.sleep(delaytime)

#turn left
def left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)

#turn right
def right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(delaytime)

#turn left in place
def spin_left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(60)
    pwm_ENB.ChangeDutyCycle(60)
    time.sleep(delaytime)

#turn right in place
def spin_right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(60)
    pwm_ENB.ChangeDutyCycle(60)
    time.sleep(delaytime)

#brake
def brake(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(60)
    pwm_ENB.ChangeDutyCycle(60)
    time.sleep(delaytime)

#camera servos
def Camera_LR(joyStickValue, delaytime):
    # Joystick value will be -1 to 1, needs to be scaled for 2.5 to 5 for servo angle
    #angle = (1.25 * (-joyStickValue)) + 3.75
    angle = (joyStickValue * 2.5) + 7.5
    GPIO.output(11, True)
    pX.ChangeDutyCycle(angle)
    time.sleep(delaytime)
    GPIO.output(11, False)
    pX.ChangeDutyCycle(0)
    time.sleep(delaytime)

def Camera_UD(joyStickValue, delaytime):
    # Joystick value will be -1 to 1, needs to be scaled for 2.5 to 5 for servo angle
    # Initialization (3.75 = 0 deg, 2.5 = -90, 5 = 90)
    #angle = (1.25 * (-joyStickValue)) + 3.75
    angle = (-joyStickValue * 2.5) + 7.5
    GPIO.output(9, True)
    pY.ChangeDutyCycle(angle)
    time.sleep(delaytime)
    GPIO.output(9, False)
    pY.ChangeDutyCycle(0)
    time.sleep(delaytime)

#whistle
def whistle():
    GPIO.output(Buzzer, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(Buzzer, GPIO.HIGH)
    time.sleep(0.001)	

#Delay 2s	try
time.sleep(2)

#The try/except statement is used to detect errors in the try block.
#the except statement catches the exception information and processes it.
#The robot car advance 1s，back 1s，turn left 2s，turn right 2s，turn left  in place 3s
#turn right  in place 3s，stop 1s。
"""
try:
    motor_init()
    while True:
        run(1)
        back(1)
        left(2)
        right(2)
        spin_left(3)
        spin_right(3)
        brake(1)
except KeyboardInterrupt:
    pass

pwm_ENA.stop()
pwm_ENB.stop()/home/pi/
"""