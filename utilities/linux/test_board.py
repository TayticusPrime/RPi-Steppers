import json
import time

from ..pi.modules.arduino import Arduino
from ..pi.modules.midi import NOTES

#Constants
CONFIG = '../config.json'
DELAY = 0.5

def main():
    ports = None
    try:
        with open(CONFIG, 'r') as file:
            ports = json.load(file)['arduino']['ports']
    except:
        print(f'WARNING: Could not find \"{CONFIG}\". Using default configuraiton')

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
    ar2.play_note(1, NOTES[60], DELAY)
    time.sleep(DELAY)
    ar2.play_note(2, NOTES[62], DELAY)
    time.sleep(DELAY)
    ar2.play_note(3, NOTES[64], DELAY)
    time.sleep(DELAY)
    ar2.play_note(4, NOTES[65], DELAY)
    time.sleep(DELAY)

if __name__ == '__main__':
    main()
