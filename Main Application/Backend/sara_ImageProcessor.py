import threading
import numpy as np
import cv2 as cv
from time import time
from math import sqrt
from Backend.ImageFrame import ImageFrame as ImageFrame

class ImageProcessor(threading.Thread):

    # Camera Viewport Specifications
    viewWidth = 640
    viewHeight = 480
    midWidth = 320
    midHeight = 240
    pxMetric = 7.5 # pixelperMetric for pixels to cm

    # Profile for Ball
    lowArea = 1000 # check
    uppArea = 3000 # check

    # Constructor
    def __init__(self, cameraID, imgQueue, enableVerbose):
        threading.Thread.__init__(self)
        self.imgQueue = imgQueue
        self.cap = cv.VideoCapture(cameraID)
        self.generateViewportSpec()
        self.lastTime = -1
        self.prevX = -1
        self.prevY = -1
        self.firstRun = True
        self.keepRunning = True
        self.enableVerbose = enableVerbose

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

         # Binary threshold
        greyImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _ , thres = cv.threshold(greyImg, 188, 255, cv.THRESH_BINARY)

        # Removes some noise from image
        kernel = np.ones( (2,2), np.uint8 )
        kernel2 = np.ones( (6,6), np.uint8 )
        dilateImg = cv.dilate(thres, kernel)
        erodeImg = cv.erode(dilateImg, kernel2)

         # Find the contours & process to find the ball
        circFind , _ = cv.findContours(erodeImg, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        nContours = 0
        for contour in circFind:
            circArea = cv.contourArea(contour)
            if circArea >= ImageProcessor.lowArea and circArea <= ImageProcessor.uppArea:
                nContours += 1
                x, y, w, h = cv.boundingRect(contour)
                # Ball position in pixel co-ords
                ball_x = (w/2 + x)
                ball_y = (h/2 + y)
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
            ball_x = 0
            ball_y = 0
        ballFound = (nContours == 1)
        
        return ballFound, img, BP_x, BP_y, ball_x, ball_y

 # Collects and returns the data needed by the Director
    def getData(self):

        velocity = 0
        elapsedTime = 0

        # Obtain frame and contours to get Ball Position
        ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY = self.generateContours()

        # Debug Info
        if self.enableVerbose:
            print("Ball Located? : {}".format(ballFound))
            print("Ball position: {} , {}".format(BP_x,BP_y))
        
        return ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY, elapsedTime, velocity

    # Cleans up OpenCV on Application Exit
    def destroyProcessor(self):
        self.keepRunning = False
        
    # Method used for this Class when running as a Thread
    def run(self):

        # While this thread is running, continually refer to the camera frame.
        # Generate ImageFrame objects to store in the queue shared with the 
        # director.

        while (self.keepRunning):
        
            # Get the latest frame
            ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY, elapsedTime, velocity = self.getData()
            
            # Display Debug
            if self.enableVerbose:
                # Print x,y grid and centre
                cv.line(cameraImage, (320,0), (320,480), (0,255,0), 1)  # Green colour
                cv.line(cameraImage, (0,240), (640,240), (0,255,0), 1) # Green colour
                cv.circle(cameraImage, (320,240), 6, (0,0,255), 2)  # Red colour
                if ballFound:
                    cv.circle(cameraImage, (int(pixelX), int(pixelY)), 30, (255, 0, 255), 2)
                    cv.circle(cameraImage, (int(pixelX), int(pixelY)), 3, (255, 0, 255), -1)

                cv.imshow("Frame", cameraImage)

                if cv.waitKey(1) == ord('q'):
                    self.keepRunning = False

            # Append to a new ImageFrame object
            imgFrameObj = ImageFrame(ballFound, cameraImage, BP_x, BP_y, pixelX, pixelY, elapsedTime, velocity)
            self.imgQueue.put(imgFrameObj)

        # Release the camera and destroy OpenCV session
        self.cap.release()
        cv.destroyAllWindows()