import serial
import struct
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer

# Declare global variables
is_auto = True  # Initial mode is Auto
is_plotting = False  # Initial state is not plotting
voltage_data, current_data, power_data = [], [], []

# Initialize serial connection (adjust port and baud rate as needed)
ser = serial.Serial('COM1', baudrate=9600, timeout=1)

# Main application window
class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
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
        self.send_button.clicked.connect(self.send_array)
        main_layout.addWidget(self.send_button, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Create the plotting area
        self.graphWidget = pg.GraphicsLayoutWidget()
        self.voltagePlot = self.graphWidget.addPlot(title="Voltage (V)")
        self.currentPlot = self.graphWidget.addPlot(title="Current (mA)")
        self.powerPlot = self.graphWidget.addPlot(title="Power (mW)")

        self.voltageCurve = self.voltagePlot.plot(pen='y')
        self.currentCurve = self.currentPlot.plot(pen='g')
        self.powerCurve = self.powerPlot.plot(pen='r')

        # Add the plotting area to the main layout
        main_layout.addWidget(self.graphWidget)
        
        # Set the plotting area visibility according to the initial mode
        self.graphWidget.setVisible(is_plotting)

        # Configure the main window
        self.setWindowTitle('Toggle Buttons and Input')
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
        self.graphWidget.setVisible(is_plotting)
        if is_plotting:
            self.start_plotting()
        else:
            self.timer.stop()

    def start_plotting(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_and_update)
        self.timer.start(100)

    def fetch_and_update(self):
        voltage, current, power = self.read_three_floats_from_uart()
        if voltage is not None:
            self.update_graph(voltage, current, power)

    def update_graph(self, voltage, current, power):
        # Convert current from amperes to milliamperes
        current *= 1000
        # Convert power from watts to milliwatts
        power *= 1000
        # Append data to lists
        voltage_data.append(voltage)
        current_data.append(current)
        power_data.append(power)
        # Update plots
        self.voltageCurve.setData(voltage_data, pen='y')
        self.currentCurve.setData(current_data, pen='g')
        self.powerCurve.setData(power_data, pen='r')
        print("Updated graphs with new data")

    def send_array(self):
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
        byte_array = first_byte + second_byte + third_byte

        # Send the array of bytes over the serial port
        ser.write(byte_array)
        print(f"Sent byte array: {byte_array.hex()}")

    def read_three_floats_from_uart(self):
        # Send 'R' to request data
        ser.write(b'R')
        # Read 12 bytes from UART (3 floats * 4 bytes each)
        byte_data = ser.read(12)
        if len(byte_data) == 12:
            # Unpack the three floats (voltage, current, and power)
            voltage, current, power = struct.unpack('<fff', byte_data)
            return voltage, current, power
        return None, None, None

# Main function to run the application
def main():
    app = QApplication([])
    main_widget = AppWindow()
    main_widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
