import RPi.GPIO as GPIO
from time import sleep

motorPin = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorPin, GPIO.OUT)
pi_pwm = GPIO.PWM(motorPin, 200)
#pi_pwm.ChangeDutyCycle(20)
pi_pwm.start(0)
pi_pwm.ChangeDutyCycle(40)
sleep(3)

pi_pwm.ChangeDutyCycle(0)
sleep(3)

pi_pwm.ChangeDutyCycle(20)
sleep(3)

while True:
    i = 0
    while i<50:
        print(i)
        
        pi_pwm.ChangeDutyCycle(i)
        sleep(0.05)
        i += 0.02
    #for duty in range(0, 101, 1):
     #   pi_pwm.ChangeDutyCycle(duty)
      #  sleep(0.01)
    #sleep(0.5)
    
    #pi_pwm.ChangeDutyCycle(10)
    #sleep(2)
    #pi_pwm.ChangeDutyCycle(75)
    
    #for duty in range(100, -1, -1):
     #   pi_pwm.ChangeDutyCycle(duty)
      #  sleep(0.01)
    #sleep(0.5)