import threading
import UARTTX as UART

class ServoController(threading.Thread):
    
    # CONSTANTS
    MAX_ANGLE = 15          # Maximum Delfection Angle
    MAX_DELTA_ANGLE = 0.5    # Maximum Rate of change of Deflection Angle per Frame
    DELAY = 3                   # Delay between each delta of queue
    INITIAL_ANGLE = 90

    # Constructor
    def __init__(self, uartController):
        super(self, threading.Thread)
        self.uart = UART(uartController)
        self.keepRunning = True

        # Send initial commands to flatten the plate
        self.controller.sendXServo(ServoController.INITIAL_ANGLE)
        self.controller.sendYServo(ServoController.INITIAL_ANGLE)

    # Sets flag to kill thread safely
    def destroy(self):
        self.keepRunning = False

    # Converts to Servo Angle
    @staticmethod
    def toServoAngle(angleX, angleY):
        angleX = 90 - angleX
        angleY = 90 + angleY
        return angleX, angleY

    # Dampens the Final Angle and Rate of Change

    # Set next
    
    # Force next position

    # Main loop for this thread
    def run(self):

        while self.keepRunning:

            # Send the desired angle to the Controller
            self.uart.sendXServo(90)
            self.uart.sendYServo(90)
            return

    