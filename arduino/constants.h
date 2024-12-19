//constants.h
/*
Author: Tayte Waterman
Date: Dec 2024
About: Used for shared constants; primarily real-time control
*/

#ifndef _CONSTANTS_H_
#define _CONSTANTS_H_

#define QUANTA 50         //Minimum time-step of clock (micro-seconds)
#define CALIBRATE_M 0.8f  //Clock scaling (percent). Used to speed/lag clock if not in real-time.
                          //  Real-Time = CALIBRATE_M * Board-Percieved-Time
#define BALANCE 7         //Delay inactive loops to balance active/inactive time. Else, pitch
                          //  will change as steppers are active.

#endif //_CONSTANTS_H_
