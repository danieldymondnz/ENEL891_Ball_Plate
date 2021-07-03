#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser2 = serial.Serial('/dev/ttyAMA1', 9600, timeout=1)
    ser3 = serial.Serial('/dev/ttyAMA2', 9600, timeout=1)
    ser2.flush()
    ser3.flush()
    pos = 10
    delay = 0
    
    while True:

        if (delay > 2):
            pos += 10
            delay = 0

        if (pos > 119):
            pos = 10

        delay += 1

        # Conver number into byte
        # pos = 181
        byte = [pos]
        byteToTx = bytearray(byte)

        # Show verbose
        print("Tx'd: " + str(byteToTx))

        # Send and Recieve via UART2/3
        size = ser2.write(byteToTx)
        #byteFrRx = ser3.readline().decode('utf-8').rstrip()

        # Show verbose
        #print("Rx'd: " + str(size) + " with " + byteFrRx)

        # Pause for 1s
        time.sleep(1)