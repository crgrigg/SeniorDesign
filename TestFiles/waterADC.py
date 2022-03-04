from time import sleep
import spidev

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
    
    return ((r[1] & 31) << 6) + (r[2] >> 2)

try:
    while True:
        channel = 0
        channeldata = poll_sensor(channel)
        
        voltage = round(((channeldata * 3300) / 1024),0)
        
        #channeldata = (voltage - 81) * 4
        print('Voltage (mV): {}'.format(voltage))
        print('Data        : {}\n'.format(channeldata))
        
        sleep(2)
        
finally:
    spi.close()
    print ("\n All cleaned up.")