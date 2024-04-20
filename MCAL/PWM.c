#include "PWM.h"

void TIMER1_PWM_intit()
{
    DDRD |= (1<<PD5);
    TCNT1 = 0;			/* Set timer1 count zero */
	ICR1 = 2499;		/* Set TOP count for timer1 in ICR1 register (FPWM = FOSC / ( N * ( 1 + TOP ) )) so we genrate PWM signal with 20 HZ*/
    TCCR1A = (1<<WGM11)|(1<<COM1A1);    /* Set Fast PWM, TOP in ICR1, Clear OC1A on compare match, clk/64 */
	TCCR1B = (1<<WGM12)|(1<<WGM13)|(1<<CS10)|(1<<CS11);
}