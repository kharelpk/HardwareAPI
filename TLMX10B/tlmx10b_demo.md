### **MX10B Reference Transmitter**
This MX10B Reference Transmitter from Thorlabs can be controlled via serial communication.

### **Prerequisite**
Please install the [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) package by running the following command:

```python
pip install pyserial
```

### **Example**

```python
import time
from mx10b import MX10B


def main():
    port = "COM3"  # Replace with the appropriate COM port for your MX10B
    mx10b = MB10B(port)

    # Set and get the ITU channel number. ITU Channel are defined using a 50 MHz grid.
    itu_channel_number = 32
    mx10b.set_ITU_channel_number(itu_channel_number)
    print(f"Set ITU channel number to {itu_channel_number}")

    current_itu_channel_number = mx10b.get_ITU_channel_number()
    print(f"Current ITU channel number: {current_itu_channel_number}")

    # Set laser power on
    mx10b.set_laser_power_on()
    print("Laser power on")

    # Wait for 5 seconds
    time.sleep(5)

    # Get measured optical output power in dBm
    optical_output_power_dBm = mx10b.get_measured_optical_output_power_dBm()
    print(f"Measured optical output power: {optical_output_power_dBm} dBm")

    # Set laser power off
    mx10b.set_laser_power_off()
    print("Laser power off")

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the MX10B class from the mx10b.py file provided.

2. Defines a main function that:

    - Assumes you have your MX10B connected to a serial port.
    - Sets the ITU channel number. For more info read the manual.
    - Gets the current ITU channel number.
    - Sets the laser power on.
    - Waits for 5 seconds, and then gets the measured optical output power in dBm.
    - Sets the laser power off.

Make sure to replace the port variable with the appropriate COM port for your MX10B.

### Finding the COM port

1. Press `Win + X` or right-click the Start button in the lower-left corner of your screen to open the power user menu.

2. Select `Device Manager` from the menu to open the Device Manager window.

3. In the Device Manager window, look for a category called `Ports (COM & LPT)`. If you don't see it, make sure your MX10B device is properly connected to your computer.

4. Click the arrow next to `Ports (COM & LPT)` to expand the list of available ports.

5. Find your MX10B device in the list. It may be listed as a `USB Serial Device`, a `Prolific USB-to-Serial Comm Port`, or something similar depending on the specific device and driver.

6. The COM port number will be displayed in parentheses next to the device name, e.g., `USB Serial Device (COM3)`.

7. Note the COM port number and use it in your code to communicate with the MX10B device.



