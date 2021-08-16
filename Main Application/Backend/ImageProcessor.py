import threading
import numpy as np
import cv2 as cv
from time import time
from math import sqrt
from Backend import ImageFrame

class ImageProcessor(threading.Thread):

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
    def __init__(self, cameraID, imgQueue):
        threading.Thread.__init__(self)
        self.imgQueue = imgQueue
        self.cap = cv.VideoCapture(cameraID)
        self.generateViewportSpec()
        self.lastTime = -1
        self.prevX = -1
        self.prevY = -1
        self.firstRun = True
        self.run = True

    # Determine the Viewport variables
    def generateViewportSpec(self):

        # Obtain the height and width of the camera view
        self.viewWidth = int(self.cap.get(3))
        self.viewHeight = int(self.cap.get(4))

        # Generate the centerPoint
        self.midWidth = self.viewWidth//2
        self.midHeight = self.viewHeight//2

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
            if circArea >= self.lowArea and circArea <= self.uppArea:
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

        if nContours == 0:
            BP_x = 0
            BP_y = 0
        ballFound = (nContours == 1)
        
        return ballFound, img, BP_x, BP_y, ball_x, ball_y
     
    # Calculate the elapsed time since the last frame
    def calculateElapsedTime(self):

        # Get current time
        currTime = time()

        # If this is the first run of the controller, return the default 30fps
        if (self.firstRun):
            self.lastTime = currTime
            return (1/30)
        
        # Otherwise, compare clock times
        else:
            timeElapsed = currTime - self.lastTime
            self.lastTime = currTime
            return timeElapsed

    # Collects and returns the data needed by the Director
    def getData(self):
        
        # Obtain frame and contours to get Ball Position
        ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY = self.generateContours()

        # Determine the time elapsed, unless this is the first frame
        elapsedTime = self.calculateElapsedTime()

        # Generate scalar velocity of ball
        if (ballFound):
            distanceTravelled = sqrt((self.prevX - BP_x) ^ 2 + (self.prevY - BP_y) ^ 2)
            velocity = distanceTravelled / elapsedTime

        # Append current position to cache
        self.prevX = BP_x
        self.prevY = BP_y

        # Debug Info
        print("Time elapsed : {}".format(elapsedTime))
        print("Ball Located? : {}", ballFound)
        print("Ball position: {} , {}".format(BP_x,BP_y))
        print("Ball Velocity: {} ms-1", velocity)
        
        return ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY, elapsedTime, velocity

    # Cleans up OpenCV on Application Exit
    def destroyProcessor(self):
        self.run = False
        
    # Method used for this Class when running as a Thread
    def run(self):

        # While this thread is running, continually refer to the camera frame.
        # Generate ImageFrame objects to store in the queue shared with the 
        # director.

        while (self.run):
        
            # Get the latest frame
            ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY, elapsedTime, velocity = self.getData()
            
            # Append to a new ImageFrame object
            imgFrameObj = ImageFrame(ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY, elapsedTime, velocity)
            self.imgQueue.put(imgFrameObj)

        # Release the camera and destroy OpenCV session
        self.cap.release()
        cv.destroyAllWindows()