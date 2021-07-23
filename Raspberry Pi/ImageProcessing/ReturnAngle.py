##
# To print the values found during the calculation process
# For testing purposes on Laptop, set for that situation

import numpy as np
import cv2 as cv
from time import time
from UART_Servo_Controller import UART_Servo_Controller

controller = UART_Servo_Controller('COM4')

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

maxAngle = 3
increment = 1

# PID specs
Kp = 2.768
Ki = 1.08
Kd = 1.771
timestep = 1/30  # 1/fps
Ui = 0
last_error = 0
setpoint = [0,0]  # centre

controller.sendXServo(S_angleX)
controller.sendYServo(S_angleY)


def PIDsys(pos, setpoint, timestep):
    global last_error
    global Ui
    error = setpoint - pos
    UiMax = 9.5
    
    if error < 0.005 and error > -0.005:
        error = 0
        last_error = error
        return error
    
    if Ui >= UiMax:
        Ui = UiMax

    Ui = (error * timestep) + Ui
    Ud = (error - last_error) / timestep
    output = (Kp*error) + (Ki*Ui) + (Kd*Ud)
    last_error = error
    
    print("Error: {}".format(error))
    print("Ui: {}".format(Ui))
    print("Ud: {}".format(Ud))
    print("Output: {}".format(output))
    return output

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
            x, y, w, h = cv.boundingRect(contour)
            ball_x = (w//2 + x)
            ball_y = (h//2 + y)
            BP_x = ball_x - midWidth                              
            BP_y = midHeight - ball_y
            BP_x = (BP_x / pxMetric) / 100
            BP_y = (BP_y / pxMetric) / 100    
            cv.circle(frame, (ball_x, ball_y), 30, (255, 0, 255), 2)
            cv.circle(frame, (ball_x, ball_y), 3, (255, 0, 255), -1)

            P_aX = PIDsys(BP_x, setpoint[0], timestep)
            P_aY = PIDsys(BP_y, setpoint[1], timestep)
            P_aX = int(round(P_aX))
            P_aY = int(round(P_aY))

            # result can be +/-, not related to ball position, 
            # so removing the negative as required
            if P_aX < 0:
                P_aX = P_aX * -1
            if P_aY < 0:
                P_aY = P_aY * -1

            # Set Max angle of plate
            if P_aX > maxAngle:
                P_aX = maxAngle
            if P_aY > maxAngle:
                P_aY = maxAngle

            # Set increments of servo angle
            if (P_aX - prevPlate_X) > increment :
                P_aX = prevPlate_X + increment
            elif (P_aX - prevPlate_X) > increment :
                P_aX = prevPlate_X - increment
  
            if (P_aY - prevPlate_Y) > increment :
                P_aY = prevPlate_Y + increment
            elif (P_aY - prevPlate_Y) > increment :
                P_aY = prevPlate_Y - increment
                
            # Convert output from plate angle to servo angle
            S_angleX = P_aX
            S_angleY = P_aY
            #S_angleX = (Length/d) * P_aX
            #S_angleY = (Length/d) * P_aY

            # Adjusting the plate angle to servo angle range,
            # by using ball position 
            if BP_x >= 0:
                S_angleX = 90 + S_angleX
            else:
                S_angleX = 90 - S_angleX

            if BP_y >= 0:
                S_angleY = 90 - S_angleY
            else:
                S_angleY = 90 + S_angleY
        
            controller.sendXServo(S_angleX)
            controller.sendYServo(S_angleY)

            prevPlate_X = P_aX
            prevPlate_Y = P_aY 

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