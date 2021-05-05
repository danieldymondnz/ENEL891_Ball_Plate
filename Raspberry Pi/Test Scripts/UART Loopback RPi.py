#!/usr/bin/env python3
""" 
    Python UART Loopback Test Script
    Ball Plate Project 2021

 """
import serial
import time
if __name__ == '__main__':
    ser2 = serial.Serial('/dev/ttyAMA1', 9600, timeout=1)
    ser3 = serial.Serial('/dev/ttyAMA2', 9600, timeout=1)
    ser2.flush()
    ser3.flush()
    num = 0
    
    while True:
        
        print("Tx'd: " + "Test")
        ser2.write(b'Test')
        rxLine = ser3.readline().decode('utf-8').rstrip()
        print("Rx'd: " + rxLine)
        time.sleep(1)
        num += 1