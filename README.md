# RPi-Steppers

## About
The following repository contains code for a stepper-based music player. The player takes input music files (MIDI format) and translates them into stepper control values which mimic the target music notes (frequency). It is designed to work with an 8-channel (stepper) setup via Arduino Nano devices as the stepper controller, with MIDI reading and overall control from a Raspberry Pi (5) device.

![PXL_20241231_134127112](https://github.com/user-attachments/assets/0863266c-4b3e-4b67-b3c8-698e7af5bd5e)


The following code-base contains the target Arduino (Nano) code, Raspberry Pi code, and testing utilities (both from Linux and Windows) for hardware troubleshooting purposes

## Video Demos
[Tetris Theme (“Korobeiniki”)](https://youtu.be/e9bMyeX0_78)
[Bonetrousle (Toby Fox)](https://youtu.be/AKarNMXLM8k)
[Pokémon Trainer Battle Theme (Gen 1) (Junichi Masuda)](https://youtu.be/eGSxeZ7RHHc)

## Usage
### MIDI Player
Execution of the MIDI-to-Stepper main script can be found in `pi/player.py`. To use, call the script via `python player -[args] [MIDI file]`. Supported arguments are listed below, but can also be found via `-h` or `--help`:
* `--distributed` - Distribute notes across all steppers. If not selected, stepper assignment will be based on the native MIDI "instrument" assignment. Example: `python player.py --distributed MIDI/song.mid`
* `--loop` - Replay once complete. If not selected, script will terminate once song is complete. Example: `python player.py --loop MIDI/song.mid`
* `-k` - keyshift. Shift the song by the input value of keys. Recommended k = -12. Example: `python player.py -k -12 MIDI/song.mid`
* `-t` - timeshift. Speed-up/Slow-down the input MIDI by the provided value. Example: `python player.py -t 1.5 MIDI/song.mid`

### Arduino Build/Deploy
The target Arduino (Nano) contents can be found in `arduino/`. To build and deploy the contents execute `./deploy.sh` from the `arduino/` folder. This toolchain depends on `arduino-cli` with `avr` installed to run. It connects to Arduino boards connected over USB via the USB-ports defined in the root `config.json` file

### Testing
Testing of the board (for hardware troubleshooting) can be found in the `utilities/` folder. Here there are two sub-folders. `linux/` contains a python script for exercising all stepper oututs to confirm basic serial-connection and hardware setup. `windows/` contains a python script/GUI for explicit control of (a single) Arduino board to test specific serial commands/methods to the board.

## Hardware

### Circuit Diagram
![image](https://github.com/user-attachments/assets/7db0d3f4-e941-40dd-85a3-b9aaf09fa1be)


### Components
* Qty 1 - Raspberry Pi 5 - Main control board for MIDI player and Arduino build/deployment
* Qty 2 - Arduino Nano - Stepper controller board; 4 steppers per board
* Qty 8 - A4988 Stepper Driver Board (https://www.amazon.de/dp/B0CD756ZCC?ref=ppx_yo2ov_dt_b_fed_asin_title)
* Qty 8 - Stepper Motor (GEEETECH 3D Printer Motor https://www.amazon.de/dp/B0CCS1JCYL?ref=ppx_yo2ov_dt_b_fed_asin_title)
* Qty 8 - 100 uF Capacitor - Stepper motor supply (Protect rest of project from motor voltage spikes)

Variable Power-Supply: 12VDC @ 750mA
