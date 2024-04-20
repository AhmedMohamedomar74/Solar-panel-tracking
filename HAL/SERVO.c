#include "SERVO.h"



void servo_int()
{
    TIMER1_PWM_intit();
}

void servo_move(signed char angle)
{
    float F_val = 0.7 * (-90 -angle);
    OCR1A = 124 - (signed char)F_val; 
}
