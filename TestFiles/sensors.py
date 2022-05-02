import RPi.GPIO as GPIO
from time import sleep
import sys
import serial
import glob
import spidev
import Global
from gpiozero import  CPUTemperature

def read_sensors():

    dictionary = Global.MemMap
    cpu = CPUTemperature()
    ###################
    ### TEMPERATURE ###
    ###################
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            dictionary["TempSensor"]["TempC"] = temp_c
            dictionary["TempSensor"]["TempF"] = temp_f
            #return temp_c, temp_f
        
    # while True:
    #     sensorReadings = read_temp()
    #     print(sensorReadings)
    #     time.sleep(1)
        
    ################
    ### PRESSURE ###
    ################
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 250000

    def poll_sensor(channel):
        assert 0 <= channel <= 1
        
        if channel:
            cbyte = 0b11000000
        else:
            cbyte = 0b10000000
            
        r = spi.xfer2([1,cbyte,0])
        
        dictionary["DepthSensor"]["Depth"] = ((r[1] & 31) << 6) + (r[2] >> 2)
        #return ((r[1] & 31) << 6) + (r[2] >> 2)

    
    # try:
    #     while True:
    #         channel = 0
    #         channeldata = poll_sensor(channel)
    #         
    #         voltage = round(((channeldata * 3300) / 1024),0)
    #         
    #         #channeldata = (voltage - 81) * 4
    #         print('Voltage (mV): {}'.format(voltage))
    #         print('Data        : {}\n'.format(channeldata))
    #         
    #         sleep(2)
    #         
    # finally:
    #     spi.close()
    #     print ("\n All cleaned up.")

    ##################
    ### ULTRASONIC ###
    ##################
    UltraFrameSize = 4
    UltraHeader = b'\xFF'

    select0 = 23
    select1 = 24
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(select0, GPIO.OUT)
    GPIO.setup(select1, GPIO.OUT)

    ser = serial.Serial(port='/dev/serial0')
    ser.baudrate = 9600
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    ser.timeout = 1

    s0 = 0
    s1 = 0
    label = "UltraSensor1"
    # while True:
    #     GPIO.output(select0, s0)
    #     GPIO.output(select1, s1)
    #     value = ser.read(4)
    #     print(label, int.from_bytes(value[1:3],"big"))
    #     
    #     if label == "Bottom":
    #         sleep(3)
    #     
    #     ser.flushInput()
    #     
    #     if s0 == 0 and s1 == 0:
    #         s1 = 1
    #         label = "Right"
    #     elif s0 == 0 and s1 == 1:
    #         s0 = 1
    #         s1 = 0
    #         label = "Bottom"
    #     elif s0 == 1 and s1 == 0:
    #         s0 = 0
    #         label = "Left"
            
    while True:

	##############
	# CPU Temp   #
	##############
        dictionary["CPU"]["Temp"] = cpu.temperature
        ###############
        # temperature #
        ###############
        read_temp()
        #print(sensorReadings)
        #sleep(1)
        
        ############
        # pressure #
        ############
        channel = 0
        channeldata = poll_sensor(channel)
            
        #voltage = round(((channeldata * 3300) / 1024),0)
            
        #channeldata = (voltage - 81) * 4
        #print('Voltage (mV): {}'.format(voltage))
        #print('Data        : {}\n'.format(channeldata))
            
        #sleep(2)
        
        ##############
        # ultrasonic #
        ##############
        GPIO.output(select0, s0)
        GPIO.output(select1, s1)
        value = ser.read(4)
        dictionary[label]["Distance"] = int.from_bytes(value[1:3],"big")
        #print(label, int.from_bytes(value[1:3],"big"))
        
#         if label == "UltraSensor3":
#             sleep(3)
        
        ser.flushInput()
        
        if s0 == 0 and s1 == 0:
            s1 = 1
            label = "UltraSensor2"
        elif s0 == 0 and s1 == 1:
            s0 = 1
            s1 = 0
            label = "UltraSensor3"
        elif s0 == 1 and s1 == 0:
            s0 = 0
            label = "UltraSensor1"
