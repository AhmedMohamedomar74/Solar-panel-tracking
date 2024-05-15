# One-Dimensional Solar Panel Tracking

This document details the one-dimensional solar panel tracking project, which utilizes a servo motor to adjust the panel's angle for optimal sunlight exposure. A graphical user interface (GUI) provides control and data visualization.

### Features

The project boasts two control modes and a data plotting function:

**Mode 1: Manual/Automatic Mode**

* **Manual Mode:**  Allows you to specify an angle in the GUI, instructing the servo motor to position the solar panel accordingly.
* **Automatic Mode:** The servo motor automatically adjusts the panel's angle based on measured light intensity.

You can switch between these modes using the first button in the GUI.

**Mode 2: Plot/Stop Plot Mode**

* **Plot Mode:** Clicking the "Plot" button initiates the plotting of voltage, current, and power data from the solar panel.
* **Stop Plot Mode:** Clicking the "Plot" button again halts the data plotting.

### Getting Started

Here's a guide to setting up and running the project on your local machine:

**Prerequisites:**

* Python 3.x
* Libraries: Libraries: `pyserial`, `pyqtgraph`, and `PyQt5`

**Installation:**

1. Clone the repository:

   ```bash
   git clone [https://github.com/AhmedMohamedomar74/Solar-panel-tracking.git]
2. Install the required libraries:
    ```bash
    pip install -r requirements.txt

**Running the Project:**
1. Run the project script:

    ```bash
    python Integration_GUI.py

### Usage

The project's GUI provides two buttons for interacting with the solar panel tracking system:

* **First Button:**
    * Toggles between **Manual** and **Automatic** modes.
    * In **Manual Mode:**
        * Enter a desired angle in the designated field within the GUI.
        * The servo motor will then adjust the solar panel to match the specified angle.
        * GIF demonstrating Manual Mode

    ![Manual Mode GIF](Gifs/manual_mode.gif)

    * In **Automatic Mode:**
        * GIF demonstrating Automatic Mode

![Automatic Mode GIF](Gifs\automatic_mode_Reduced.gif)

* **Second Button:**
    * Clicking the button once initiates **Plot Mode**.
    * In **Plot Mode:**
        * The GUI starts plotting voltage, current, and power data from the solar panel in real-time.
        * Note: The measurements for power, voltage, and current will increase as the light to the solar panel increases.
        * GIF demonstrating Plot Mode

    ![Plot Mode GIF](Gifs\Plot_mode_reduced.gif)

    * Clicking the button again stops the data plotting (**Stop Plot Mode**).


