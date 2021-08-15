import threading
import time
import UART as UART

class ServoPlateAugmentationSystem(threading.Thread):

    # Constants
    MAX_ANGLE = 15          # Maximum Delfection Angle
    MAX_DELTA_ANGLE = 5     # Maximum Rate of change of Deflection Angle / sec

    def __init__(self, devicePath, baud, bits):
        threading.Thread.__init__(self)
        self.baudDelay = ServoPlateAugmentationSystem.__calculateDelay__(baud, bits)
        self.framePerSec = baud / bits
        self.dTheta = ServoPlateAugmentationSystem.MAX_DELTA_ANGLE/self.framePerSec
        
        # Initalise variables
        self.setXAngle = 0
        self.setYAngle = 0
        self.currXAngle = 0
        self.currYAngle = 0

        # Create UART Controller
        self.uart = UART(devicePath)

        # Operating Flags
        self.keepRunning = True
        self.pause = False

    @staticmethod
    def __calculateDelay__(baud, bits):
        '''
        Calculate the delay used based on the Baud Rate and number of Bits per packet. 
        Method is able to be modified further to add/remove delays to compesnate for python execution.
        '''
        period = 1 / (baud / bits)
        return period

    @staticmethod
    def __convAngleToServo__(servoXAngle, servoYAngle):
        ''' Convert from plate axis system to servo axis system. '''
        servoXAngle = 90 - servoXAngle
        servoYAngle = 90 + servoYAngle
        return servoXAngle, servoYAngle

    def setNextAngle(self, setXAngle, setYAngle):
        ''' Set a new desired angle for the servos in degrees. '''
        self.setXAngle = setXAngle
        self.setYAngle = setYAngle
    
    def plateAugmentation(self):
        
        servoX = self.servoXAngle
        servoY = self.servoYAngle


        # Convert to Servo Angle system
        servoX, servoY = ServoPlateAugmentationSystem.__convAngleToServo__(servoX, servoY)

        return self.currXAngle, self.currYAngle


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

    def terminate(self):
        ''' Terminate the '''
        self.keepRunning = False

    def pauseResume(self):
        ''' Pause/Resume the movement of the plate without terminating the thread. '''
        self.pause = not self.pause

    def run(self):
        
        # Keep Thread alive unless the keepRunning flag is unset
        while self.keepRunning:

            # If not paused, continue to generate positions
            if not self.pause:
                # Execute
                continue
            
            # Put the thread to sleep for the baud delay
            time.sleep(self.baudDelay)