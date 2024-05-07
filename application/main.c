#include "../HAL/multimeter.h"
#include "../HAL/SERVO.h"

// Definitions
#define BUFFER_SIZE 3

// Global variables
signed char angle_value = 0;
unsigned char Rec_arr[BUFFER_SIZE];
unsigned char counter = 0;
volatile unsigned char data_available = 0; // Flag to indicate data availability
signed char angle = 0;

// Function prototypes
void Automatic_control(signed char *angle_value);
void check_Arr(unsigned char *arr);

int main()
{
    // Initialization
    UART_init(9600);
    multimeterInit();
    servo_int();
    // Main loop
    while (1)
    {
        // Check if data is available
        if (data_available)
        {
            // Process received data
            if (Rec_arr[2] == 0x50)
            {
                // Process the ADC_READ(3) based on the 'p' command
                // int val_adc = 0x03FF & ADC_READ(3);
                UART_TX_int(ADC_READ(3));
            }
            // 41ff50 4d2d50
            if (Rec_arr[0] == 0x41)
            {
                Automatic_control(&angle);
            }
            else if (Rec_arr[0] == 0x4d)
            {
                servo_move(Rec_arr[1]);
            }

            // Reset data availability flag and counter after processing
            data_available = 0;
            counter = 0;
        }
    }
}

void Automatic_control(signed char *angle_value)
{
    unsigned int Read_lift = ADC_READ(0);
    unsigned int Read_right = ADC_READ(1);
    int tol = 20;
    int difference_H = Read_lift - Read_right;
    if ((difference_H > tol) || (difference_H < (-1 * tol)))
    {
        if (Read_lift > Read_right)
        {
            (*angle_value)++;
            if (*angle_value > 90)
            {
                *angle_value = 90;
            }
        }
        else if (Read_lift < Read_right)
        {
            (*angle_value)--;
            if (*angle_value < -90)
            {
                *angle_value = -90;
            }
        }
        servo_move(*angle_value);
    }
}

void check_Arr(unsigned char *arr)
{
    // Process commands in arr[0] and arr[2]
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

    if (arr[2] == 'p')
    {
        UART_TX_int(ADC_READ(3));
    }
}

ISR(USART_RXC_vect)
{
    if (counter < BUFFER_SIZE)
    {
        // Store received data in array
        Rec_arr[counter] = UDR;
        counter++;

        // If 3 bytes are received, set data availability flag
        if (counter == BUFFER_SIZE)
        {
            data_available = 1;
        }
    }
    else
    {
        // Reset counter if it goes out of bounds (safety measure)
        counter = 0;
    }
}
