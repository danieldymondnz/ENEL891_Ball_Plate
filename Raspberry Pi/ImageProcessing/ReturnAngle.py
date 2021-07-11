##
# To print the values found during the calculation process
# For testing purposes

import numpy as np
import cv2 as cv
from time import time

cap = cv.VideoCapture(0)
# Values for ImgProcessing
midWidth = 320
midHeight = 240
lowOrange = np.array([ 0, 120, 140])
uppOrange = np.array([ 22, 255, 255])
pxMetric = 16.84 # pixelperMetric for pixels to cm
toRads = 180 / np.pi
# Initial Values for angles
P_aX = 0 # plate angle X initial value
P_aY = 0 # plate angle Y initial value
S_angleX = 90  # initial angle of servos
S_angleY = 90  # initial angle of servos
prevServo_X = 0 # initial
prevServo_Y = 0 # initial
d = 0.05 # servo arm length
Length = 0.10 # distance from servo plate connection to centre pivot point
# PID specs
Kp = 2.66
Ki = 0
Kd = 1.68
timestep = 1/30  # 1/fps
UiSum = 0
last_error = 0
setpoint = [0,0]  # centre

#def tiltAdjust(pos,angle):
    # Adjust for plate tilt 
    # cos is for radians
    #angle = angle / toRads
    #pos = np.cos(angle) * pos
    #return pos
def PIDsys(pos, setpoint, timestep):
    global last_error
    global UiSum
    error = setpoint - pos
    # if error +/- 0.5: error = 0
    #check this is ok
    if error < 0.005 and error > -0.005:
        error = 0
        last_error = error
        return error
    
    Ui = (error * timestep) + UiSum
    Ud = (error - last_error) / timestep
    output = (Kp*error) + (Ki*Ui) + (Kd*Ud)
    last_error = error
    UiSum = UiSum + Ui
    ## If using Intergrator, need to stop windup
    #if UiSum > UiMax:
        #UiSum = UiMax
    
    return output

#loop_time = time()

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
            # adjust to centre
            BP_x = ball_x - midWidth                              
            BP_y = midHeight - ball_y
            # apply pixelMetric: pixels to cm
            # convert cm to m
            BP_x = (BP_x / pxMetric) / 100
            BP_y = (BP_y / pxMetric) / 100    
    
            cv.circle(frame, (ball_x, ball_y), 35, (255, 0, 255), 2)
            cv.circle(frame, (ball_x, ball_y), 3, (255, 0, 255), -1)
            # Adjust for plate tilt
            #if 10 < P_aX < -10:  # if angle 0-70 or 120-180
                #Xm = tiltAdjust(Xm,P_aX)
            #if 10 < P_aY < -10:  # if angle 0-70 or 120-180
                #Ym = tiltAdjust(Ym,P_aY)
            # Send ball X,Y into PID, return Output angle
        
            P_aX = PIDsys(BP_x, setpoint[0], timestep)
            P_aY = PIDsys(BP_y, setpoint[1], timestep)
            # Round result since it not matter to servo
            P_aX = int(round(P_aX))
            P_aY = int(round(P_aY))

            # result can be +/-, not related to ball position, 
            # so removing the negative as required
            if P_aX < 0:
                P_aX = P_aX * -1
            if P_aY < 0:
                P_aY = P_aY * -1

            # Set Max angle of plate
            #if P_aX > 20:
                #P_aX = 20
            #if P_aY > 20:
                #P_aY = 20

             # Set increments of servo angle
            #if (P_aX - prevPlate_X) > 1 :
                #P_aX = 2
            #if (P_aY - prevPlate_Y) > 1 :
                #P_aY = 2
  
            # Convert output from plate angle to servo angle
            S_angleX = (Length/d) * P_aX
            S_angleY = (Length/d) * P_aY

            # Angle checks,
            #if S_angleX < 1 and not 0:
                #S_angleX = 1
            
            #if S_angleY < 1 and not 0:
                #S_angleY = 1

           
            # Adjusting the plate angle to servo angle range,
            # by using ball position 
            if BP_x >= 0:
                S_angleX = 90 - S_angleX
            else:
                S_angleX = 90 + S_angleX

            if BP_y >= 0:
                S_angleY = 90 + S_angleY
            else:
                S_angleY = 90 - S_angleY
        
            
            prevPlate_X = P_aX
            prevPlate_Y = P_aY 

            print("Ball position: {} , {}".format(BP_x,BP_y))
            print("Output X: {}".format(P_aX))
            print("Output Y: {}".format(P_aY))
            print("Servo angle X : {}".format(S_angleX))
            print("Servo angle Y : {}".format(S_angleY))

            

     # Print x,y grid and centre - if desired
    cv.line(frame, (midWidth,0), (midWidth,480), (0,255,0), 1)  # Green colour
    cv.line(frame, (0,midHeight), (640,midHeight), (0,255,0), 1) # Green colour
    cv.circle(frame, (midWidth,midHeight), 6, (0,0,255), 2)  # Red colour
    cv.imshow("Frame", frame)
    #print('Elapsed {}'.format(1 / (time() - loop_time)))
    #loop_time = time()

    end = cv.getTickCount()
    fq = cv.getTickFrequency()
    
    #print(end - start)
    tot_time = (end - start) / fq
    #print(tot_time*1000)

    if cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()      