#arduino.py
'''
Author: Tayte Waterman
Date: Dec 2024
About: The following contains the Arduino class used to manage arduino-stepper communication and
control.
'''

#Dependencies
import serial
import struct
import time

#Constants
STEPPERS_PER_CONTROLLER = 4
INIT_TIME = 2.0

#RequestMode Enum
OFF = 0
ON = 1
PULSE = 2
ALL_OFF = 3
STANDARD_MODE = 4
FLIP_FLOP_MODE = 5

class Arduino:
    def __init__(self, channel):
        print(f'Initializing Arduino on {channel}...')
        self.channel = channel
        self.arduino = serial.Serial(channel, 9600, timeout=1)
        time.sleep(INIT_TIME)

    def serialize(self, stepper, mode, frequency, duration):
        #Serialize arguments and send to arduino
        payload = struct.pack('B B f f', stepper, mode, frequency, duration)
        self.arduino.write(payload)
        return self.arduino.is_open

    def play_note(self, stepper, frequency, duration=None):
        #Play a single note for duration (sec). If duration not provided, play indefinitely

        if (stepper<1 or stepper>STEPPERS_PER_CONTROLLER) or frequency < 0 or duration < 0: return -1

        mode = PULSE
        if(duration == None): mode = ON

        return self.serialize(stepper, mode, frequency, duration)
    
    def turn_off(self, stepper=None):
        #Turn off provided stepper. If stepper not provided, turn off all steppers

        if stepper != None and (stepper<1 or stepper>STEPPERS_PER_CONTROLLER): return -1

        if stepper != None:
            return self.serialize(stepper, OFF, 0.0, 0.0)
        else:
            return self.serialize(1, ALL_OFF, 0.0, 0.0)
    
    def flip_flop_mode(self, state):
        #Set flip-flop mode (whether motor should change direction with each note or not)

        mode = STANDARD_MODE
        if state: mode = FLIP_FLOP_MODE

        return self.serialize(1, mode, 0.0, 0.0)
