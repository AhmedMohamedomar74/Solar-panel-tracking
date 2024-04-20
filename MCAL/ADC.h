/*
 * ADC.h
 *
 *  Created on: 14Apr.,2024
 *      Author: ahmed
 */

#ifndef MCAL_ADC_H_
#define MCAL_ADC_H_

#include <avr/io.h>			/* Include AVR std. library file */
#include <stdio.h>			/* Include std. library file */
#include <util/delay.h>		/* Include Delay header file */




void ADC_INIT();
unsigned int ADC_READ(unsigned char channel_number);
#endif /* MCAL_ADC_H_ */
