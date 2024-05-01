#define F_CPU 8000000UL /* Define CPU Frequency e.g. here its 8MHz */
#include <avr/io.h>     /* Include AVR std. library file */
#include <avr/interrupt.h>
#include <stdio.h>      /* Include std. library file */
#include <util/delay.h> /* Include Delay header file */

#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

void UART_init(long USART_BAUDRATE);
unsigned char UART_RxChar();
void UART_TxChar(char ch);
void UART_TX_Float(float F_val);


extern unsigned char REC_char;
