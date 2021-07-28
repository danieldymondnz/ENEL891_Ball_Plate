##
# To print the values found during the calculation process
# For testing purposes on Laptop, set for that situation
##

from PIDController import PIDController as PID
from time import time
from UART_Servo_Controller import UART_Servo_Controller
from ImageProcessor import ImageProcessor
import cv2 as cv

# Constants
cameraID = 2

# Create a new Servo Controller and Image Processor
controller = UART_Servo_Controller('COM3')
imgProc = ImageProcessor(cameraID)

# Initial Values for angles
P_aX = 0 # plate angle X initial value
P_aY = 0 # plate angle Y initial value
S_angleX = 90  # initial angle of servos
S_angleY = 90  # initial angle of servos

d = 0.045 # servo arm length
Length = 0.06 # distance from servo plate connection to centre pivot point

# PID Specifications
Kp = 20 #2.768
Ki = 1.08
Kd = 15

# Aim for the Setpoint in the Center of the Plate
setpoint = [0,0]

# PID Controllers for the Servos
xAxis = PID(Kp, Ki, Kd, setpoint[0])
yAxis = PID(Kp, Ki, Kd, setpoint[1])

# Send initial commands to flatten the plate
controller.sendXServo(S_angleX)
controller.sendYServo(S_angleY)

# Loop
while True:
    
    # Grab new Position
    ballFound, BP_x, BP_y, elapsedTime = imgProc.getPosition()

    if (ballFound):

        print("Controller Command")
    
        # Send position data to the PID Controllers and determine the desired Plate Angles
        P_aX = xAxis.compute(BP_x, elapsedTime)
        P_aY = yAxis.compute(BP_y, elapsedTime)

        # Convert output from plate angle to servo angle
        S_angleX = P_aX
        S_angleY = P_aY

        # Adjusting the plate angle to servo angle range,
        # by using ball position 
        S_angleX = 90 - S_angleX
        S_angleY = 90 + S_angleY

        # Send the desired angle to the Controller
        controller.sendXServo(S_angleX)
        controller.sendYServo(S_angleY)

        # Print to view details
        
        print("Plate Angle X: {}".format(P_aX))
        print("Plate Angle Y: {}".format(P_aY))
        print("Servo angle X : {}".format(S_angleX))
        print("Servo angle Y : {}".format(S_angleY))

        if cv.waitKey(1) == ord('q'):
            break

imgProc.destroyProcessor() 