# Write your code here :-)

import time
import board
import pulseio
from adafruit_motor import servo
from analogio import AnalogOut
from analogio import AnalogIn

throwingAccelerationThreshold = 3.005

IDLE = 0
HAS_BEEN_THROWN = 1
WAITING_FOR_AUTO_LEVEL = 2
AUTO_LEVEL = 3

WAIT_TIME = 500

def updateSystem():
    currentAccel = readAccelerometer()
    timeCount +=1


def evaluateState(state):
    if(state == IDLE):
        if(currentAccel > throwingAccelerationThreshold):
            return HAS_BEEN_THROWN
    if(state == HAS_BEEN_THROWN):
        return WAITING_FOR_AUTO_LEVEL
    if(state == WAITING_FOR_AUTO_LEVEL):
        if(timeCount > WAIT_TIME):
            return AUTO_LEVEL
    return state



def reactToState(state):
    if(state == HAS_BEEN_THROWN):
        timeCount = 0
    if(state == AUTO_LEVEL):
        analog_in = AnalogIn(board.A4)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

# Initialize PWM output for the servo (on pin A2):
#pwm = pulseio.PWMOut(board.A2, frequency=50)
pwm = pulseio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm, min_pulse = 500, max_pulse = 2500)
# Create a servo object, my_servo.
#my_servo = servo.Servo(pwm)

def mathMap(input,minInput,maxInput,minOutput,maxOutput):
    return (input - minInput)*(maxOutput - minOutput)/(maxInput - minInput) + minOutput

setpoint = 1.67

UnknownConstant = 1

while True:

    AccelVolt = (get_voltage(analog_in))

    currentOutput = my_servo.angle
    #print(currentOutput)

    #error = setpoint - AccelVolt

    #output = error*UnknownConstant


    if(AccelVolt > setpoint):
        currentOutput += 0.5
    elif(AccelVolt < setpoint):
        currentOutput -= 0.5

    NewAngle =  currentOutput

    if(NewAngle > 180):
        NewAngle= 180
    elif(NewAngle < 0):
        NewAngle = 0


    #print((get_voltage(analog_in),))
    time.sleep(0.01)

    my_servo.angle = NewAngle



while(True):
    updateSystem()
    state = evaluateState(state)
    reactToState(state)
    time.sleep(0.02)

