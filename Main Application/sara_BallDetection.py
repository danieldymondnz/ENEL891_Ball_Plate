import numpy as np
import cv2 as cv

class BallDetection:

    # Camera Viewport Specifications
    viewWidth = 640
    viewHeight = 480
    midWidth = 320
    midHeight = 240
    pxMetric = 7.5
    lowArea = 1000 # check
    uppArea = 3000 # check

    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.firstRun = True

    def getFrame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            print("Image Capture Error")
            # "No Frame found"
        
    def generateContours(self, img):
        # Binary threshold
        greyImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _ , thres = cv.threshold(greyImg, 188, 255, cv.THRESH_BINARY)

        # Removes some noise from image
        kernel = np.ones( (2,2), np.uint8 )
        kernel2 = np.ones( (6,6), np.uint8 )
        dilateImg = cv.dilate(thres, kernel)
        self.erodeImg = cv.erode(dilateImg, kernel2)

        # Find the contours & process to find the ball
        circFind , _ = cv.findContours(self.erodeImg, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        nContours = 0
        for contour in circFind:
            circArea = cv.contourArea(contour)
            if circArea >= BallDetection.lowArea and circArea <= BallDetection.uppArea:
                nContours += 1
                x, y, w, h = cv.boundingRect(contour)
                # Ball position in pixel co-ords
                ball_x = (w/2 + x)
                ball_y = (h/2 + y)

                # Ball position in meters and cartesian co-ords
                BP_x = (ball_x - BallDetection.midWidth)
                BP_y = (BallDetection.midHeight - ball_y)
                BP_x = (BP_x / BallDetection.pxMetric) / 100
                BP_y = (BP_y / BallDetection.pxMetric) / 100

        if nContours == 0:
               # BP_x = 0
               # BP_y = 0
            pass
        ballFound = (nContours == 1)

        return ballFound, BP_x, BP_y, ball_x, ball_y


    def getBallPosition(self):
        img = self.getFrame()
        ballFound, cameraFrame, BP_x, BP_y, pixelX, pixelY = self.generateContours(img)  
        if (ballFound):
            self.prevX = BP_x
            self.prevY = BP_y
          


    def destroyCamera(self):
        self.cap.release()
        cv.destroyAllWindows() 