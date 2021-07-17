



from time import time
from timeit import default_timer as timer

#from UART_Servo_Controller import UART_Servo_Controller

#controller = UART_Servo_Controller('COM4')

InProgress = True

# Initial Values for angles
S_angleX = 90  # initial angle of servos
S_angleY = 90  # initial angle of servos

fps = 0.03
twoframes = 2*fps

testime = 0.5

#controller.sendXServo(90)
#controller.sendYServo(90)

angle = [0, 1, 2, 3, 4, 5]

up = 0
down = 5
count = 1
start = timer()

while (InProgress):

    end = timer()

    setdelay = end - start

    if setdelay > testime:
        print("SetDelay: {}".format(setdelay))

        if (count == 1):
            ServoX = angle[up]
            ServoY = angle[down]
            S_angleX = 90 + ServoX
            S_angleY = 90 - ServoY
            #controller.sendXServo(S_angleX)
            #controller.sendYServo(S_angleY)
            up += 1
            down -= 1
            print("Count: {}".format(count))
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("ServoY: {}".format(ServoY))
            print("S_angleY: {}".format(S_angleY))
            start = timer()
            if up > 5:
                up = 1
                down = 4
                count += 1

        if (count == 2):
            ServoX = angle[down]
            ServoY = angle[up]
            S_angleX = 90 + ServoX
            S_angleY = 90 + ServoY
            #controller.sendXServo(S_angleX)
            #controller.sendYServo(S_angleY)
            up += 1
            down -= 1
            print("Count: {}".format(count))
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("ServoY: {}".format(ServoY))
            print("S_angleY: {}".format(S_angleY))
            start = timer()
            if up > 5:
                up = 1
                down = 4
                count += 1

        if (count == 3):
            ServoX = angle[up]
            ServoY = angle[down]
            S_angleX = 90 - ServoX
            S_angleY = 90 + ServoY
            #controller.sendXServo(S_angleX)
            #controller.sendYServo(S_angleY)
            up += 1
            down -= 1
            print("Count: {}".format(count))
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("ServoY: {}".format(ServoY))
            print("S_angleY: {}".format(S_angleY))
            
            start = timer()
            if up > 5:
                up = 1
                down = 4
                count += 1

        if (count == 4):
            ServoX = angle[down]
            ServoY = angle[up]
            S_angleX = 90 - ServoX
            S_angleY = 90 - ServoY
            #controller.sendXServo(S_angleX)
            #controller.sendYServo(S_angleY)
            up += 1
            down -= 1
            print("Count: {}".format(count))
            print("ServoX: {}".format(ServoX))
            print("S_angleX: {}".format(S_angleX))
            print("ServoY: {}".format(ServoY))
            print("S_angleY: {}".format(S_angleY))
            start = timer()
            if up > 5:
                up = 1
                down = 4
                count = 1




