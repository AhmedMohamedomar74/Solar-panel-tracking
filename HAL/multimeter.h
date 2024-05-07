/*
 * multimeter.h
 *
 *  Created on: 7May,2024
 *      Author: ahmed
 */

#ifndef HAL_MULTIMETER_H_
#define HAL_MULTIMETER_H_

#include "../MCAL/ADC.h"
#include "../MCAL/UART.h"

#define First_resistance 10000
#define Second_resistance 5000
#define Voltage_Reff 4.15

void multimeterInit();
void Send_Measurements();
#endif /* HAL_MULTIMETER_H_ */
