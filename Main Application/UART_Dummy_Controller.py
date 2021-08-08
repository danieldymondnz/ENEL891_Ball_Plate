# Dummy Controller
# Has all controls of the original controller, but no functionality. Used for testing.

class UART_Dummy_Controller:

    # Constants for maximum angle deflection from 90 degrees
    MAX_DEFLECTION = 32
    X_ANGLE_TUNER =  -2.5 * 2      # Values for ANGLE_TUNER is [desired angle] * 2
    Y_ANGLE_TUNER = 0 * 2

    # The Constructor which sets the Serial Port
    def __init__(self, uartDevicePath):
        return

    # Function to handle X Servo Angle and Control Ouputs
    @staticmethod
    def sendXServo(servoXAngle):
        return

    # Function to handle Y Servo Angle and Control Outputs
    @staticmethod 
    def sendYServo(servoYAngle):
        return

    # Private methods to be set private

    # Converts a Given Angle into the 7-bit value required by the FPGA
    def convertAngle(angle):

        # Check if angle is a number between 0 to 180 deg, otherwise throw exception
        try:
            angle = int(angle)
        except ValueError:
            raise ValueError("The angle specified is not a valid numerical value.")

        if (angle > 180 or angle < 0):
            raise ValueError("The angle specified is outside the scope of this servo.")

        # If value is okay, then convert into closest binary representation
        binaryPos = ((angle - 58) / 0.5) - 1
        binaryPos = int(binaryPos)
        return binaryPos

    # Takes the Binary Position Data and Servo Select and generates the 8-bit value
    def generateUARTData(binaryPosition, isYServo):

        # Assembles the byte
        if (isYServo == 1):
            byteInt = binaryPosition + 128
        else:
            byteInt = binaryPosition
        
        byte = [byteInt]

        return bytearray(byte)


    # Performs the UART TX for some given data
    def uartTX(data):
        return