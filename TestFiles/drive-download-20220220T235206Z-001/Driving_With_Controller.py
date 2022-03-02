import xbox
import CarRun
import RPi.GPIO as GPIO
import time

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

# Instantiate the controller
joy = xbox.Joystick()

# Initialize the motor
CarRun.motor_init()
CarRun.servo_init()
CarRun.peripheralInit()

# Press back button to end driving session

while not joy.Back():
    # Getting PWM values for left and right side of ATV for steering
    if joy.leftX(0) == 0:
        LeftPWM = 60
        RightPWM = 60
    elif joy.leftX(0) < 0:
        LeftPWM = 60
        RightPWM = round(60 + ((joy.leftX(0) * 60)))
    elif joy.leftX(0) > 0:
        LeftPWM = round(60 - (joy.leftX(0) * 60))
        RightPWM = 60
    if joy.leftBumper() == 1:
        CarRun.spin_left(0.01)
    elif joy.rightBumper() == 1:
        CarRun.spin_right(0.01)
    elif joy.rightTrigger() > 0.75:
        CarRun.run(0.01, LeftPWM, RightPWM)
    elif joy.leftTrigger() > 0.75:
        CarRun.back(0.01, LeftPWM, RightPWM)
    else:
        CarRun.brake(0.01)

    joyx = round(joy.rightX(0), 2)
    joyy = round(joy.rightY(0), 2)
    #print('joyx ',joyx, 'joyy', joyy)
    CarRun.Camera_LR(joyx, 0.05)
    CarRun.Camera_UD(joyy, 0.05)

    
