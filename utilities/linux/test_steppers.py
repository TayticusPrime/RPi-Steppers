#test_steppers.py
'''
Author: Tayte Waterman
Date: Dec 2024
About: Test arduino-stepper hardware (Linux). Script exercises all steppers for two arduino
boards. For more granular control use Windows GUI in utilities/windows/
'''

#External dependencies
import os
import sys
import json
import time

#Internal dependencies
MODULES_PATH = '../../pi/modules'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), MODULES_PATH)))
from arduino import Arduino
from midi import NOTES

#Constants
CONFIG = '../../config.json'
DELAY = 0.2

def main():
    ports = None
    try:
        with open(CONFIG, 'r') as file:
            ports = json.load(file)['arduino']['ports']
    except:
        print(f'WARNING: Could not find \"{CONFIG}\". Using default configuration')
        ports = [
                '/dev/ttyUSB0',
                '/dev/ttyUSB1'
                ]

    ar1 = Arduino(ports[0])
    ar2 = Arduino(ports[1])

    #Bank 1
    ar1.play_note(1, NOTES[60], DELAY)
    time.sleep(DELAY)
    ar1.play_note(2, NOTES[62], DELAY)
    time.sleep(DELAY)
    ar1.play_note(3, NOTES[64], DELAY)
    time.sleep(DELAY)
    ar1.play_note(4, NOTES[65], DELAY)
    time.sleep(DELAY)

    #Bank 2
    ar2.play_note(1, NOTES[67], DELAY)
    time.sleep(DELAY)
    ar2.play_note(2, NOTES[69], DELAY)
    time.sleep(DELAY)
    ar2.play_note(3, NOTES[71], DELAY)
    time.sleep(DELAY)
    ar2.play_note(4, NOTES[72], DELAY)
    time.sleep(DELAY)

    #Decrement bank 2
    ar2.play_note(4, NOTES[72], DELAY)
    time.sleep(DELAY)
    ar2.play_note(3, NOTES[71], DELAY)
    time.sleep(DELAY)
    ar2.play_note(2, NOTES[69], DELAY)
    time.sleep(DELAY)
    ar2.play_note(1, NOTES[67], DELAY)
    time.sleep(DELAY)
    
    #Decrement bank 1
    ar1.play_note(4, NOTES[65], DELAY)
    time.sleep(DELAY)
    ar1.play_note(3, NOTES[64], DELAY)
    time.sleep(DELAY)
    ar1.play_note(2, NOTES[62], DELAY)
    time.sleep(DELAY)
    ar1.play_note(1, NOTES[60], DELAY)
    time.sleep(DELAY)

    #All steppers - Cmaj7(9,13)
    time.sleep(DELAY * 2)
    ar1.play_note(1, NOTES[48], DELAY * 10)
    ar1.play_note(2, NOTES[52], DELAY * 10)
    ar1.play_note(3, NOTES[55], DELAY * 10)
    ar1.play_note(4, NOTES[59], DELAY * 10)
    ar2.play_note(1, NOTES[62], DELAY * 10)
    ar2.play_note(2, NOTES[65], DELAY * 10)
    ar2.play_note(3, NOTES[69], DELAY * 10)
    ar2.play_note(4, NOTES[59], DELAY * 10)

if __name__ == '__main__':
    main()
