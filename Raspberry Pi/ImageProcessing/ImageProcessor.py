

import numpy as np
import cv2 as cv

class ImageProcessor:

    # Constants
    # cap = camera

    # Camera Viewport Specifications
    viewWidth = 640
    viewHeight = 480
    midWidth = 320
    midHeight = 240
    pxMetric = 7.5 # pixelperMetric for pixels to cm

    # Colour Profile for Ball
    lowOrange = np.array([ 2, 120, 140])
    uppOrange = np.array([ 24, 255, 255])

    # Constructor



    # Determine the Viewport variables
    def generateViewportSpec(self):

        # Obtain the height and width of the camera view
        self.viewWidth = int(self.cap.get(3))
        self.viewHeight = int(self.cap.get(4))

        # Generate the centerPoint
        self.midWidth = self.viewWidth//2
        self.midHeight = self.viewHeight//2

    # Locate and return the position of the ball
    