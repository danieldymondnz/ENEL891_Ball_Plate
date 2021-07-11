# Servo Controller
# Sets a UART Controller on specified UART device with baud of 9600

import serial

class UART_Servo_Controller:

    # Constants for maximum angle deflection from 90 degrees
    MAX_DEFLECTION = 20

    # The Constructor which sets the Serial Port
    def __init__(self, uartDevicePath):
        global serialPort
        serialPort = serial.Serial(uartDevicePath, 9600, timeout=1)
        serialPort.flush()

    # Function to handle X Servo Angle and Control Ouputs
    @staticmethod
    def sendXServo(servoXAngle):
        xAngleBits = UART_Servo_Controller.convertAngle(servoXAngle)
        xByte = UART_Servo_Controller.generateUARTData(xAngleBits, 0)
        UART_Servo_Controller.uartTX(xByte)

    # Function to handle Y Servo Angle and Control Outputs
    @staticmethod 
    def sendYServo(servoYAngle):
        yAngleBits = UART_Servo_Controller.convertAngle(servoYAngle)
        yByte = UART_Servo_Controller.generateUARTData(yAngleBits, 1)
        UART_Servo_Controller.uartTX(yByte)

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

        # If angle is greater than bound, then set to the maximum
        if (abs(angle - 90) < UART_Servo_Controller.MAX_DEFLECTION):
            angle = angle / abs(angle) * UART_Servo_Controller.MAX_DEFLECTION

        # If value is okay, then convert into closest binary representation
        binaryPos = angle / 180 * 127
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
        global serialPort
        size = serialPort.write(data)