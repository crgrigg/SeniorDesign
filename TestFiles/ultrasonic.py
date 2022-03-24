from time import sleep
import sys
import serial
import os

UltraFrameSize = 4
UltraHeader = b'\xFF'

ser = serial.Serial(port='/dev/serial0')
ser.baudrate = 9600
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 1

while True:
    value = ser.read(4)
    print(value)
    print(int.from_bytes(value[1:3],"big"))
    sleep(.5)