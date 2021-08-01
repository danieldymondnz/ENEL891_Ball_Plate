

from time import time
from timeit import default_timer as timer


from UART_Servo_Controller import UART_Servo_Controller

controller = UART_Servo_Controller('COM3')

InProgress = False

# Initial Values for angles
S_angleX = 90  # initial angle of servos
S_angleY = 90  # initial angle of servos



lineList = [0, 2.5, 5, 2.5, 0]

fps = 0.03
twoframes = 2*fps

testime = 1

controller.sendXServo(90)
controller.sendYServo(90)

Left = True
Right = False
count = 0
start = timer()
while (InProgress):

    end = timer()

    setdelay = end - start

    if setdelay > testime:
        print("SetDelay: {}".format(setdelay))
        if (Left):
            
            ServoX = lineList[count]
            S_angleX = 90 - ServoX
                #controller.sendXServo(ServoX)
            count += 1
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("Count: {}".format(count))

            start = timer()

            if count > 4:
                count = 0
                Left = False
                Right = True

        if (Right):

            ServoX = lineList[count]
            S_angleX = 90 + ServoX
                #controller.sendXServo(ServoX)
            count += 1
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("Count: {}".format(count))

            start = timer()

            if count > 4:
                count = 0
                Left = True
                Right = False



