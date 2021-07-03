
import numpy as np
import cv2 as cv

## Webcam capture and setting

def nothing(x):
    pass

# To adjust HSV values and find Pixel Metric
cap = cv.VideoCapture(0)
camWidth = cap.get(3)
camHeight = cap.get(4)
fps = cap.get(cv.CAP_PROP_FPS) 
camWidth = int(camWidth)
camHeight = int(camHeight)
midWidth = camWidth//2
midHeight = camHeight//2
cv.namedWindow('Trackbars')
cv.createTrackbar('H_Low', 'Trackbars', 0, 179,nothing)
cv.createTrackbar('H_Upper', 'Trackbars', 0, 179,nothing)
cv.createTrackbar('S_Low', 'Trackbars', 0, 255,nothing)
cv.createTrackbar('S_Upper', 'Trackbars', 0, 255,nothing)
cv.createTrackbar('V_Low', 'Trackbars', 0, 255,nothing)
cv.createTrackbar('V_Upper', 'Trackbars', 0, 255,nothing)
    
while True:
    ret, frame = cap.read()
    HL = cv.getTrackbarPos('H_Low', 'Trackbars')
    SL = cv.getTrackbarPos('S_Low', 'Trackbars')
    VL = cv.getTrackbarPos('V_Low', 'Trackbars')
    HU = cv.getTrackbarPos('H_Upper', 'Trackbars')
    SU = cv.getTrackbarPos('S_Upper', 'Trackbars')
    VU = cv.getTrackbarPos('V_Upper', 'Trackbars')
    lowOrange = np.array([ HL, SL, VL])
    uppOrange = np.array([ HU, SU, VU])
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lowOrange, uppOrange)
    cv.imshow("Frame", frame)
    cv.imshow("Mask", mask)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
    
print("Low Orange = ", lowOrange)
print("Upper Orange = ", uppOrange)
print("MidWidth = ", midWidth)
print("MidHeight = ", midHeight)
