/*
 * PWM.h
 *
 *  Created on: 14Apr.,2024
 *      Author: ahmed
 */

#ifndef PWM_H_
#define PWM_H_

#define F_CPU 8000000UL		/* Define CPU Frequency e.g. here its 8MHz */
#include <avr/io.h>			/* Include AVR std. library file */
#include <stdio.h>			/* Include std. library file */
#include <util/delay.h>		/* Include Delay header file */

void TIMER1_PWM_intit();
#endif /* PWM_H_ */
