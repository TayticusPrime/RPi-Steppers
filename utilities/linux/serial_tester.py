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
    #Initialize arduino communication
    ar1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ar2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    time.sleep(2.0)

    request(ar1,1,1,523.25,0.0)
    request(ar2,1,1,523.25,0.0)
    request(ar1,2,1,659.25,0.0)
    request(ar2,2,1,659.25,0.0)
    request(ar1,3,1,783.99,0.0)
    request(ar2,3,1,783.99,0.0)
    request(ar1,4,1,1046.50,0.0)
    request(ar2,4,1,1046.50,0.0)

    time.sleep(5.0)

    request(ar1,1,3,0.0,0.0)
    request(ar2,1,3,0.0,0.0)

    '''
    DELAY = 0.33
    #Test first stepper bank (Arduino 1)
    request(ar1, 1, 2, 523.25, DELAY)
    time.sleep(DELAY)
    request(ar1, 2, 2, 659.25, DELAY)
    time.sleep(DELAY)
    request(ar1, 3, 2, 783.99, DELAY)
    time.sleep(DELAY)
    request(ar1, 4, 2, 1046.50, DELAY)
    time.sleep(DELAY)
    request(ar1, 3, 2, 783.99, DELAY)
    time.sleep(DELAY)
    request(ar1, 2, 2, 659.25, DELAY)
    time.sleep(DELAY)
    request(ar1, 1, 2, 523.25, DELAY)
    time.sleep(DELAY)

    time.sleep(0.5)

    #Test second stepper bank (Arduino 2)
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

    time.sleep(0.5)
    #Enable all
    request(ar1, 1, 1, 523.25, 0.0)
    time.sleep(DELAY)
    request(ar1, 2, 1, 659.25, 0.0)
    time.sleep(DELAY)
    request(ar1, 3, 1, 783.99, 0.0)
    time.sleep(DELAY)
    request(ar1, 4, 1, 1046.50, 0.0)
    time.sleep(DELAY)
    request(ar2, 1, 1, 523.25, 0.0)
    time.sleep(DELAY)
    request(ar2, 2, 1, 659.25, 0.0)
    time.sleep(DELAY)
    request(ar2, 3, 1, 783.99, 0.0)
    time.sleep(DELAY)
    request(ar2, 4, 1, 1046.50, 0.0)
    time.sleep(DELAY)

    time.sleep(2.0)

    #Deactivate all
    request(ar1, 1, 3, 0.0, DELAY)
    request(ar2, 1, 3, 0.0, DELAY)
    '''

if __name__ == '__main__':
    main()