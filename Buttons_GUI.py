import serial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

# Declare global variables
is_auto = True  # Initial mode is Auto
is_plotting = False  # Initial state is not plotting

# Initialize serial connection (adjust port and baud rate as needed)
ser = serial.Serial('COM1', baudrate=9600, timeout=1)

# Main application window
class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize GUI components
        self.initUI()
    
    def initUI(self):
        # Create a vertical layout for the entire window
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the "Auto/Manual" button and input field
        auto_input_layout = QHBoxLayout()

        # Create the "Auto/Manual" button
        global auto_button
        auto_button = QPushButton("Manual" if is_auto else "Auto")
        auto_button.clicked.connect(self.toggle_auto_button)  # Connect button click event to toggle_auto_button function

        # Create the input field for the angle
        global input_field
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter angle here")
        input_field.setVisible(not is_auto)  # Show the input field only in Manual mode

        # Add the "Auto/Manual" button and input field to the horizontal layout
        auto_input_layout.addWidget(auto_button)
        auto_input_layout.addWidget(input_field)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(auto_input_layout)

        # Create the "Plot/Stop Plot" button
        global plot_button
        plot_button = QPushButton("Plot" if not is_plotting else "Stop Plot")
        plot_button.clicked.connect(self.toggle_plot_button)  # Connect button click event to toggle_plot_button function

        # Create the "Send" button
        global send_button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_array)  # Connect button click event to send_array function

        # Add the "Plot/Stop Plot" and "Send" buttons to the main layout
        main_layout.addWidget(plot_button, alignment=Qt.AlignLeft | Qt.AlignBottom)
        main_layout.addWidget(send_button, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Set the main layout to the window
        self.setLayout(main_layout)
        # Set the window title
        self.setWindowTitle('Toggle Buttons and Input')
        # Resize the window
        self.resize(350, 150)

    def toggle_auto_button(self):
        global is_auto  # Declare is_auto as a global variable

        # Toggle the state of is_auto
        is_auto = not is_auto

        # Update the button text based on the current state of is_auto
        auto_button.setText("Manual" if is_auto else "Auto")

        # Update visibility of the input field based on the current mode
        input_field.setVisible(not is_auto)  # Show the input field only in Manual mode

    def toggle_plot_button(self):
        global is_plotting  # Declare is_plotting as a global variable

        # Toggle the state of is_plotting
        is_plotting = not is_plotting

        # Update the button text based on the current state of is_plotting
        plot_button.setText("Stop Plot" if is_plotting else "Plot")

    def send_array(self):
        # Determine the first byte based on mode
        first_byte = b'A' if is_auto else b'M'  # 'A' for automatic mode, 'M' for manual mode

        # Determine the second byte
        if is_auto:
            second_byte = b'\xFF'  # Second byte is FF for automatic mode
        else:
            # Get the value from the input field
            value_str = input_field.text()
            try:
                value = int(value_str)
                # Ensure the value is in the range -127 to 127
                if not (-127 <= value <= 127):
                    print(f"Value {value} is out of range (-127 to 127). Please enter a valid angle.")
                    return
                # Convert the value to a signed byte
                second_byte = value.to_bytes(1, byteorder='big', signed=True)
            except ValueError:
                print(f"Invalid value entered: {value_str}. Please enter a valid integer.")
                return

        # Determine the third byte based on plotting mode
        third_byte = b'P' if is_plotting else b'b'  # 'P' for plotting mode, 'b' for stopping plot mode

        # Combine the bytes into an array
        byte_array = first_byte + second_byte + third_byte

        # Send the array of bytes over the serial port
        ser.write(byte_array)
        print(f"Sent byte array: {byte_array.hex()}")

# Main function to run the application
def main():
    print("Starting application...")

    # Initialize the PyQt application
    app = QApplication([])

    # Create an instance of AppWindow as the main widget
    main_widget = AppWindow()

    # Show the main widget
    main_widget.show()

    print("Entering application event loop")
    # Start the application event loop
    app.exec_()

if __name__ == "__main__":
    main()
