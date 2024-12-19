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
        if self.index < len(self.track.notes) and timestamp >= self.track.notes[self.index].start:
            note = self.track.notes[self.index]
            self.arduino.send(self.stepper, 
                              PULSE, 
                              NOTES[note.pitch - 12], 
                              note.end - note.start)
            self.index += 1

class Player:
    def __init__(self, filename):
        self.controller = Arduino('/dev/ttyUSB0')
        self.loadMIDI(filename)

    def loadMIDI(self, filename):
        midi = pretty_midi.PrettyMIDI(filename)

        self.tracks = []
        for i, instrument in enumerate(midi.instruments):
            if i >= MAX_STEPPERS: break
            self.tracks.append(Track(instrument, self.controller, i+1))

    def run(self):
        start = time.time()
        while(True):
            timestamp = time.time() - start
            for track in self.tracks:
                track.update(timestamp)
            time.sleep(0.1)

def main():
    '''
    player = Player('song.mid')
    player.run()
    '''

    controller = Arduino('/dev/ttyUSB0')

    midi = pretty_midi.PrettyMIDI('song_1.mid')

    channel = midi.instruments[0]
    track_1 = Track(channel, controller, 1)
    channel = midi.instruments[1]
    track_2 = Track(channel, controller, 2)
    channel = midi.instruments[2]
    track_3 = Track(channel, controller, 3)
    channel = midi.instruments[3]
    track_4 = Track(channel, controller, 4)
    start = time.time()
    while(True):
        track_1.update(time.time() - start)
        track_2.update(time.time() - start)
        track_3.update(time.time() - start)
        track_4.update(time.time() - start)
        time.sleep(0.05)
    
    '''
    # Extract notes
    for i, instrument in enumerate(midi.instruments):
        print(f"Instrument {i}: {instrument.name}")
        for note in instrument.notes:
            print(f"Note: {note.pitch}, Start: {note.start}, End: {note.end}")
    '''

if __name__ == "__main__":
    main()
