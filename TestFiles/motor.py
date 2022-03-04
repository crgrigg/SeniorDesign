import RPi.GPIO as GPIO
from time import sleep

motorPin = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorPin, GPIO.OUT)

#Test1
#----------------------------------
# pi_pwm = GPIO.PWM(motorPin, 16000)
# #pi_pwm.ChangeDutyCycle(20)
# pi_pwm.start(50) #was at 0
# #pi_pwm.ChangeDutyCycle(50)
# sleep(3)
# 
# pi_pwm.ChangeDutyCycle(100)
# sleep(3)
# 
# pi_pwm.ChangeDutyCycle(0)
# sleep(3)
# 
# while True:
#     i = 1
#     while i<100:
#         print(i)
#         
#         pi_pwm.ChangeDutyCycle(i)
#         
#         sleep(3)
#         i += 1
#         
#----------------------------------------------------------------

pi_pwm = GPIO.PWM(motorPin, 4725)
# #pi_pwm.ChangeDutyCycle(20)
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
        
#---------------------------------------
# pi_pwm = GPIO.PWM(motorPin, 4725)
# pi_pwm.ChangeFrequency(500000)
# sleep(3)
# pi_pwm.ChangeFrequency(1000000)
# sleep(3)
# 
# pi_pwm.ChangeFrequency(4725)
# # #pi_pwm.ChangeDutyCycle(20)
# pi_pwm.start(100) #need this line
# # pi_pwm.ChangeDutyCycle(50)
# # sleep(3)
# # 
# # pi_pwm.ChangeDutyCycle(100)
# # sleep(3)
# #  
# # pi_pwm.ChangeDutyCycle(0)
# # sleep(3)
# 
# while True:
#     i = 10
#     while i<100:
#         print(i)
#         
#         pi_pwm.ChangeDutyCycle(i)
#         
#         sleep(10)
#         i += 1