//controller.cpp

//Includes
#include "controller.h"
#include "constants.h"
#include <Arduino.h>

//Constructors
Controller::Controller(uint8_t step_pin, uint8_t dir_pin, uint8_t enbl_pin) {
  Controller(step_pin, dir_pin, enbl_pin, false);
}

Controller::Controller(uint8_t step_pin, uint8_t dir_pin, uint8_t enbl_pin, bool flip_flop_mode):
  _step_pin(step_pin), _dir_pin(dir_pin), _enbl_pin(enbl_pin), _flip_flop_mode(flip_flop_mode) {
  _clock = 0;
  _active = false;
  _clock = 0;
  _end = 0;
  _direction = DEFAULT_DIRECTION;

  pinMode(_enbl_pin, OUTPUT);
  digitalWrite(enbl_pin, HIGH);
  pinMode(_step_pin, OUTPUT);
  digitalWrite(_step_pin, LOW);
  pinMode(_dir_pin, OUTPUT);
  digitalWrite(_dir_pin, LOW);
}

//Destructor
Controller::~Controller() {
  //Purposefully left empty (nothing to destruct)
}

//Active stepper at freq (Hz) for duration (sec)
void Controller::pulse(float freq, float duration) {
  //Set mode and compute clock values
  _pulse = true;
  _clock = 0;
  _end = (uint32_t)((1000000 * duration) * CALIBRATE_M);
  _active = true;

  _sub_clock = 0;
  _sub_end = (uint32_t)((1000000 / freq) * CALIBRATE_M);
  _sub_mid = (uint32_t)(_sub_end / 2);

  //Enable stepper chip
  digitalWrite(_enbl_pin, LOW);

  //Change direction with each activation
  if(_flip_flop_mode) digitalWrite(_dir_pin, changeDirection());

  //Init step pin to active
  digitalWrite(_step_pin, HIGH);
  _step_active = true;
}

//Change pin state and retain state. state=true ON, state=false OFF @ frequency (Hz)
void Controller::changeState(bool state, float freq) {
  _pulse = false;
  _active = state;
  
  if(_active) {
    //If active, set clock values
    _clock = 0;
    _end = 1;
  
    _sub_clock = 0;
    _sub_end = (uint32_t)((1000000 / freq) * CALIBRATE_M);
    _sub_mid = (uint32_t)(_sub_end / 2);

    //Enable stepper chip
    digitalWrite(_enbl_pin, LOW);

    //Change direction on activation
    if(_flip_flop_mode) digitalWrite(_dir_pin, changeDirection());

    digitalWrite(_step_pin, HIGH);
    _step_active = true; 
  }
  else {
    //If inactive, turn off pins
    digitalWrite(_enbl_pin, HIGH);
    digitalWrite(_step_pin, LOW);
    digitalWrite(_dir_pin, LOW);
  }
}

//Update contents in real-time
void Controller::update() {
  if(_active) {
    //If active update clock and assess. Only if active
    if(_clock < _end) {
      //Step midpoint
      if(_step_active && _sub_clock >= _sub_mid) {
        digitalWrite(_step_pin, LOW);
        _step_active = false;
      }
      //Step end/new-step (start here)
      else if(!_step_active && _sub_clock >= _sub_end) {
        digitalWrite(_step_pin, HIGH);
        _step_active = true;
        _sub_clock = 0;
      }
      //Update clocks
      _sub_clock += QUANTA;          
      if(_pulse) _clock += QUANTA; //Only update if in finite pulse mode
    }
    else {
      digitalWrite(_enbl_pin, HIGH);
      digitalWrite(_step_pin, LOW);
      digitalWrite(_dir_pin, LOW);
      _active = false;
    }
  }
  else {
    delayMicroseconds(BALANCE);
  }
}

//Change current stepper direction and return new state
uint8_t Controller::changeDirection() {
  if(_direction == LOW) {
    _direction = HIGH;
  }
  else {
    _direction = LOW;
  }
  return _direction;
}

//Set reverse mode state (setter)
void Controller::setReverseMode(bool state) {
  _direction = DEFAULT_DIRECTION;
  _flip_flop_mode = state;
}

//Turn off stepper and reset direction
void Controller::turnOff() {
  digitalWrite(_enbl_pin, HIGH);
  digitalWrite(_step_pin, LOW);
  digitalWrite(_dir_pin, LOW);
  _active = false;
}
