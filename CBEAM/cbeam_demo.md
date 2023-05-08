### **Openbuilds C-BEAM CNC Machine**
**
The CBEAM CNC machine can be controlled via serial communication using the provided Python class.

### **Prerequisite**
Please install the [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) package by running the following command:

```shell
pip install pyserial
```

### **Example**
Below, we provide an example showing you how to communicate with your CBEAM CNC machine. The API issues serial commands to communicate with the instrument.

```python
import time
from cbeam import CBEAM

def main():
    address = "/dev/ttyUSB0"  # Replace with the appropriate serial port for your CBEAM CNC machine
    cbeam = CBEAM("CBEAM", address)

    # Connect to the CBEAM CNC machine
    if cbeam.connect():
        print("Connected to CBEAM CNC machine")

        # Unlock the CNC machine
        cbeam.set_unlock()

        # Set the home position
        cbeam.set_home()

        # Set the X, Y, and Z positions
        cbeam.set_position_X(100)
        cbeam.set_position_Y(50)
        cbeam.set_position_Z(0)

        # Wait for the move to complete
        cbeam.wait_for_move_complete()

        # Run G-code from a file
        # gcode_filename = "example.gcode"
        # cbeam.run_gcode(gcode_filename)

        # Disconnect from the CBEAM CNC machine
        cbeam.disconnect()

if __name__ == "__main__":
    main()

```

This example code does the following:

1. Imports the necessary modules and the CBEAM class from the cbeam.py file provided.

2. Defines a main function that:

    - Assumes you have your CBEAM CNC machine connected to a serial port.
    - Connects to the CBEAM CNC machine.
    - Unlocks the CNC machine.
    - Sets the home position.
    - Sets the X, Y, and Z positions.
    - Waits for the move to complete.
    - Disconnects from the CBEAM CNC machine.

Make sure to replace the address variable with the appropriate serial port for your CBEAM CNC machine. Please visit the 'Tutorials' section to find the appropriate serial port.

