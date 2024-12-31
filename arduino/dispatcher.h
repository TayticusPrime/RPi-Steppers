//dispatcher.h
/*
Author: Tayte Waterman
Date: Dec 2024
About: the Dispatcher class is used to contain and manage stepper-controller objects.
It takes and translated values from serial data and translates it into stepper
commands, as well as manages real-time execution of the contained steppers.

Description of serial commands:
  Args:
    stepper (uint8_t) - which stepper to control (1-MAX_STEPPER)
    mode (Enum) - what operation to execute (see below)
    frequency (Hz) - what frequency to play
    duration (s) - how long to play note

  Mode dependencies:
    MODE            | MANDATORY ARGS                | IGNORED ARGS
    ----------------|-------------------------------|-----------------------------
    OFF             | stepper                       | frequency, duration
    ON              | stepper                       | frequency, duration
    PULSE           | stepper, frequency, duration  | (none)
    ALL_OFF         | (none)                        | stepper, frequency, duration
    STANDARD_MODE   | (none)                        | stepper, frequency, duration
    FLIP_FLOP_MODE  | (nont)                        | stepper, frequency, duration

  Serialization:
                  [ byte0 ] [ byte1 ] [ byte2 ] [ byte3 ]
                 ----------------------------------------
    bytes(0-3)  | [stepper] [ mode  ] [    RESERVED     ]
    bytes(4-7)  | [              frequency              ]
    bytes(8-11) | [              duration               ]
*/

#ifndef _DISPATCHER_H_
#define _DISPATCHER_H_

//Includes
#include <stdint.h>
#include "controller.h"

//Constants
#define POLL_TIME 0.005f      //Seconds
#define MAX_CONTROLLERS 4
#define REQUEST_LENGTH 12   //Length of serial request payload

//Mode (in request) enumeration values
enum RequestMode: uint8_t {
  OFF = 0,            //Turn off specific stepper
  ON = 1,             //Turn on specific stepper (indefinitely)
  PULSE = 2,          //Turn on specific stepper for finite duration
  ALL_OFF = 3,        //Turn off all steppers
  STANDARD_MODE = 4,  //(Persistent mode) Keep stepper always moving in one direction
  FLIP_FLOP_MODE = 5  //(Persistent mode) Switch stepper direction with each new note
};

//Struct of serial request
struct Request {
  uint8_t stepper_id;
  RequestMode mode;
  uint16_t res;
  float frequency;
  float duration;
};

//Union to support serial-to-struct translation
union RequestUnion {
  Request request;
  uint8_t buffer[REQUEST_LENGTH];
};

class Dispatcher {
  public:
    //Constructor/Destructors
    Dispatcher();
    ~Dispatcher();

    //Create a controller object and attach it
    void attachController(uint8_t id, uint8_t step_pin, uint8_t dir_pin, uint8_t enbl_pin); //flip_flop_mode = false
    void attachController(uint8_t id, uint8_t step_pin, uint8_t dir_pin, uint8_t enbl_pin, bool flip_flop_mode);
    //Increment in real-time
    void update();
    //Set reverse or always forward mode
    void setReverseMode(bool state);
    //Turn off all steppers
    void allOff();
    
  private:
    Controller* _controllers[MAX_CONTROLLERS];  //Steppers
    uint16_t _poll;   //Serial polling time-event
    uint16_t _clock;  //Clock
};

#endif //_DISPATCHER_H_
