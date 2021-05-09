#   UART Controller Implementation Test Script
#   Sends two identical angles using the UART Servo Controller
#   for use by the FPGA to generate two PWM signals
#   Daniel Dymond 2021

import time
from UART_Servo_Controller.py import UART_Servo_Controller
if __name__ == '__main__':

    # Create new Controller Object on UART2 for RPi-IoT
    controller = UART_Servo_Controller('/dev/ttyAMA1')

    # Initial position of 0 degrees
    angle = 0
    
    # Loops in 10 deg increments
    while True:

        # Set angle for this increment
        angle += 10
        if (angle > 180)
            angle = 0

        # Show Verbose
        print("Angle Out: " + str(angle))
        
        # Send via UART2
        controller.sendXServo(angle)
        controller.sendYServo(angle)

        # Pause for 5s
        time.sleep(1)