#include "ADC.h"



static void Channel_Select(unsigned char channel_number);

void ADC_INIT()
{
   ADCSRA |= ((0 << ADPS2) | (0 << ADPS1) | (0 << ADPS0)) | (1 << ADEN);
   ADMUX |= (0 << ADLAR) | (1 << REFS0) | (0 << REFS1);
   DDRA = 0;
}

unsigned int ADC_READ(unsigned char channel_number)
{
    ADMUX &=0b11100000;
    ADMUX |=channel_number;
    unsigned int Ain;
    unsigned int AinLow;
    ADCSRA = ADCSRA | (1 << ADSC);
    /* Polling on the flag */
    while (((ADCSRA >> ADIF) & 1) == 0);
    AinLow = ADCL;
    Ain = (int)ADCH * 256;
    Ain = Ain + AinLow;
    return (Ain);

}

static void Channel_Select(unsigned char channel_number)
{

    switch (channel_number)
    {
    case 0:
        ADMUX |=  0;
        break;
    case 1:
        ADMUX |= 1;
        break;
    case 2:
        ADMUX |= 2;
        break;
    case 3:
        ADMUX |=  3;
        break;
    case 4:
        ADMUX |= 4;
        break;
    case 5:
        ADMUX |= 5;
        break;
    case 6:
        ADMUX |= 6;
        break;
    case 7:
        ADMUX |= 7;
        break;
    default:
        // Handle invalid channel numbers here
        break;
    }
}

