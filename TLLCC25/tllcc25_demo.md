### **LCC25 Liquid Crystal Controller**
This LCC25 Liquid Crystal Controller from Thorlabs can be controlled via USB communication.

### **Prerequisite**
Please download and install the Thorlabs [T-Cube LCC Series](https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=LCC25), which installs the .dll files necessary to communicate with the LCC25.

### **Example**
 
```python
import time
from tllcc25 import TLLCC25


def main():
    dll_path = "path/to/your/dll/file.dll"  # Replace with the path to your DLL file. LCC25CommandLib_win32.dll for 32-bit system.
    tllcc25 = TLLCC25(dll_path)

    # List all connected LCC25 devices
    devices = tllcc25.list()
    print(f"Connected devices: {devices}")

    # Get available ports
    available_ports = tllcc25.get_ports()
    print(f"Available ports: {available_ports}")

    if devices:
        # Open the first device
        device_serial, device_port = devices[0]
        baud_rate = 115200
        timeout = 3
        handle = tllcc25.open(device_serial, baud_rate, timeout)
        print(f"Opened device {device_serial} with handle {handle}")

        # Set the output mode to voltage1
        mode = 1  # 0: modulation, 1: voltage1, 2: voltage2
        tllcc25.set_output_mode(handle, mode)
        print(f"Set output mode to voltage1")

        # Get the current output mode
        current_mode = tllcc25.get_output_mode(handle)
        print(f"Current output mode: {current_mode}")

        # Set voltage1 value
        voltage1_value = 5.0
        tllcc25.set_voltage1(handle, voltage1_value)
        print(f"Set voltage1 value to {voltage1_value}")

        # Set voltage2 value
        voltage2_value = 10.0
        tllcc25.set_voltage2(handle, voltage2_value)
        print(f"Set voltage2 value to {voltage2_value}")

        # Wait for 5 seconds before closing the port
        time.sleep(5)

        # Close the device
        tllcc25.close(handle)
        print(f"Closed device {device_serial}")


if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the TLLCC25 class from the tllcc25.py file provided.

2. Defines a main function that:
    - Assumes you have at least one connected LCC25 device. 
    - It opens the first device.
    - Sets the output mode to voltage1.
    - Gets the current output mode.
    - Sets voltage1 and voltage2 values
    - Waits for 5 seconds, and then closes the device.

Make sure to replace the `dll_path` variable with the correct path to your DLL file.
