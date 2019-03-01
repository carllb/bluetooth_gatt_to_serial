#!/usr/bin/env python3

import serial
import time

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

if( not ser.isOpen() ):
	print("Error")


num = 0xDEADBEEF
while True:
	print("Sending...")
	bts = (num).to_bytes(4, byteorder='little')
	ser.write(bts)
	time.sleep(1)
	num = num + 1
