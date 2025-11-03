#2025, S.Diane, script for reading serial data from Arduino, ESP32, etc.

import sys, serial

ser = serial.Serial('COM3', 115200) # Replace with your port and baud rate
max_reads=100
max_errors=100
iter, ierr=0,0

while iter<max_reads and ierr<max_errors:
    try:
        data_raw = ser.readline()
        data_str = data_raw.decode('utf-8').strip(" ,\r\n")
        print(data_str)
        iter+=1
    except:
        print("Error while reading serial data")
        ierr+=1

ser.close()
