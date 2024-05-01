#include "../MCAL/ADC.h"
#include "../MCAL/UART.h"

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

Measaure_t Measured_voltage(unsigned int adc_value);

int main() {
    ADC_INIT();
    UART_init(9600);
    unsigned char eight_bit_var = ADC_READ(2);
    Measaure_t Measure = Measured_voltage(eight_bit_var);
    while (1) {
        switch (UART_RxChar())
        {
        case 'R':
            UART_TX_Float(Measure.voltage_measument);
            UART_TX_Float(Measure.current_measument);
            UART_TX_Float(Measure.Power_measurment);
            break;
        
        default:
            break;
        }
    }
}

Measaure_t Measured_voltage(unsigned int adc_value) {
    Measaure_t temp;
    temp.voltage_measument = ((float)adc_value * Voltage_Reff / 1023.0) * (First_resistance + Second_resistance) / Second_resistance;
    temp.current_measument = temp.voltage_measument / (First_resistance + Second_resistance);
    temp.Power_measurment = temp.voltage_measument * temp.current_measument;
    return temp;
}
