import serial
import struct
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer
import time

# Declare global variables
is_auto = True  # Initial mode is Auto
is_plotting = False  # Initial state is not plotting
latest_array = None  # Variable to store the latest array

# Initialize serial connection (adjust port and baud rate as needed)
# Define the serial connection as a global variable
try:
    ser = serial.Serial('COM11', baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Error initializing serial connection: {e}")
    ser = None  # Set to None if there's an error

# Plot window class for displaying plots in a separate window
class PlotWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the plots
        layout = QVBoxLayout(self)

        # Create the plot widgets for voltage, current, and power
        self.plot_widget = pg.GraphicsLayoutWidget()
        layout.addWidget(self.plot_widget)

        # Create plots
        self.voltage_plot = self.plot_widget.addPlot(title="Voltage")
        self.voltage_curve = self.voltage_plot.plot()

        self.plot_widget.nextRow()  # Move to the next row of plots

        self.current_plot = self.plot_widget.addPlot(title="Current")
        self.current_curve = self.current_plot.plot()

        self.plot_widget.nextRow()  # Move to the next row of plots

        self.power_plot = self.plot_widget.addPlot(title="Power")
        self.power_curve = self.power_plot.plot()

        # Set plot ranges
        self.voltage_plot.setYRange(0, 5)  # Voltage range: 0-5 V
        self.current_plot.setYRange(0, 0.46)  # Current range: 0-0.46 mA
        self.power_plot.setYRange(0, 2.3)  # Power range: 0-2.3 mW

        # Set the window title and size
        self.setWindowTitle("Plots")
        self.resize(400, 600)

        # Initialize data lists
        self.time_data = []
        self.voltage_data = []
        self.current_data = []
        self.power_data = []

        # Timer to update the plots regularly (1 second)
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plots)

    def update_plots(self):
        # Update the plots with the latest data
        self.voltage_curve.setData(self.time_data, self.voltage_data)
        self.current_curve.setData(self.time_data, self.current_data)
        self.power_curve.setData(self.time_data, self.power_data)

    def clear_plots(self):
        # Clear data lists
        self.time_data = []
        self.voltage_data = []
        self.current_data = []
        self.power_data = []
        # Clear curves
        self.voltage_curve.setData([], [])
        self.current_curve.setData([], [])
        self.power_curve.setData([], [])

    def set_plot_labels(self):
        # Set the y-axis labels for the plots
        self.voltage_plot.setLabel('left', 'Voltage (V)')
        self.current_plot.setLabel('left', 'Current (mA)')
        self.power_plot.setLabel('left', 'Power (mW)')

# Main application window
class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Create a QTimer to handle automatic sending every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_latest_array)
        self.timer.start(1000)  # Timer interval set to 1000 ms (1 second)

        # Create an instance of PlotWindow (but do not show it yet)
        self.plot_window = PlotWindow()
        
        # Initialize the start time for time tracking
        self.start_time = 0

    def initUI(self):
        # Create a vertical layout for the entire window
        main_layout = QVBoxLayout(self)

        # Create a horizontal layout for the "Auto/Manual" button and input field
        auto_input_layout = QHBoxLayout()

        # Create the "Auto/Manual" button
        self.auto_button = QPushButton("Manual" if is_auto else "Auto")
        self.auto_button.clicked.connect(self.toggle_auto_button)
        
        # Create the input field for the angle
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter angle here")
        self.input_field.setVisible(not is_auto)  # Show input field only in Manual mode
        auto_input_layout.addWidget(self.auto_button)
        auto_input_layout.addWidget(self.input_field)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(auto_input_layout)

        # Create the "Plot/Stop Plot" button
        self.plot_button = QPushButton("Plot" if not is_plotting else "Stop Plot")
        self.plot_button.clicked.connect(self.toggle_plot_button)
        main_layout.addWidget(self.plot_button, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Create the "Send" button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.update_array_and_send)
        main_layout.addWidget(self.send_button, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Configure the main window
        self.setWindowTitle('Toggle Buttons, Input, and Plotting')
        self.resize(350, 300)

    def toggle_auto_button(self):
        global is_auto
        is_auto = not is_auto
        self.auto_button.setText("Manual" if is_auto else "Auto")
        self.input_field.setVisible(not is_auto)

    def toggle_plot_button(self):
        global is_plotting
        is_plotting = not is_plotting
        self.plot_button.setText("Stop Plot" if is_plotting else "Plot")

        if is_plotting:
            # If plot mode is activated, show the plot window
            self.plot_window.show()
            # Reset the start time for the plot window
            self.start_time = time.time()
            # Start the plot timer
            self.plot_window.plot_timer.start(1000)
            # Set plot labels to display units
            self.plot_window.set_plot_labels()
        else:
            # If plot mode is deactivated, clear the plots and hide the plot window
            self.plot_window.clear_plots()
            self.plot_window.hide()
            # Stop the plot timer
            self.plot_window.plot_timer.stop()

    def update_array_and_send(self):
        # Check if the serial connection is initialized
        if ser is None:
            print("Serial connection is not initialized.")
            return
        
        # Determine the first byte based on mode
        first_byte = b'A' if is_auto else b'M'  # 'A' for automatic mode, 'M' for manual mode
        
        # Determine the second byte
        if is_auto:
            second_byte = b'\xFF'  # Second byte is FF for automatic mode
        else:
            value_str = self.input_field.text()
            try:
                value = int(value_str)
                if not (-127 <= value <= 127):
                    print(f"Value {value} is out of range (-127 to 127). Please enter a valid angle.")
                    return
                # Convert the angle value to a signed byte
                second_byte = value.to_bytes(1, byteorder='big', signed=True)
            except ValueError:
                print(f"Invalid value entered: {value_str}. Please enter a valid integer.")
                return

        # Determine the third byte based on plotting mode
        third_byte = b'P' if is_plotting else b'b'  # 'P' for plotting mode, 'b' for stopping plot mode

        # Combine the bytes into an array
        global latest_array
        latest_array = first_byte + second_byte + third_byte

        # Send the array of bytes over the serial port
        try:
            ser.write(latest_array)
            print(f"Sent byte array: {latest_array.hex()}")

            # If in plot mode, immediately read an integer value from the microcontroller
            if is_plotting:
                self.receive_integer_from_uart()
        except serial.SerialException as e:
            print(f"Error during serial communication: {e}")

    def send_latest_array(self):
        # Check if the serial connection is initialized
        if ser is None:
            print("Serial connection is not initialized.")
            return
        
        # Send the latest array if it exists
        if latest_array is not None:
            try:
                ser.write(latest_array)
                print(f"Sent latest byte array: {latest_array.hex()}")

                # If in plot mode, immediately read an integer value from the microcontroller
                if is_plotting:
                    self.receive_integer_from_uart()
            except serial.SerialException as e:
                print(f"Error during serial communication: {e}")

    def receive_integer_from_uart(self):
        # Check if the serial connection is initialized
        if ser is None:
            print("Serial connection is not initialized.")
            return
        
        # Read 2 bytes from UART (16-bit integer)
        try:
            incoming_bytes = ser.read(2)
            print(f"incoming_bytes = {incoming_bytes}")
            if len(incoming_bytes) == 2:
                # Unpack the integer value from the 2-byte data
                int_value = struct.unpack('<H', incoming_bytes)[0]
                
                # Calculate voltage, current, and power
                voltage = (int_value * 4.15 / 1023.0) * (10000 + 5000) / 5000
                current = voltage / (10000 + 5000)
                power = current * voltage

                # Convert current and power to milliamperes and milliwatts
                current *= 1000  # Convert to mA
                power *= 1000  # Convert to mW

                print(f"Voltage = {voltage}")
                print(f"Current = {current} mA")
                print(f"Power = {power} mW")
                
                # Display the received integer value
                print(f"Received 2-byte unsigned integer from device: {int_value}")

                # Store the data for plotting
                current_time = time.time() - self.start_time
                self.plot_window.time_data.append(current_time)
                self.plot_window.voltage_data.append(voltage)
                self.plot_window.current_data.append(current)
                self.plot_window.power_data.append(power)
            else:
                print("Received incorrect amount of data after sending array.")
        except serial.SerialException as e:
            print(f"Error during serial communication: {e}")

# Main function to run the application
def main():
    app = QApplication([])
    main_widget = AppWindow()
    main_widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
