//arduino.ino
/*
Author: Tayte Waterman
Date: Dec 2024
About: The following arduino sketch manages an arduino-stepper controller which takes serial
commands and translates them into specific frequencies used to play music over the steppers.
*/

#include "dispatcher.h"

#define FLIP_FLOP_MODE true

//Dispatcher object - contains and manages controller sub-objects
Dispatcher dispatcher;

void setup() {
  //Initialize serial connection
  Serial.begin(9600);
  while(!Serial) {}

  //Attach stepper controllers
  dispatcher.attachController(0, 13, 12, 11, FLIP_FLOP_MODE);
  dispatcher.attachController(1, 10, 9, 8, FLIP_FLOP_MODE);
  dispatcher.attachController(2, 7, 6, 5, FLIP_FLOP_MODE);
  dispatcher.attachController(3, 4, 3, 2, FLIP_FLOP_MODE);
}

void loop() {
  //Call dispatcher update
  dispatcher.update();
}
