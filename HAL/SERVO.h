/*
 * SERVO.h
 *
 *  Created on: 14Apr.,2024
 *      Author: ahmed
 */

#ifndef HAL_SERVO_H_
#define HAL_SERVO_H_

#include "../MCAL/PWM.h"

void servo_int();
void servo_move (signed char angle);

#endif /* HAL_SERVO_H_ */
