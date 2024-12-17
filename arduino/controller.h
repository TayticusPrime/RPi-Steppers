//controller.h
/*
Author: Tayte Waterman
Date: Dec 2024
About: The Controller class is used to controll stepper motors for the purpose
of musical note creation. The class contains methods for setting the motors to
specific input frequencies, for specific durations, executed in real-time.
*/

#ifndef _CONTROLLER_H_
#define _CONTROLLER_H_

//Includes
#include <stdint.h>

class Controller {
  public:
    //Constructor/Destructor
    Controller(uint8_t step_pin, uint8_t dir_pin);
    virtual ~Controller();

    //Activate stepper for a finite time
    void pulse(float freq, float duration);
    //Change the persistent stepper state
    void changeState(bool state, float freq);
    //Increment in real-time
    void update();
    //Turn off stepper and reset direction
    void turnOff();
    
  private:
    //Pins
    uint8_t _step_pin;  //Pin for step control
    uint8_t _dir_pin;   //Pin for direction control

    //Clock and limited duration activation
    bool _active;         //Flag - whether stepper active or not
    uint32_t _clock;      //Clock - activation duration
    uint32_t _end;        //End time (for finite pulse)

    //Step control
    uint32_t _sub_clock;  //Clock - step waveform
    uint32_t _sub_mid;    //Waveform midpoint
    uint32_t _sub_end;    //Waveform end
    bool _step_active;    //Step active
    bool _pulse;          //Flag - finite activation

    //Direction control
    uint8_t changeDirection();  //Change direction
    uint8_t _direction;         //Current direction
};

#endif //_CONTROLLER_H_
