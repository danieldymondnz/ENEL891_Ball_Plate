##
# To print the values found during the calculation process
# For testing purposes on Laptop, set for that situation
##

from Backend.ImgProcess import ImgProcess
import threading
from queue import Queue
import cv2 as cv
from Backend import *

# CONFIG

# Serial Port
BAUD_RATE = 9600
NUM_OF_BITS = 8

# PID Specifications
KP = 20 #2.768
KI = 1.08
KD = 15

class Director(threading.Thread):

    # Initialise components for the Director
    def __init__(self, cameraID, serialAddress, verbose):

        # Aim for the setpoint in the Center of the Plate
        self.setpoint = [0,0]

        # PID Controllers for the Servos
        self.xAxis = PID.PID(KP, KI, KD, self.setpoint[0], False)
        self.yAxis = PID.PID(KP, KI, KD, self.setpoint[1], False)

        # Initialise the Image Processor Thread
        self.imgQueue = Queue()
        #self.imgProc = ImageProcessor.ImageProcessor(cameraID, self.imgQueue, False)
        self.imgProc = ImgProcess.ImgProcess(cameraID, self.imgQueue, False)
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
    def run(self):

        # Keep running this loop of code until the the "terminate" method is called
        while(self.keepRunning):
            self.__performLoopIteration__()
        
        # Safely destroy the image processor
        self.imgProc.destroyProcessor()

    # Method checks the queue and gets the latest frame
    def __getNextQueueImage__(self):

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
    def __performLoopIteration__(self):

        # Grab the next Image from the Queue
        nextImg = self.__getNextQueueImage__()

        # If no image is queued, return.
        if nextImg == None:
            if self.enableVerbose:
                print("No Frame in Queue to Process")
            return

        # Transmit the frame of the ball to the GUI
        # TODO
        
        # If plate is being overriden to flat, then set servo position
        if self.returnPlateToFlat == True:
            if self.enableVerbose:
                print("Plate set to flatten")
            return

        # Otherwise, if image is returned...
        # If ball is found
        if (nextImg.isBallFound()):

            if self.enableVerbose:
                print("Ball Found in Frame")

            # Get Information
            BP_x, BP_y = nextImg.getBallPosition()
            timestamp = nextImg.getTimeStamp()

            
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

    def holdPlate(self):
        ''' Hold the plate in the current position. '''
        self.augmentation.hold()

    def releasePlate(self):
        ''' Release any active hold acting on the plate and resume control. '''
        self.augmentation.resume()
        self.returnPlateToFlat = False

    def flattenPlate(self):
        ''' Returns the plate to the flat position. '''
        self.augmentation.setNextAngle(0,0)
        self.returnPlateToFlat = True

    def kill(self):
        ''' Destroys the director thread and all child objects. '''
        self.keepRunning = False