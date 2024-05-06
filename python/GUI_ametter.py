import serial
import struct
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Function to read three float values from UART
def read_three_floats_from_uart(port='COM10', baudrate=9600):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print("Sending 'R' to UART")
            ser.write(b'A')  # Send the character 'R' to request data

            # Read 12 bytes from UART (3 floats * 4 bytes each)
            byte_data = ser.read(12)
            print(f"Read {len(byte_data)} bytes from UART")

            # Check if we received the full 12 bytes
            if len(byte_data) == 12:
                # Unpack three floats: voltage, current, and power
                voltage, current, power = struct.unpack('<fff', byte_data)
                print(f"Voltage: {voltage}, Current: {current}, Power: {power}")
                return voltage, current, power
            else:
                print("Received insufficient data")
                return None, None, None
    except serial.SerialException as e:
        print(f"Error with serial communication: {e}")
        return None, None, None

# Function to update the graph with the latest data
def update_graph(voltage, current, power):
    # Convert current from amperes to milliamperes and power from watts to milliwatts
    current *= 1000  # Convert to mA
    power *= 1000  # Convert to mW
    
    # Append data to lists
    voltage_data.append(voltage)
    current_data.append(current)
    power_data.append(power)
    
    # Update the plots with the new data
    voltage_curve.setData(voltage_data)
    current_curve.setData(current_data)
    power_curve.setData(power_data)
    print("Updated graphs with new data")

# Main function to run the application
def main():
    print("Starting application...")
    
    # Initialize the PyQt application
    app = QApplication([])
    
    # Create a PyQtGraph window for the plots
    win = pg.GraphicsLayoutWidget()
    win.setWindowTitle("Real-Time Plotting")
    win.resize(800, 800)  # Resize the window to make it bigger (adjust the dimensions as needed)
    win.show()

    # Create three plots for voltage, current, and power in a vertical arrangement
    voltage_plot = win.addPlot(row=0, col=0, title="Voltage (V)")
    current_plot = win.addPlot(row=1, col=0, title="Current (mA)")
    power_plot = win.addPlot(row=2, col=0, title="Power (mW)")

    # Set the ranges for each plot
    voltage_plot.setYRange(0, 5)  # Voltage range: 0-5 V
    current_plot.setYRange(0, 0.46)  # Current range: 0-0.46 mA
    power_plot.setYRange(0, 2.3)  # Power range: 0-2.3 mW

    # Create line objects for the plots
    global voltage_curve, current_curve, power_curve
    voltage_curve = voltage_plot.plot(pen='y')
    current_curve = current_plot.plot(pen='g')
    power_curve = power_plot.plot(pen='r')

    # Initialize data lists for each plot
    global voltage_data, current_data, power_data
    voltage_data = []
    current_data = []
    power_data = []
    
    # Create a timer to update the data every 100 ms
    def update_data():
        # Read data from UART
        voltage, current, power = read_three_floats_from_uart()
        
        if voltage is not None:
            # Update the graph with the latest data
            update_graph(voltage, current, power)
    
    # Timer configuration
    timer = QTimer()
    timer.timeout.connect(update_data)
    timer.start(100)  # Update every 100 ms
    
    print("Entering application event loop")
    # Start the application event loop
    app.exec_()

if __name__ == "__main__":
    main()