#player.py
'''
Author: Tayte Waterman
Date: Dec 2024
About: The following script reads external MIDI files and translates up to 8 channels
of the contained content into serial commands to play via Arduino-controlled
stepper motors. See help (--help or -h) for more details
'''

#External Dependencies
import os
import sys
import argparse
import json

#Internal Dependencies
MODULES_PATH = './modules'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), MODULES_PATH)))
from arduino import Arduino
from midi import Player
from midi import NOTES

#Constants
CONFIG = '../config.json'

def main():
    #Help and argument parsing definition:
    parser = argparse.ArgumentParser(description='Arduino stepper MIDI player')

    parser.add_argument('filename', help='Input MIDI file of type .mid')
    parser.add_argument('--loop', action='store_true', help='Continuously replay file')
    parser.add_argument('--distributed', action='store_true', help='Distribute midi notes across steppers')
    parser.add_argument('-k', type=int, help='Number of notes to keyshift the original MIDI file by. Default=-12', default=0)
    parser.add_argument('-t', type=float, help='Scalar for speeding-up/slowing-down track', default=1.0)
    args = parser.parse_args()

    #Extract arduino config information from external file
    ports = None
    try:
        with open(CONFIG, 'r') as file:
            ports = json.load(file)['arduino']['ports']
    except:
        print(f'WARNING: Could not find \"{CONFIG}\". Using default configuration')
    
    #Instantiate Player, load midi, and play including provided terminal arguments
    player = Player(ports=ports)
    player.loadMIDI(args.filename, distributed=args.distributed)
    player.run(loop=args.loop, keyshift=args.k, timeshift=args.t)

if __name__ == "__main__":
    main()
