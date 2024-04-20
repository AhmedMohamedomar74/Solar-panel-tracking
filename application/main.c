// #include "../HAL/SERVO.h"
// #include "../MCAL/ADC.h"

// #define First_resistance 100000
// #define Second_resistance 10000

// int main()
// {
//     signed char angle_value = 0;
//     servo_int();
//     ADC_INIT();
//     servo_move(angle_value);
//     int tol = 50;
//     while (1)
//     {
    	
//         // unsigned int Read_lift = ADC_READ(0);
//         // unsigned int Read_right = ADC_READ(1);
//         // int differance_H = Read_lift - Read_right;
//         // if ((differance_H > tol) || (differance_H < (-1 * tol)))
//         // {
//         //    if (Read_lift > Read_right)
//         //    {
//         //         angle_value = ++angle_value;
//         //         if (angle_value > 90)
//         //         {
//         //             angle_value = 90;

//         //         }
                
//         //    }
//         //    else if (Read_lift < Read_right)
//         //    {
//         //         angle_value = --angle_value;
//         //         if (angle_value < -90)
//         //         {
//         //             angle_value = -90;
                    
//         //         }
                
//         //    }
//         //    servo_move(angle_value);
//         // }
//         unsigned int Read_adc_value = ADC_READ(2);
//         float Read_adc_voltage_value = (1023 / 5) * Read_adc_value;
//         float Voltage_measurment = (Read_adc_value / Second_resistance)  * (Second_resistance + First_resistance);
//     }

// }
#include "../MCAL/ADC.h"

#define F_CPU 8000000UL			/* Define frequency here its 8MHz */
//#define USART_BAUDRATE 9600
#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

#define First_resistance 100000
#define Second_resistance 10000
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
    while (1) {
        Measaure_t Measure = Measured_voltage(ADC_READ(2));
        UART_TxChar(Measure.voltage_measument);
    }
}

Measaure_t Measured_voltage(unsigned int adc_value) {
    Measaure_t temp;
    temp.voltage_measument = ((float)adc_value * Voltage_Reff / 1023.0) * (First_resistance + Second_resistance) / Second_resistance;
    temp.current_measument = temp.voltage_measument / (First_resistance + Second_resistance);
    temp.Power_measurment = temp.voltage_measument * temp.current_measument;
    return temp;
}



void UART_init(long USART_BAUDRATE)
{
	UCSRB |= (1 << RXEN) | (1 << TXEN);/* Turn on transmission and reception */
	UCSRC |= (1 << URSEL) | (1 << UCSZ0) | (1 << UCSZ1);/* Use 8-bit character sizes */
	UBRRL = BAUD_PRESCALE;		/* Load lower 8-bits of the baud rate value */
	UBRRH = (BAUD_PRESCALE >> 8);	/* Load upper 8-bits*/
}

unsigned char UART_RxChar()
{
	while ((UCSRA & (1 << RXC)) == 0);/* Wait till data is received */
	return(UDR);			/* Return the byte*/
}

void UART_TxChar(char ch)
{
	while (! (UCSRA & (1<<UDRE)));	/* Wait for empty transmit buffer*/
	UDR = ch ;
}
