import serial
import struct
import time
import pretty_midi

from notes import NOTES

#Constants
INIT_TIME = 2.0
MAX_STEPPERS = 4

#RequestMode Enum
OFF = 0
ON = 1
PULSE = 2
ALL_OFF = 3

class Arduino:
    def __init__(self, channel):
        print(f'Initializing communication to Arduino on {channel}...')
        self.channel = channel
        self.arduino = serial.Serial(channel, 9600, timeout=1)
        time.sleep(INIT_TIME)

    def send(self, stepper, mode, frequency, duration):
        if (stepper<1 or stepper>4) or (mode<0 or mode>3) or frequency < 0 or duration < 0: return -1

        payload = struct.pack('B B f f', stepper, mode, frequency, duration)
        self.arduino.write(payload)
        return self.arduino.is_open
    
    def read(self):
        if self.arduino.in_waiting > 0:
            return self.arduino.read(self.arduino.in_waiting)

class Track:
    def __init__(self, track, arduino, stepper):
        self.track = track
        self.arduino = arduino
        self.stepper = stepper

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
        self.controller = Arduino('/dev/ttyUSB0')
        self.filename = filename
        self.loadMIDI(filename)

    def loadMIDI(self, filename):
        midi = pretty_midi.PrettyMIDI(filename)

        self.tracks = []
        for i, instrument in enumerate(midi.instruments):
            if i >= MAX_STEPPERS: break
            self.tracks.append(Track(instrument, self.controller, i+1))

    def run(self):
        print(f'Playing file \"{self.filename}\"...')

        start = time.time()
        complete = False
        while(not complete):
            timestamp = time.time() - start
            complete = True
            for track in self.tracks:
                status = track.update(timestamp)
                complete = complete and status
            time.sleep(0.05)

        print(f'Completed \"{self.filename}!\"')

def main():
    player = Player('song_1.mid')
    player.run()

if __name__ == "__main__":
    main()
