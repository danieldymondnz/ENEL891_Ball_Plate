


import numpy as np
import cv2 as cv
from PIDController import PIDController as PID
from time import time
from UART_Servo_Controller import UART_Servo_Controller


controller = UART_Servo_Controller('COM3')


cap = cv.VideoCapture(2)
# Values for ImgProcessing
midWidth = 320
midHeight = 240

pxMetric = 7.5 # pixelperMetric for pixels to cm

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
#xAxis = PID(Kp, Ki, Kd, setpoint[0])
yAxis = PID(Kp, Ki, Kd, setpoint[1])

# Send initial commands to flatten the plate
controller.sendXServo(S_angleX)
controller.sendYServo(S_angleY)


while True:
    start = cv.getTickCount()  # Time Step for PID calculations. 
    # Get Frame
    ret, frame = cap.read()
    img = frame.copy()  

    grayframe = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    _ , thres = cv.threshold(grayframe, 188, 255, cv.THRESH_BINARY)

    #kernel = np.ones((2,2), np.uint8)
    kernel = np.ones((2,2), np.uint8)
    k2 = np.ones((6,6), np.uint8)
    diltimg = cv.dilate(thres, kernel)
    erodeimg = cv.erode(diltimg, k2)
    # Get contours
    circFind, _ = cv.findContours(erodeimg, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in circFind:
        circArea = cv.contourArea(contour)
        if circArea > 500:
            # Creates a rectangle around ball and calculates center point
            x, y, w, h = cv.boundingRect(contour) #Draw bounding rectangle
            ball_x = (w/2 + x)         # Get X axis co-ord for center of rectangle
            ball_y = (h/2 + y)         # Get Y axis co-ord for conter of rectangle
            # adjust to centre
            BP_x = ball_x - midWidth    # Get ball pos relative to center of plate being 0,0                             
            BP_y = midHeight - ball_y  
            # apply pixelMetric: pixels to cm
            # convert cm to m 
            BP_x = (BP_x / pxMetric) / 100      
            BP_y = (BP_y / pxMetric) / 100    
            # Draw the found circle on the frame
            cv.circle(frame, (int(ball_x), int(ball_y)), 30, (255, 0, 255), 2)
            cv.circle(frame, (int(ball_x), int(ball_y)), 3, (255, 0, 255), -1)

            # Time Step fpr PID calculations
            end = cv.getTickCount()
            fq = cv.getTickFrequency()
            tot_time = (end - start) / fq
            print("Time elapsed : ".format(end - start))
            print("Total Time : ".format(tot_time*1000))
            ### Need to send to PID as TIMESTEP ###
            
            # Send position data to the PID Controllers and determine the desired Plate Angles
            #P_aX = xAxis.compute(BP_x)
            P_aY = yAxis.compute(BP_y)

            # Round the Plate Angle
            # P_aX = int(round(P_aX))
            # P_aY = int(round(P_aY))

            # Convert output from plate angle to servo angle
            #S_angleX = P_aX
            S_angleY = P_aY
            #S_angleX = (Length/d) * P_aX
            #S_angleY = (Length/d) * P_aY

            # Adjusting the plate angle to servo angle range,
            # by using ball position 
            #S_angleX = 90 - S_angleX

            S_angleY = 90 + S_angleY

            # Send the desired angle to the Controller
            #controller.sendXServo(S_angleX)
            controller.sendYServo(S_angleY)

            # Print to view details
            print("Ball position: {} , {}".format(BP_x,BP_y))
            #print("Plate Angle X: {}".format(P_aX))
            print("Plate Angle Y: {}".format(P_aY))
            #print("Servo angle X : {}".format(S_angleX))
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
