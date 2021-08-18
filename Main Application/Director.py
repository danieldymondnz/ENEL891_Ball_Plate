##
# To print the values found during the calculation process
# For testing purposes on Laptop, set for that situation
##

import queue
import time
from queue import Queue
import cv2 as cv
from Backend import *

# CONFIG

# Serial Port
BAUD_RATE = 9600
NUM_OF_BITS = 10

# Initial Values for angles
P_aX = 0 # plate angle X initial value
P_aY = 0 # plate angle Y initial value
S_angleX = 0  # initial angle of servos
S_angleY = 0  # initial angle of servos

d = 0.045 # servo arm length
Length = 0.06 # distance from servo plate connection to centre pivot point

# PID Specifications
Kp = 20 #2.768
Ki = 1.08
Kd = 15

# Aim for the Setpoint in the Center of the Plate
setpoint = [0,0]

class Director:

    # Initialise components for the Director
    def __init__(self, cameraID, serialAddress, verbose):

        # PID Controllers for the Servos
        self.xAxis = PID.PID(Kp, Ki, Kd, setpoint[0], False)
        self.yAxis = PID.PID(Kp, Ki, Kd, setpoint[1], False)

        # Initialise the Image Processor Thread
        self.imgQueue = Queue()
        self.imgProc = ImageProcessor.ImageProcessor(cameraID, self.imgQueue, False)
        self.imgProc.start()

        # Initialise the Augmentation System and start Thread
        self.augmentation = ServoPlateAugmentationSystem.ServoPlateAugmentationSystem(serialAddress, BAUD_RATE, NUM_OF_BITS, 0)
        self.augmentation.start()

        # Flags for this Class
        self.enableVerbose = verbose
        self.keepRunning = True

        # Mode
        # self.patternMode = PatternTypes.CENTER

    # The main loop for this thread
    def main(self):

        # Keep running this loop of code until the the "terminate" method is called
        while(self.keepRunning):
            self.performLoopIteration()
            if cv.waitKey(1) == ord('q'):
                self.keepRunning = False
        
        # Safely destroy the image processor
        self.imgProc.destroyProcessor()


    # Method checks the queue and gets the latest frame
    def getNextQueueImage(self):

        # Review the current number of items in the queue
        queueSize = self.imgQueue.qsize()

        # If no items exist, reuturn null
        if (queueSize == 0):
            return None

        elif (queueSize == 1):
            return self.imgQueue.get_nowait()
            
        else:
            while(self.imgQueue.qsize() > 1):
                self.imgQueue.get_nowait()
                if self.enableVerbose:
                    print("Frame was flushed from Queue")
            return self.imgQueue.get_nowait()

    # Performs the logic needed for the Director to sequence the classes
    def performLoopIteration(self):

        # Grab the next Image from the Queue
        nextImg = self.getNextQueueImage()
        
        # If no image is queued, return.
        if nextImg == None:
            if self.enableVerbose:
                print("No Frame in Queue to Process")
            return

        # Otherwise, if image is returned...
        # If ball is found
        if (nextImg.isBallFound()):

            if self.enableVerbose:
                print("Ball Found in Frame")

            # Get Information
            BP_x, BP_y = nextImg.getBallPosition()
            timestamp = nextImg.getTimeStamp()

            # Transmit the frame of the ball to the GUI
            # TODO

        
            # Send position data to the PID Controllers and determine the desired Plate Angles
            P_aX = self.xAxis.compute(BP_x, timestamp)
            P_aY = self.yAxis.compute(BP_y, timestamp)

            # Send the desired angle to SPAS for Augmentation and Tx
            self.augmentation.setNextAngle(P_aX, P_aY)

            # Print Verbose if Desired
            if (self.enableVerbose):
                print("Ball Pos X, Y: {}, {}".format(BP_x, BP_y))
                print("Plate Angle X, Y: {}, {}".format(P_aX, P_aY))

        else:
            if self.enableVerbose:
                print("Ball not found in frame")

    # Switch the mode of the Director to a Pattern or Otherwise
    # Must pass a PatternTypes Enum
    def setMode(self, patternMode):

        # If this is a type of Enumeration, then select the correct Pattern Object
        if isinstance(patternMode, PatternTypes):
            pass

        # Return back to ZERO POSITION

        # Then Change Mode

        # Otherwise, throw an exception
        else:
            Exception("The mode provide is not a form of pattern.")

        # Return if execution complete
        return True

    # Sets the flag to terminate this Director object and it's threads
    def terminate(self):
        self.keepRunning = False