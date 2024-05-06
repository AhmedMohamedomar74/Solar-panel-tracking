import serial
import struct
import time

# Configure the serial connection
port = 'COM10'  # Replace with the correct port for your device (e.g., 'COM3' for Windows, '/dev/ttyUSB0' for Linux/Mac)
baud_rate = 9600  # Replace with your device's baud rate
timeout = 1  # Adjust as needed (in seconds)

# Initialize the serial connection
ser = serial.Serial(port, baud_rate, timeout=timeout)

def main():
    print(f"Connected to {port} at {baud_rate} baud.")

    # Send the start flag 'A' to the microcontroller
    start_flag = b'A'
    ser.write(start_flag)
    print("Sent start flag 'A'.")

    # Read four bytes from the serial port
    # This function blocks until the specified number of bytes (4 bytes) is read or timeout is reached
    incoming_bytes = ser.read(12)

    # Check if 4 bytes were received
    if len(incoming_bytes) == 12:
        # Display the received bytes in hexadecimal format
        hex_string = incoming_bytes.hex()
        print(f"Received 4 bytes in hexadecimal: {hex_string}")

        # Unpack the bytes to a float using the 'struct' module in little-endian float format
        voltage,current,power = struct.unpack('<fff', incoming_bytes)

        # Display the received float value
        print(f"Received float value from MC (voltage): {voltage}")
        print(f"Received float value from MC (current): {current}")
        print(f"Received float value from MC (power): {power}")
    else:
        print("Did not receive 12 bytes of data.")

    # Close the serial connection when done
    ser.close()
    print("Serial port closed.")

if __name__ == "__main__":
    main()
