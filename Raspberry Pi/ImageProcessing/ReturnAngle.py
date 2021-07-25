##
# To print the values found during the calculation process
# For testing purposes on Laptop, set for that situation

import numpy as np
import cv2 as cv
from PIDController import PIDController as PID
from time import time
#from UART_Servo_Controller import UART_Servo_Controller


#controller = UART_Servo_Controller('COM4')


cap = cv.VideoCapture(2)
# Values for ImgProcessing
midWidth = 320
midHeight = 240
lowOrange = np.array([ 2, 120, 140])
uppOrange = np.array([ 24, 255, 255])
pxMetric = 7.8 # pixelperMetric for pixels to cm

# Initial Values for angles
P_aX = 0 # plate angle X initial value
P_aY = 0 # plate angle Y initial value
S_angleX = 90  # initial angle of servos
S_angleY = 90  # initial angle of servos
prevPlate_X = 0
prevPlate_Y = 0

d = 0.045 # servo arm length
Length = 0.06 # distance from servo plate connection to centre pivot point

increment = 1

# PID Specifications
Kp = 2.768
Ki = 1.08
Kd = 1.771

# Aim for the Setpoint in the Center of the Plate
setpoint = [0,0]

# PID Controllers for the Servos
xAxis = PID(Kp, Ki, Kd, setpoint[0])
yAxis = PID(Kp, Ki, Kd, setpoint[1])

# Send initial commands to flatten the plate
#controller.sendXServo(S_angleX)
#controller.sendYServo(S_angleY)

# Loop
while True:
    start = cv.getTickCount()
    ret, frame = cap.read()
    img = frame.copy()   # Copy Frame for image processing
    # Filter by colour and make a mask
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lowOrange, uppOrange)
    # Get contours
    circFind, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in circFind:
        circArea = cv.contourArea(contour)
        if circArea > 1000:
            x, y, w, h = cv.boundingRect(contour) #Draw bounding rectangle
            ball_x = (w//2 + x)         # Get X axis co-ord for center of rectangle
            ball_y = (h//2 + y)         # Get Y axis co-ord for conter of rectangle
            BP_x = ball_x - midWidth    # Get ball pos relative to center of plate being 0,0                             
            BP_y = midHeight - ball_y   
            BP_x = (BP_x / pxMetric) / 100      # Convert from pixels to cm, then meters
            BP_y = (BP_y / pxMetric) / 100    
            # Draw the found circle on the frame
            cv.circle(frame, (ball_x, ball_y), 30, (255, 0, 255), 2)
            cv.circle(frame, (ball_x, ball_y), 3, (255, 0, 255), -1)

            # Send position data to the PID Controllers and determine the desired Plate Angles
            P_aX = xAxis.compute(BP_x)
            P_aY = xAxis.compute(BP_y)

            # Round the Plate Angle
            # P_aX = int(round(P_aX))
            # P_aY = int(round(P_aY))

            # Convert output from plate angle to servo angle
            S_angleX = P_aX
            S_angleY = P_aY
            #S_angleX = (Length/d) * P_aX
            #S_angleY = (Length/d) * P_aY

            # Adjusting the plate angle to servo angle range,
            # by using ball position 
            S_angleX = 90 + S_angleX

            # Haven't checked Y angle yet
            S_angleY = 90 + S_angleY

        
            # Send the desired angle to the Controller
            #controller.sendXServo(S_angleX)
            #controller.sendYServo(S_angleY)

            print("Ball position: {} , {}".format(BP_x,BP_y))
            print("Plate Angle X: {}".format(P_aX))
            print("Plate Angle Y: {}".format(P_aY))
            print("Servo angle X : {}".format(S_angleX))
            print("Servo angle Y : {}".format(S_angleY))
        
           
            

    # Print x,y grid and centre - if desired
    cv.line(frame, (midWidth,0), (midWidth,480), (0,255,0), 1)  # Green colour
    cv.line(frame, (0,midHeight), (640,midHeight), (0,255,0), 1) # Green colour
    cv.circle(frame, (midWidth,midHeight), 6, (0,0,255), 2)  # Red colour
    cv.imshow("Frame", frame)

    end = cv.getTickCount()
    fq = cv.getTickFrequency()
    
    #print(end - start)
    tot_time = (end - start) / fq
    #print(tot_time*1000)

    if cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()      