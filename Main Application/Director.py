##
# To print the values found during the calculation process
# For testing purposes on Laptop, set for that situation
##

import queue
import ImageFrame
from PIDController import PIDController as PID
from time import time
from queue import Queue
from ImageProcessor import ImageProcessor
from Patterns.PatternTypes import PatternTypes
import cv2 as cv

# Initial Values for angles
P_aX = 0 # plate angle X initial value
P_aY = 0 # plate angle Y initial value
S_angleX = 90  # initial angle of servos
S_angleY = 90  # initial angle of servos

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
        self.xAxis = PID(Kp, Ki, Kd, setpoint[0])
        self.yAxis = PID(Kp, Ki, Kd, setpoint[1])

        # Initialise the Image Processor Thread
        self.imgQueue = Queue()
        self.imgProc = ImageProcessor(cameraID)

        # Controller
        self.controller = UART_Servo_Controller(serialAddress)

        # Flags
        self.enableVerbose = verbose
        self.keepRunning = True

        # Mode
        self.patternMode = PatternTypes.CENTER

    # The main loop for this thread
    def main(self):

        # Send initial commands to flatten the plate
        self.controller.sendXServo(S_angleX)
        self.controller.sendYServo(S_angleY)

        # Start the Image Processor Thread
        self.imgProc.run()

        # Keep running this loop of code until the the "terminate" method is called
        while(self.keepRunning):
            self.performLoopIteration()
            if cv.waitKey(1) == ord('q'):
                break
        
        # Safely destory the image processor
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
            return self.imgQueue.get_nowait()

    # Performs the logic needed for the Director to sequence the classes
    def performLoopIteration(self):

        # Grab the next Image from the Queue
        nextImg = ImageFrame(self.getNextQueueImage())
        
        # If no image is queued, return.
        if nextImg == None:
            if self.enableVerbose:
                print("No Frame in Queue to Process")
            return

        # Otherwise, if image is returned...
        else:
            
            # If ball is found
            if (nextImg.isBallFound()):

                if self.enableVerbose:
                    print("Ball Found in Frame")

                # Transmit the frame of the ball to the GUI
                # TODO
            
                # Send position data to the PID Controllers and determine the desired Plate Angles
                P_aX = self.xAxis.compute(BP_x, elapsedTime)
                P_aY = self.yAxis.compute(BP_y, elapsedTime)

                # Convert output from plate angle to servo angle
                S_angleX = P_aX
                S_angleY = P_aY

                # Adjusting the plate angle to servo angle range,
                # by using ball position 
                S_angleX = 90 - S_angleX
                S_angleY = 90 + S_angleY

                # Send the desired angle to the Controller
                self.controller.sendXServo(S_angleX)
                self.controller.sendYServo(S_angleY)

                # Print Verbose if Desired
                if (self.enableVerbose):
                    print("Plate Angle X, Y: {}, {}".format(P_aX, P_aY))

                    print("Servo angle X : {}".format(S_angleX))
                    print("Servo angle Y : {}".format(S_angleY))

            else:
                if self.enableVerbose:
                    print("Ball not found in frame")

    # Switch the mode of the Director to a Pattern or Otherwise
    # Must pass a PatternTypes Enum
    def setMode(self, patternMode):

        # If this is a type of Enumeration, then select the correct Pattern Object
        if isinstance(patternMode, PatternTypes):
            pass

        # Otherwise, throw an exception
        else:
            Exception("The mode provide is not a form of pattern.")

    # Sets the flag to terminate this Director object and it's threads
    def terminate(self):
        self.keepRunning = False