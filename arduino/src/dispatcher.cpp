//dispatcher.cpp

//References
#include "include/dispatcher.h"
#include "include/constants.h"
#include <Arduino.h>

//Constructor
Dispatcher::Dispatcher() {
  pinMode(11, OUTPUT);
  _poll = 1000000 * POLL_TIME / QUANTA;
  _clock = _poll;
  for(int i=0; i<MAX_CONTROLLERS; ++i) {
    _controllers[i] = NULL;
  }
}

//Destructor
Dispatcher::~Dispatcher() {
  for(int i=0; i<MAX_CONTROLLERS; ++i) {
    if(_controllers[i]) {
      delete _controllers[i];
      _controllers[i] = NULL;
    }
  }
}

//Create and attache stepper-controller object
void Dispatcher::attachController(uint8_t id, uint8_t step_pin, uint8_t dir_pin, uint8_t enbl_pin) {
  attachController(id, step_pin, dir_pin, enbl_pin, false);
}
void Dispatcher::attachController(uint8_t id, uint8_t step_pin, uint8_t dir_pin, uint8_t enbl_pin, bool flip_flop_mode) {
  if(_controllers[id]) delete _controllers[id];
  _controllers[id] = new Controller(step_pin, dir_pin, enbl_pin, flip_flop_mode);
}

//Update - call this cyclically to update contents in real-time
void Dispatcher::update() {
  if(_clock == _poll) {
    if (Serial.available() >= REQUEST_LENGTH) {
      RequestUnion rqUnion;
      Serial.readBytes(rqUnion.buffer, REQUEST_LENGTH);

      --rqUnion.request.stepper_id;
      if(rqUnion.request.stepper_id < MAX_CONTROLLERS && _controllers[rqUnion.request.stepper_id]) {
        switch(rqUnion.request.mode) {
          case(RequestMode::PULSE):
            _controllers[rqUnion.request.stepper_id]->pulse(rqUnion.request.frequency, rqUnion.request.duration);
            break;
          case(RequestMode::ON):
            _controllers[rqUnion.request.stepper_id]->changeState(true, rqUnion.request.frequency);
            break;
          case(RequestMode::OFF):
            _controllers[rqUnion.request.stepper_id]->changeState(false, rqUnion.request.frequency);
            break;
          case(RequestMode::STANDARD_MODE):
            setReverseMode(false);
            break;
          case(RequestMode::FLIP_FLOP_MODE):
            setReverseMode(true);
            break;
          case(RequestMode::ALL_OFF):
          default:
            allOff();
            break;
        }
      }
    }

    _clock = 0;
  }
  else {
    ++_clock;
  }

  for(int i=0; i<MAX_CONTROLLERS; ++i) {
    if(_controllers[i]) _controllers[i]->update();
  }

  delayMicroseconds(QUANTA);
}

//Set reverse mode for all steppers
void Dispatcher::setReverseMode(bool state) {
  for(int i=0; i<MAX_CONTROLLERS; ++i) {
    if(_controllers[i]) _controllers[i]->setReverseMode(state);
  }
}

//Turn off all steppers and reset direction
void Dispatcher::allOff() {
  for(int i=0; i<MAX_CONTROLLERS; ++i) {
    if(_controllers[i]) _controllers[i]->turnOff();
  }
}
