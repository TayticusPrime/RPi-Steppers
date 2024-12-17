#include "dispatcher.h"

//Dispatcher object - contains and manages controller sub-objects
Dispatcher dispatcher;

void setup() {
  //Initialize serial connection
  Serial.begin(9600);
  while(!Serial) {}

  //Attach stepper controllers
  dispatcher.attachController(0, 12, 11);
  dispatcher.attachController(1, 10, 9);
  dispatcher.attachController(2, 8, 7);
  dispatcher.attachController(3, 6, 5);
}

void loop() {
  //Call dispatcher update
  dispatcher.update();
}
