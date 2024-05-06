#include "UART.h"

#define F_CPU 8000000UL /* Define frequency here its 8MHz */
// #define USART_BAUDRATE 9600
#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

void UART_init(long USART_BAUDRATE)
{
	UCSRB |= (1 << RXEN) | (1 << TXEN) | (1 << RXCIE);	 /* Turn on transmission and reception */
	UCSRC |= (1 << URSEL) | (1 << UCSZ0) | (1 << UCSZ1); /* Use 8-bit character sizes */
	UBRRL = BAUD_PRESCALE;								 /* Load lower 8-bits of the baud rate value */
	UBRRH = (BAUD_PRESCALE >> 8);						 /* Load upper 8-bits*/
	sei();
}

unsigned char UART_RxChar()
{
	while ((UCSRA & (1 << RXC)) == 0)
		;		  /* Wait till data is received */
	return (UDR); /* Return the byte*/
}

void UART_TxChar(char ch)
{
	while (!(UCSRA & (1 << UDRE)))
		; /* Wait for empty transmit buffer*/
	UDR = ch;
}

void UART_SendString(char *str)
{
	unsigned char j = 0;

	while (str[j] != 0) /* Send string till null */
	{
		UART_TxChar(str[j]);
		j++;
	}
}

void UART_TX_Float(float F_val)
{
	unsigned char *PTR = (unsigned char *)&F_val;
	for (unsigned char i = 0; i < sizeof(float) / sizeof(unsigned char); i++)
	{
		UART_TxChar(PTR[i]);
	}
}

void UART_TX_int(unsigned int unsignedint_val)
{
	unsigned char *PTR = (unsigned char *)&unsignedint_val;
	for (unsigned char i = 0; i < sizeof(unsigned int) / sizeof(unsigned char); i++)
	{
		UART_TxChar(PTR[i]);
	}
}