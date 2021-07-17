## Rectangle Shape
# Servos move in rectanlge shape, no ball detection, servo control only

from time import time
from timeit import default_timer as timer

#from UART_Servo_Controller import UART_Servo_Controller

#controller = UART_Servo_Controller('COM4')

InProgress = True

# Initial Values for angles
S_angleX = 90  # initial angle of servos
S_angleY = 90  # initial angle of servos

patternList = [0, 2.5, 5, 2.5, 0]

fps = 0.03
twoframes = 2*fps

testime = 1

#controller.sendXServo(90)
#controller.sendYServo(90)

#pattern = ["Right", "Down", "Left", "Up"]

count = 0
patternCount = 1
start = timer()
while (InProgress):

    end = timer()

    setdelay = end - start

    if setdelay > testime:
        print("SetDelay: {}".format(setdelay))

        ## Right Pattern - X Servo down
        if (patternCount == 1):
            ServoX = patternList[count]
            S_angleX = 90 + ServoX
            #controller.sendXServo(S_angleX)
            count += 1
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("Count: {}".format(count))
            start = timer()
            if count > 4:
                count = 0
                patternCount += 1
                setdelay = testime * 0.5

        ## Down Pattern - Y Servo down
        if (patternCount == 2):
            ServoY = patternList[count]
            S_angleY = 90 + ServoY
            #controller.sendXServo(S_angleY)
            count += 1
            print("ServoY: {}".format(ServoY))
            print("S_angleY: {}".format(S_angleY))
            print("Count: {}".format(count))
            start = timer()
            if count > 4:
                count = 0
                patternCount += 1
                setdelay = testime
        
        ## Left Pattern - X Servo up
        if (patternCount == 3):
            ServoX = patternList[count]
            S_angleX = 90 - ServoX
            #controller.sendXServo(S_angleX)
            count += 1
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("Count: {}".format(count))
            start = timer()
            if count > 4:
                count = 0
                patternCount += 1
                setdelay = testime * 0.5

        ## Up Pattern - Y Servo up
        if (patternCount == 4):
            ServoY = patternList[count]
            S_angleY = 90 - ServoY
            #controller.sendYServo(S_angleY)
            count += 1
            print("ServoY: {}".format(ServoY))
            print("S_angleY: {}".format(S_angleY))
            print("Count: {}".format(count))
            start = timer()
            if count > 4:
                count = 0
                patternCount = 1
                setdelay = testime