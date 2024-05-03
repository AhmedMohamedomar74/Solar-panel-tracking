/*
 * Ameter.h
 *
 *  Created on: 2May,2024
 *      Author: ahmed
 */

#ifndef HAL_AMETER_H_
#define HAL_AMETER_H_

#include "../MCAL/ADC.h"

#define F_CPU 8000000UL			/* Define frequency here its 8MHz */
//#define USART_BAUDRATE 9600


#define First_resistance 10000
#define Second_resistance 1000
#define Voltage_Reff 5

typedef struct measument {
    float voltage_measument;
    float current_measument;
    float Power_measurment;
} Measaure_t;

void Ameter_init();

Measaure_t Measured_voltage(unsigned int adc_channel);

#endif /* HAL_AMETER_H_ */
