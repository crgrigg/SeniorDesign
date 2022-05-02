import RPi.GPIO as GPIO
from time import sleep
import sys
import serial
import os

UltraFrameSize = 4
UltraHeader = b'\xFF'

select0 = 23
select1 = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(select0, GPIO.OUT)
GPIO.setup(select1, GPIO.OUT)

# GPIO.output(select0, 1)
# GPIO.output(select1, 0)

ser = serial.Serial(port='/dev/serial0')
ser.baudrate = 9600
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 1

s0 = 0
s1 = 0
label = "Left"
while True:
    GPIO.output(select0, s0)
    GPIO.output(select1, s1)
    value = ser.read(4)
    #print(value)
    print(label, int.from_bytes(value[1:3],"big"))
    
    if label == "Bottom":
        sleep(3)
    
    ser.flushInput()
    
    if s0 == 0 and s1 == 0:
        s1 = 1
        label = "Right"
    elif s0 == 0 and s1 == 1:
        s0 = 1
        s1 = 0
        label = "Bottom"
    elif s0 == 1 and s1 == 0:
        s0 = 0
        label = "Left"