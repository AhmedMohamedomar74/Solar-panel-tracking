#include "multimeter.h"

void multimeterInit()
{
    ADC_INIT();
}

void Send_Measurements()
{
    float voltage = ((float)ADC_READ(2) * Voltage_Reff / 1023.0) * (First_resistance + Second_resistance) / Second_resistance;
    UART_TX_Float(voltage);
    float current = voltage / (First_resistance + Second_resistance);
    UART_TX_Float(current);
    float Power = voltage * current;
    UART_TX_Float(Power);
}
