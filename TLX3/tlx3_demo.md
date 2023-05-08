### **TLX3 Tunable Laser Source**
This tunable O-band laser sournce from Thorlabs can be controlled via serial communication using [USB or RS-232 ports](https://www.thorlabs.com/drawings/95d5daba0b697a3d-072A9758-9744-FD02-FF791D3D5CED2767/TLX3-ProgrammingGuide.pdf).

### **Prerequisite**
Please install the [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) package by running the following command: 

```python
pip install pyserial
```
Also install the [Thorlabs software](https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=TLX3) if you are using the USB communication.

### **Example**

```python
import time
from tlx3 import TLX3


def main():
    port = "COM3"  # Replace with the appropriate COM port for your TLX3
    tlx3 = TLX3(port)

    # Connect to the TLX3
    tlx3.connect()

    # Set and get the wavelength
    wavelength = 1550000  # in pm
    tlx3.set_wavelength(wavelength)
    print(f"Set wavelength to {wavelength} pm")

    current_wavelength = tlx3.get_wavelength()
    print(f"Current wavelength: {current_wavelength} pm")

    # Set laser power on
    tlx3.set_laser_on(1)
    print("Laser power on")

    # Wait for 5 seconds
    time.sleep(5)

    # Get laser status and power
    laser_status = tlx3.get_laser_status()
    laser_power = tlx3.get_laser_power()
    print(f"Laser status: {laser_status}, Laser power: {laser_power}")

    # Set laser power off
    tlx3.set_laser_on(0)
    print("Laser power off")

    # Disconnect from the TLX3
    tlx3.disconnect()

if __name__ == "__main__":
    main()
```


This example code does the following:

1. Imports the necessary modules and the TLX3 class from the tlx3.py file provided.

2. Defines a main function that:

    - Assumes you have your TLX3 connected to a serial port.
    - Connects to the TLX3 device.
    - Sets the wavelength (in pm).
    - Gets the current wavelength (in pm).
    - Sets the laser power on.
    - Waits for 5 seconds, and then gets the laser status and power.
    - Sets the laser power off.
    - Disconnects from the TLX3.

Make sure to replace the port variable with the appropriate COM port for your TLX3. See 'Tutorials' section for more details.