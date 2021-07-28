

import numpy as np
import cv2 as cv
import time

class ImageProcessor:

    # Constants
    # cap = camera

    # Camera Viewport Specifications
    viewWidth = 640
    viewHeight = 480
    midWidth = 320
    midHeight = 240
    pxMetric = 7.5 # pixelperMetric for pixels to cm

    # Profile for Ball
    lowOrange = np.array([ 2, 120, 140])
    uppOrange = np.array([ 24, 255, 255])
    lowArea = 1000
    uppArea = 3000

    # Constructor
    def __init__(self, cameraID):
        self.cap = cv.VideoCapture(cameraID)
        self.generateViewportSpec()
        self.lastTime = -1


    # Determine the Viewport variables
    def generateViewportSpec(self):

        # Obtain the height and width of the camera view
        self.viewWidth = int(self.cap.get(3))
        self.viewHeight = int(self.cap.get(4))

        # Generate the centerPoint
        self.midWidth = self.viewWidth//2
        self.midHeight = self.viewHeight//2

    # Locate and return the position of the ball
    def getPosition(self):

        # Obtain frame and contours
        ballFound, BP_x, BP_y = self.generateContours()

        # Determine the time elapsed, unless this is the first frame
        elapsedTime = self.calculateElapsedTime()

        # Debug Info
        print("Time elapsed : {}".format(elapsedTime))
        print("Ball Located? : {}", ballFound)
        print("Ball position: {} , {}".format(BP_x,BP_y))

        return ballFound, BP_x, BP_y

    # Capture image from the Camera and grab contours
    def generateContours(self):

        # Get the frame and make a copy for Image Processing
        ret, frame = self.cap.read()
        img = frame.copy()

        # Filter by colour and make a mask
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, self.lowOrange, self.uppOrange)

        # Find the contours & process to find the ball
        circFind, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        nContours = 0
        for contour in circFind:
            circArea = cv.contourArea(contour)
            if circArea >= self.lowArea & contour <= self.uppArea:
                nContours += 1
                # Creates a rectangle around ball and calculates center point
                x, y, w, h = cv.boundingRect(contour) #Draw bounding rectangle
                ball_x = (w/2 + x)         # Get X axis co-ord for center of rectangle
                ball_y = (h/2 + y)         # Get Y axis co-ord for conter of rectangle
                # adjust to centre
                BP_x = ball_x - self.midWidth    # Get ball pos relative to center of plate being 0,0                             
                BP_y = self.midHeight - ball_y  
                # apply pixelMetric: pixels to cm
                # convert cm to m 
                BP_x = (BP_x / self.pxMetric) / 100      
                BP_y = (BP_y / self.pxMetric) / 100 


        ballFound = (nContours == 1)
        
        return ballFound, BP_x, BP_y

        
    # Calculate the elapsed time since the last frame
    def calculateElapsedTime(self):

        # Get current time
        currTime = time()

        # If this is the first run of the controller, return the default 30fps
        if (self.lastTime == -1):
            self.lastTime = currTime
            return (1/30)
        
        # Otherwise, compare clock times
        else:
            timeElapsed = currTime - self.lastTime
            self.lastTime = currTime
            return timeElapsed


    # Cleans up OpenCV on Application Exit
    def destroyProcessor(self):
        self.cap.release()
        cv.destroyAllWindows()