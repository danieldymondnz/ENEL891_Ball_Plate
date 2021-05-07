#   UART Binary Servo Control Test Script
#   Sends two identical signals (bits 6:0) for the two servos (identified with bit 7)
#   for the FPGA to general two PWM signals to drive each servo.
#   Daniel Dymond 2021

#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':

    # Hook up to UART 2 (GPIO 0/1)
    ser2 = serial.Serial('/dev/ttyAMA1', 9600, timeout=1)
    ser2.flush()

    # Initial position of 10
    pos = 10
    delay = 0
    
    # Loop forever
    while True:

        if (delay > 2):
            pos += 10
            delay = 0

        if (pos > 119):
            pos = 10

        delay += 1

        # Conver number into byte
        # pos = 181
        byteX = [pos]
        byteY = [pos + 128]
        byteToTxX = bytearray(byteX)
        byteToTxY = bytearray(byteY)
        
        # Show verbose
        print("Tx'd: X=" + str(pos) + ", Y=" + str(pos + 128))

        # Send via UART2
        size = ser2.write(byteToTxX)
        size = ser2.write(byteToTxY)

        # Pause for 1s
        time.sleep(1)