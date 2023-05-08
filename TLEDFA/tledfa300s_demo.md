### **Thorlabs EDFA 300s**
This Thorlabs Erbuium doped fiber amplifier (EDFA) [300s](https://www.thorlabs.de/thorproduct.cfm?partnumber=EDFA300S) can be controlled via a usb interface.

### **Prerequisite**
1. Install pyvisa package using pip:
```shell
pip install pyvisa
```

### **Example**
Below we show an example, showing how to use pyvisa to obtain data from your polarimeter.

```python
from tledfa300s import EDFA300S

def main():
    # Create an instance of the EDFA class
    port = "COM1"  # Replace "COM1" with the appropriate port for your system
    edfa = EDFA(port)

    # Get help and status information
    print(edfa.get_status())

    # Enable the laser and set the laser diode current to 50%
    edfa.enable_laser()
    edfa.set_laser_diode_current(50)

    # Get the current laser diode current
    print(edfa.get_laser_diode_current())

    # Disable the laser and close the serial connection
    edfa.disable_laser()
    edfa.close()

if __name__ == "__main__":
    main()


```

This example code does the following:

1. This script uses the EDFA class to interact with the Thorlabs EDFA 300s device.

2. The script creates an instance of the EDFA class with the appropriate serial port.
    - It retrieves status information from the device and prints it.
    - Enables the laser and sets the laser diode current to 50 mA.
    - Gets the current laser diode current and prints it.
    - Disables the laser and closes the serial connection to the device.

Please look up the documentation for your operating system on how to identify the serial port.
