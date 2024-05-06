#include "../MCAL/UART.h"
#include "../MCAL/ADC.h"

#define First_resistance 10000
#define Second_resistance 5000
#define Voltage_Reff 4.15

unsigned char REC_var;

int main()
{
    UART_init(9600);
    ADC_INIT();
    while (1)
    {
        if (REC_var == 'A')
        {
            float voltage = ((float)ADC_READ(2) * Voltage_Reff / 1023.0) * (First_resistance + Second_resistance) / Second_resistance;
            UART_TX_Float(voltage);
            float current = voltage / (First_resistance + Second_resistance);
            UART_TX_Float(current);
            float Power = voltage * current;
            UART_TX_Float(Power);
            REC_var = 0;
        }
    }
}

ISR(USART_RXC_vect)
{
    REC_var = UDR;
}
