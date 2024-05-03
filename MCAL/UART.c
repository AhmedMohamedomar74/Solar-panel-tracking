#include "UART.h"

unsigned char Rec_arr[3] = {0, 0, 0};

void UART_init(long USART_BAUDRATE)
{
    UCSRB |= (1 << RXEN) | (1 << TXEN) | (1 << RXCIE);   /* Turn on transmission and reception */
    UCSRC |= (1 << URSEL) | (1 << UCSZ0) | (1 << UCSZ1); /* Use 8-bit character sizes */
    UBRRL = BAUD_PRESCALE;                               /* Load lower 8-bits of the baud rate value */
    UBRRH = (BAUD_PRESCALE >> 8);                        /* Load upper 8-bits*/
    sei();                                               /*Enable all interrupts */
}

unsigned char UART_RxChar()
{
    while ((UCSRA & (1 << RXC)) == 0)
        ;         /* Wait till data is received */
    return (UDR); /* Return the byte*/
}

void UART_TxChar(char ch)
{
    while (!(UCSRA & (1 << UDRE)))
        ; /* Wait for empty transmit buffer*/
    UDR = ch;
}

void UART_TX_Float(float F_val)
{
    unsigned char *PTR = (unsigned char *)&F_val;
    for (unsigned char i = 0; i < sizeof(float) / sizeof(unsigned char); i++)
    {
        UART_TxChar(PTR[i]);
        // _delay_ms(1000);
    }
}

ISR(USART_RXC_vect)
{
    static unsigned char counter = 0; // Now 'counter' is local to this ISR

    if (counter < 3)
    {
        Rec_arr[counter] = UDR;
        counter++;
    }
    else
    {
        counter = 0; // Reset counter after 3rd byte
    }
}
