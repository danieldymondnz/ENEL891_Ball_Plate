##
# To print the values found during the calculation process
# For testing purposes

import numpy as np
import cv2 as cv

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
d = 0.05 # servo arm length
Length = 0.10 # distance from servo plate connection to centre pivot point
# PID specs
Kp = 2
Ki = 0.3
Kd = 1.8
timestep = 1/30  # 1/fps
Ui = 0
last_error = 0
setpoint = [0,0]

def getPosition(circFind):  # returns ball position (x,y) [meters]
    # for contours found - finds circle
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
    return ball_x, ball_y, BP_x, BP_y

#def tiltAdjust(pos,angle):
    # Adjust for plate tilt 
    # cos is for radians
    #angle = angle / toRads
    #pos = np.cos(angle) * pos
    #return pos

def PIDsys(pos, setpoint, timestep):
    global last_error
    global Ui
    error = setpoint - pos
    # if error +/- 0.03: error = 0
    Ui = (error * timestep) + Ui
    Ud = (error - last_error) / timestep
    output = (Kp*error) + (Ki*Ui) + (Kd*Ud)
    last_error = error
    return output

while True:
    ret, frame = cap.read()
    img = frame.copy()   # Copy Frame for image processing
    # Filter by colour and make a mask
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lowOrange, uppOrange)
    # Get contours
    circFind, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    if circFind != 0:
        ball_x, ball_y, Xm, Ym = getPosition(circFind)  # X pos measured , Y pos measured : [meters]
        cv.circle(frame, (ball_x, ball_y), 35, (255, 0, 255), 2)
        cv.circle(frame, (ball_x, ball_y), 3, (255, 0, 255), -1)
        # Adjust for plate tilt
        #if 10 < P_aX < -10:  # if angle 0-70 or 120-180
            #Xm = tiltAdjust(Xm,P_aX)
        #if 10 < P_aY < -10:  # if angle 0-70 or 120-180
            #Ym = tiltAdjust(Ym,P_aY)
        # Send ball X,Y into PID, return Output angle
        UX = PIDsys(Xm, setpoint[0], timestep)
        UY = PIDsys(Ym, setpoint[1], timestep)
        P_aX = UX
        P_aY = UY

        # Convert output from plate angle to servo angle
        S_angleX = (Length/d) * P_aX
        S_angleY = (Length/d) * P_aY

        S_angleX = 90 + S_angleX
        S_angleY = 90 - S_angleY

        print("Ball position: {} , {}".format(Xm,Ym))
        print("Output X: {}".format(UX))
        print("Output Y: {}".format(UY))
        print("Servo angle X : {}".format(S_angleX))
        print("Servo angle Y : {}".format(S_angleY))

     # Print x,y grid and centre - if desired
    cv.line(frame, (midWidth,0), (midWidth,480), (0,255,0), 1)  # Green colour
    cv.line(frame, (0,midHeight), (640,midHeight), (0,255,0), 1) # Green colour
    cv.circle(frame, (midWidth,midHeight), 6, (0,0,255), 2)  # Red colour
    cv.imshow("Frame", frame)

    if cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()      