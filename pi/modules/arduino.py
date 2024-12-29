#player.py

'''
Author: Tayte Waterman
Date: Dec 2024
About: The following script reads external MIDI files and translates up to 8 channels
of the contained content into serial commands to play via Arduino-controlled
stepper motors.
'''

#Dependencies
import serial
import struct
import time

#Constants
INIT_TIME = 2.0

#RequestMode Enum
OFF = 0
ON = 1
PULSE = 2
ALL_OFF = 3
STANDARD_MODE = 4
FLIP_FLOW_MODE = 5

class Arduino:
    def __init__(self, channel):
        print(f'Initializing Arduino on {channel}...')
        self.channel = channel
        self.arduino = serial.Serial(channel, 9600, timeout=1)
        time.sleep(INIT_TIME)

    def send(self, stepper, mode, frequency, duration):
        if (stepper<1 or stepper>4) or (mode<0 or mode>3) or frequency < 0 or duration < 0: return -1

        payload = struct.pack('B B f f', stepper, mode, frequency, duration)
        self.arduino.write(payload)
        return self.arduino.is_open
