import numpy as np
import cv2 as cv
from scipy.spatial import distance as dist

## Webcam capture and setting
# Laptop 0 front cam, 1 rear cam, 2 usb cam
cap = cv.VideoCapture(0)
#cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
camWidth = cap.get(3)  # currently 640
camHeight = cap.get(4)  # currently 480
fps = cap.get(cv.CAP_PROP_FPS)  #maybe 5
## try another FPS fetch method and compare : TO DO ...
use_time = 1 / fps

camWidth = int(camWidth)
camHeight = int(camHeight)
midWidth = camWidth//2  # 320 pixels
midHeight = camHeight//2  # 240 pixels
lowOrange = np.array([ 0, 120, 140]) 
uppOrange = np.array([ 22, 255, 255])

def getPosition(circFind):
    for contour in circFind:
        circArea = cv.contourArea(contour)
        if circArea > 1000:
            x, y, w, h = cv.boundingRect(contour)
            ball_x = (w//2 + x)
            ball_y = (h//2 + y)
            ball_x = ball_x - midWidth                              
            ball_y = midHeight - ball_y
    return ball_x, ball_y

    

while True:
    ret, frame = cap.read()
    img = frame.copy()   # Copy Frame for image processing
    # Filter by colour and make a mask
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lowOrange, uppOrange)
    # Get contours
    circFind, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    Xm, Ym = getPosition(circFind)

    #if circFind != 0:
    
 
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()       