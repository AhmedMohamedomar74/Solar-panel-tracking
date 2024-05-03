#include "../HAL/Ameter.h"
#include "../MCAL/UART.h"
#include "../HAL/SERVO.h"

void chec_Arr(unsigned char *arr);
void Plot_fun(Measaure_t Measure);
void Automatic_control(signed char *angle_value);

#define ADC_CHANELL 2
signed char angle_value = 0;
int main()
{
    UART_init(9600);
    Ameter_init();
    servo_int();
    while (1)
    {
        chec_Arr(Rec_arr);
    }
}

void Plot_fun(Measaure_t Measure)
{
    UART_TX_Float(Measure.voltage_measument);
    UART_TX_Float(Measure.current_measument);
    UART_TX_Float(Measure.Power_measurment);
}

void Automatic_control(signed char *angle_value)
{
    unsigned int Read_lift = ADC_READ(0);
    unsigned int Read_right = ADC_READ(1);
    int tol = 50;
    int differance_H = Read_lift - Read_right;
    if ((differance_H > tol) || (differance_H < (-1 * tol)))
    {
        if (Read_lift > Read_right)
        {
            *(angle_value) = ++*(angle_value);
            if (*(angle_value) > 90)
            {
                *(angle_value) = 90;
            }
        }
        else if (Read_lift < Read_right)
        {
            *(angle_value) = --*(angle_value);
            if (*(angle_value) < -90)
            {
                *(angle_value) = -90;
            }
        }
        servo_move(*(angle_value));
    }
}

void chec_Arr(unsigned char *arr)
{
    switch (arr[0])
    {
    case 'A':
        Automatic_control(&angle_value);
        break;

    case 'M':
        servo_move((signed char)arr[1]);
        break;

    default:
        break;
    }

    switch (arr[2])
    {
    case 'P':
    	{
    		Measaure_t Measure_adc =  Measured_voltage(ADC_CHANELL);
    		Plot_fun(Measure_adc);
    	}
        break;
    default:
        break;
    }
}
