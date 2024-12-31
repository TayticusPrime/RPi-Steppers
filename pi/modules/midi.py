#midi.py
'''
Author: Tayte Waterman
Date: Dec 2024
About: The following contains MIDI to arduino-stepper translation and playing. The main Player
class can be used to instantiate arduino-stepper objects and play supplied midi files over them
'''

#External Dependencies
import os
import sys
import time
import pretty_midi

#Internal Dependencies
MODULES_PATH = '.'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), MODULES_PATH)))
from arduino import Arduino
from arduino import STEPPERS_PER_CONTROLLER

#Constants
MAX_CONTROLLERS = 2
QUANTA = 0.05

NOTES = {
    'MIN': 21,
    21:  27.5000,  # A0
    22:  29.1352,  # A#0/Bb0
    23:  30.8677,  # B0
    24:  32.7032,  # C1
    25:  34.6478,  # C#1/Db1
    26:  36.7081,  # D1
    27:  38.8909,  # D#1/Eb1
    28:  41.2034,  # E1
    29:  43.6535,  # F1
    30:  46.2493,  # F#1/Gb1
    31:  48.9994,  # G1
    32:  51.9130,  # G#1/Ab1
    33:  55.0000,  # A1
    34:  58.2705,  # A#1/Bb1
    35:  61.7354,  # B1
    36:  65.4064,  # C2
    37:  69.2957,  # C#2/Db2
    38:  73.4162,  # D2
    39:  77.7817,  # D#2/Eb2
    40:  82.4069,  # E2
    41:  87.3071,  # F2
    42:  92.4986,  # F#2/Gb2
    43:  97.9989,  # G2
    44:  103.826,  # G#2/Ab2
    45:  110.000,  # A2
    46:  116.541,  # A#2/Bb2
    47:  123.471,  # B2
    48:  130.813,  # C3
    49:  138.591,  # C#3/Db3
    50:  146.832,  # D3
    51:  155.563,  # D#3/Eb3
    52:  164.814,  # E3
    53:  174.614,  # F3
    54:  184.997,  # F#3/Gb3
    55:  195.998,  # G3
    56:  207.652,  # G#3/Ab3
    57:  220.000,  # A3
    58:  233.082,  # A#3/Bb3
    59:  246.942,  # B3
    60:  261.626,  # C4 (Middle C)
    61:  277.183,  # C#4/Db4
    62:  293.665,  # D4
    63:  311.127,  # D#4/Eb4
    64:  329.628,  # E4
    65:  349.228,  # F4
    66:  369.994,  # F#4/Gb4
    67:  391.995,  # G4
    68:  415.305,  # G#4/Ab4
    69:  440.000,  # A4
    70:  466.164,  # A#4/Bb4
    71:  493.883,  # B4
    72:  523.251,  # C5
    73:  554.365,  # C#5/Db5
    74:  587.330,  # D5
    75:  622.254,  # D#5/Eb5
    76:  659.255,  # E5
    77:  698.456,  # F5
    78:  739.989,  # F#5/Gb5
    79:  783.991,  # G5
    80:  830.609,  # G#5/Ab5
    81:  880.000,  # A5
    82:  932.328,  # A#5/Bb5
    83:  987.767,  # B5
    84:  1046.50,  # C6
    85:  1108.73,  # C#6/Db6
    86:  1174.66,  # D6
    87:  1244.51,  # D#6/Eb6
    88:  1318.51,  # E6
    89:  1396.91,  # F6
    90:  1479.98,  # F#6/Gb6
    91:  1567.98,  # G6
    92:  1661.22,  # G#6/Ab6
    93:  1760.00,  # A6
    94:  1864.66,  # A#6/Bb6
    95:  1975.53,  # B6
    96:  2093.00,  # C7
    97:  2217.46,  # C#7/Db7
    98:  2349.32,  # D7
    99:  2489.02,  # D#7/Eb7
    100: 2637.02,  # E7
    101: 2793.83,  # F7
    102: 2959.96,  # F#7/Gb7
    103: 3135.96,  # G7
    104: 3322.44,  # G#7/Ab7
    105: 3520.00,  # A7
    106: 3729.31,  # A#7/Bb7
    107: 3951.07,  # B7
    108: 4186.01,  # C8
    'MAX': 108,
}

#Track class - manage a single "track" of notes assigned to a single arduino stepper
class Track:
    def __init__(self, notes, arduino, stepper):
        self.notes = notes
        self.arduino = arduino
        self.stepper = stepper

        self.index = 1

    def restart(self):
        self.index = 1
    
    def update(self, timestamp, keyshift=0, scalar=1.0):
        #Externally called. Update contents. provide external timestamp for real-time progression

        #If notes to be played, play them if the timestamp of the next note has arrived
        if self.index < len(self.notes):
            if timestamp >= self.notes[self.index].start * scalar:
                note = self.notes[self.index]
                pitch = note.pitch + keyshift
                if pitch >= NOTES['MIN'] and pitch <= NOTES['MAX']:
                    self.arduino.play_note( self.stepper,
                                            NOTES[pitch],
                                            (note.end - note.start) * scalar
                                            )
                self.index += 1
            
            #Flag that track is still playing (incomplete)
            return False

        else:
            #Flag that track is complete
            return True

class Player:
    def __init__(self, filename=None, ports=None):
        if ports == None: #Default usb ports
            self.controllers = [
                Arduino('/dev/ttyUSB0'),
                Arduino('/dev/ttyUSB1')
                ]
        else:
            self.controllers = [
                Arduino(ports[0]),
                Arduino(ports[1])
                ]
        if filename != None: self.loadMIDI(filename)

    def loadMIDI(self, filename, distributed=False):
        #Load midi from file and pre-process

        self.filename = filename
        midi = pretty_midi.PrettyMIDI(filename)

        self.tracks = []
        if not distributed:
            #Assign based on midi instrument assignment
            for index, instrument in enumerate(midi.instruments):
                if index >= MAX_CONTROLLERS * STEPPERS_PER_CONTROLLER: break
                i = index // STEPPERS_PER_CONTROLLER
                j = index % STEPPERS_PER_CONTROLLER
                self.tracks.append(Track(instrument.notes, self.controllers[i], j+1))
        
        else:
            #Distribute notes across all channels instead of midi assignment
            print('Resdistributing notes...')

            #Create a 'supertrack' of all notes combined into one list in order
            supertrack = []
            for i, instrument in enumerate(midi.instruments):
                supertrack += instrument.notes
            supertrack = sorted(supertrack, key=lambda x: x.start)
            
            #Iterate over notes and one-by-one assign notes to steppers in order. Wrap around
            #  to first stepper once the last stepper is reached
            tracks = [[] for x in range(MAX_CONTROLLERS * STEPPERS_PER_CONTROLLER)]
            i = 0
            for note in supertrack:
                #If a note is still being played find the next free stepper. If none can be
                #  found, overwrite original stepper
                temp = i
                while len(tracks[i]) != 0 and note.start < tracks[i][-1].end:
                    i += 1
                    if i >= MAX_CONTROLLERS * STEPPERS_PER_CONTROLLER: i = 0
                    if i == temp: break

                tracks[i].append(note)
            
            #Convert results to self.tracks
            for i in range(MAX_CONTROLLERS):
                for j in range(STEPPERS_PER_CONTROLLER):
                    k = i * STEPPERS_PER_CONTROLLER + j
                    self.tracks.append(Track(tracks[k], self.controllers[i], j+1))

    def run(self, loop=False, keyshift=0, timeshift=1.0):
        #Play contained midi (processed) song
        print(f'Playing file \"{self.filename}\"...')
        scalar = 1.0/timeshift

        #While song still active fetch real-time and call stepper update()
        while(True):
            #Restart in case previous song indices present
            for track in self.tracks:
                track.restart()

            #Fetch real-time from system, convert to relative song-time and update
            start = time.time()
            complete = False
            while(not complete):
                timestamp = time.time() - start
                complete = True
                for track in self.tracks:
                    status = track.update(timestamp, keyshift, scalar)
                    complete = complete and status
                time.sleep(QUANTA)  #Minimum iteration step (don't hog CPU)

            if not loop: break

        print(f'Completed \"{self.filename}!\"')
