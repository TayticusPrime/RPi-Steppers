import serial
import struct
import time

#RequestMode enum
OFF = 0
ON = 1
PULSE = 2
ALL_OFF = 3

def request(arduino, pin, mode, frequency, duration):
    data = struct.pack('B B f f', pin, mode, frequency, duration)
    arduino.write(data)

def main():
    ar1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ar2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    time.sleep(2.0)

    DELAY = 0.5
    request(ar1, 1, 2, 261.63, DELAY)
    time.sleep(DELAY)
    request(ar1, 2, 2, 329.63, DELAY)
    time.sleep(DELAY)
    request(ar1, 3, 2, 392.00, DELAY)
    time.sleep(DELAY)
    request(ar1, 4, 2, 523.25, DELAY)
    time.sleep(DELAY)
    request(ar1, 3, 2, 392.00, DELAY)
    time.sleep(DELAY)
    request(ar1, 2, 2, 329.63, DELAY)
    time.sleep(DELAY)
    request(ar1, 1, 2, 261.63, DELAY)
    time.sleep(DELAY)

    request(ar2, 1, 2, 523.25, DELAY)
    time.sleep(DELAY)
    request(ar2, 2, 2, 659.25, DELAY)
    time.sleep(DELAY)
    request(ar2, 3, 2, 783.99, DELAY)
    time.sleep(DELAY)
    request(ar2, 4, 2, 1046.50, DELAY)
    time.sleep(DELAY)
    request(ar2, 3, 2, 783.99, DELAY)
    time.sleep(DELAY)
    request(ar2, 2, 2, 659.25, DELAY)
    time.sleep(DELAY)
    request(ar2, 1, 2, 523.25, DELAY)
    time.sleep(DELAY)

if __name__ == '__main__':
    main()
