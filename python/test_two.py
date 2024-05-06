import serial
import struct

# Configure the serial connection
port = 'COM11'  # Replace with the correct port for your device (e.g., 'COM3' for Windows, '/dev/ttyUSB0' for Linux/Mac)
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

    # Wait a short period of time to allow the microcontroller to process the start flag
    # Uncomment and adjust the sleep time if needed
    # time.sleep(0.5)

    # Read 2 bytes from the serial port
    # This function blocks until the specified number of bytes (2 bytes) is read or timeout is reached
    incoming_bytes = ser.read(2)
    print(f"Received bytes: {incoming_bytes}")

    # If 2 bytes are received
    if len(incoming_bytes) == 2:
        # Unpack the bytes to a 2-byte integer using the 'struct' module
        # '<h' indicates little-endian 2-byte (short) integer format
        int_value, = struct.unpack('<h', incoming_bytes)

        # Display the received integer value
        print(f"Received 2-byte integer from device: {int_value}")

    else:
        print("Did not receive 2 bytes of data.")

    # Close the serial connection when done
    ser.close()

if __name__ == "__main__":
    main()
