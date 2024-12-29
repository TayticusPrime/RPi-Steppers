#player.py

'''
Author: Tayte Waterman
Date: Dec 2024
About: The following script reads external MIDI files and translates up to 8 channels
of the contained content into serial commands to play via Arduino-controlled
stepper motors.
'''

#External Dependencies
import argparse
import json

#Internal Dependencies
from modules.midi import Player

#Constants
CONFIG = '../config.json'

def main():
    parser = argparse.ArgumentParser(description='Arduino stepper MIDI player')

    parser.add_argument('filename', help='Input MIDI file of type .mid')
    parser.add_argument('--loop', action='store_true', help='Continuously replay file')
    parser.add_argument('--distributed', action='store_true', help='Distribute midi notes across steppers')
    parser.add_argument('-k', type=int, help='Number of notes to keyshift the original MIDI file by. Default=-12', default=0)
    parser.add_argument('-t', type=float, help='Scalar for speeding-up/slowing-down track', default=1.0)
    args = parser.parse_args()

    ports = None
    try:
        with open(CONFIG, 'r') as file:
            ports = json.load(file)['arduino']['ports']
    except:
        print(f'WARNING: Could not find \"{CONFIG}\". Using default configuraiton')
    
    player = Player(ports=ports)
    player.loadMIDI(args.filename, distributed=args.distributed)
    player.run(loop=args.loop, keyshift=args.k, timeshift=args.t)

if __name__ == "__main__":
    main()
