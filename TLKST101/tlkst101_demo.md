### **KST101 KCube Stepper Motor Controller**
The Thorlabs KST101 KCube Stepper Motor Controller can be controlled via USB communication.

### **Prerequisite**
Please download and install the Thorlabs [Kinesis Software](https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=Motion_Control), which installs .dll files necessary to communicate with the inertial motor.

### **Example**

```python
import time
from tlkst101 import TLKST101

def main():
    dll_path = "path/to/your/dll/file"  # Replace with the path to your DLL file.
    serial_number = "28000322"  # Replace with your KST101's serial number

    kst101 = TLKST101(serial_number, dll_path)

    # Connect to the device
    kst101.connect()
    print(f"Connected to KST101 with serial number: {serial_number}")

    # Home the device
    kst101.home()
    print("Homed KST101")

    # Move the device to an absolute position in real-world units
    position = 10
    kst101.move_to_position_real_units(position)
    print(f"Moved KST101 to position {position}")

    # Wait for 2 seconds
    time.sleep(2)

    # Get the current position
    current_position = kst101.get_position()
    print(f"Current position of KST101: {current_position}")

    # Disconnect from the device
    kst101.disconnect()
    print(f"Disconnected from KST101 with serial number: {serial_number}")

if __name__ == "__main__":
    main()
```
This example code does the following:

1. Imports the necessary modules and the TLKST101 class from the tlkst101.py file provided.
2. Defines a main function that:
    - Connects to the KST101 with the given serial number.
    - Homes the device.
    - Moves the device to an absolute position in real-world units.
    - Waits for 2 seconds.
    - Gets the current position of the device.
    - Disconnects from the KST101.

Make sure to replace the dll_path variable with the correct path to your DLL file and serial_number with your KST101's serial number. Typically, the dll files are located in `C:\Program Files\Thorlabs\Kinesis`.