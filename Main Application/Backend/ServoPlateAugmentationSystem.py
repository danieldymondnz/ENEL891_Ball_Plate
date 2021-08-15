import threading
import time

class ServoPlateAugmentationSystem(threading.Thread):

    # Constants
    MAX_ANGLE = 15          # Maximum Delfection Angle
    MAX_DELTA_ANGLE = 5     # Maximum Rate of change of Deflection Angle / sec

    def __init__(self, baud, bits):
        threading.Thread.__init__(self)
        self.baudDelay = ServoPlateAugmentationSystem.__calculateDelay__(baud, bits)
        self.framePerSec = baud / bits

    @staticmethod
    def __calculateDelay__(baud, bits):
        '''
        Calculate the delay used based on the Baud Rate and number of Bits per packet. 
        Method is able to be modified further to add/remove delays to compesnate for python execution.
        '''
        period = 1 / (baud / bits)
        return period

    
    def plateAugmentation(rawAngle):
        
        newAngle = rawAngle
        return newAngle


        # Caps the maximum angle
        if newOutput > PID.MAX_ANGLE:
            newOutput = PID.MAX_ANGLE
        elif newOutput < -1 * PID.MAX_ANGLE:
            newOutput = -1 * PID.MAX_ANGLE

        # Check the change in angle
        # TODO Check this!
        # Set increments of servo angle
        if abs(newOutput - self.output) > PID.MAX_DELTA_ANGLE:
            newOutput = (newOutput / abs(newOutput)) * PID.MAX_DELTA_ANGLE