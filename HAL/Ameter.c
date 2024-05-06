#include "Ameter.h"

void Ameter_init()
{
    ADC_INIT();
}

Measaure_t Measured_voltage(unsigned int adc_channel)
{
    unsigned char adc_value = ADC_READ(adc_channel);
    Measaure_t temp;
    temp.voltage_measument = ((float)adc_value * 4.15 / 1023.0) * (First_resistance + Second_resistance) / Second_resistance;
    temp.current_measument = temp.voltage_measument / (First_resistance + Second_resistance);
    temp.Power_measurment = temp.voltage_measument * temp.current_measument;
    return temp;
}
