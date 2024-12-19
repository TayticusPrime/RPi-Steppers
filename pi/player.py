import argparse
import serial
import struct
import time
import pretty_midi

from notes import NOTES

#Constants
INIT_TIME = 2.0
STEPPERS_PER_CONTROLLER = 4 
MAX_CONTROLLERS = 2
QUANTA = 0.05

#RequestMode Enum
OFF = 0
ON = 1
PULSE = 2
ALL_OFF = 3

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
    
class Track:
    def __init__(self, track, arduino, stepper):
        self.track = track
        self.arduino = arduino
        self.stepper = stepper

        self.index = 1

    def restart(self):
        self.index = 1
    
    def update(self, timestamp):
        if self.index < len(self.track.notes):
            if timestamp >= self.track.notes[self.index].start:
                note = self.track.notes[self.index]
                self.arduino.send(self.stepper, PULSE, NOTES[note.pitch - 12], note.end - note.start)
                self.index += 1
            return False

        else:
            return True

class Player:
    def __init__(self, filename):
        self.controllers = [
                Arduino('/dev/ttyUSB0'),
                Arduino('/dev/ttyUSB1')
                ]
        self.filename = filename
        self.loadMIDI(filename)

    def loadMIDI(self, filename):
        midi = pretty_midi.PrettyMIDI(filename)

        self.tracks = []
        for index, instrument in enumerate(midi.instruments):
            if index >= MAX_CONTROLLERS * STEPPERS_PER_CONTROLLER: break
            i = index // STEPPERS_PER_CONTROLLER
            j = index % STEPPERS_PER_CONTROLLER
            self.tracks.append(Track(instrument, self.controllers[i], j+1))

    def run(self, loop=False):
        print(f'Playing file \"{self.filename}\"...')

        while(True):
            for track in self.tracks:
                track.restart()

            start = time.time()
            complete = False
            while(not complete):
                timestamp = time.time() - start
                complete = True
                for track in self.tracks:
                    status = track.update(timestamp)
                    complete = complete and status
                time.sleep(QUANTA)

            if not loop: break

        print(f'Completed \"{self.filename}!\"')

def main():
    parser = argparse.ArgumentParser(description='Arduino stepper MIDI player')

    parser.add_argument('filename', help='Input MIDI file of type .mid')
    parser.add_argument('--loop', action='store_true', help='Continuously replay file')

    args = parser.parse_args()
    
    player = Player(args.filename)
    player.run(args.loop)

if __name__ == "__main__":
    main()
