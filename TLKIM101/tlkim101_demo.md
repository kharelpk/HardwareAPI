### **KIM101 Inertial Motor**
The Thorlabs KIM101 Inertial Motor can be controlled via USB communication.

### **Prerequisite**
Please download and install the Thorlabs [Kinesis Software](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=12033), which installs .dll files necessary to communicate with the inertial motor.

### **Example**

```python
import time
from tlkim101 import TLKIM101

def main():
    dll_path = "path/to/your/dll/file"  # Replace with the path to your DLL file.
    serial_number = "28000322"  # Replace with your KIM101's serial number
    channel = 1

    kim101 = TLKIM101(serial_number, dll_path)

    # Connect to the device
    kim101.connect(channel)
    print(f"Connected to KIM101 with serial number: {serial_number}")

    # Home the device
    kim101.home(channel)
    print(f"Homed KIM101 on channel {channel}")

    # Move the device to an absolute position
    position = 10
    kim101.move_absolute(channel, position)
    print(f"Moved KIM101 to position {position} on channel {channel}")

    # Wait for 2 seconds
    time.sleep(2)

    # Move the device relative to its current position
    step_size = 5
    kim101.move_relative(channel, step_size)
    print(f"Moved KIM101 by {step_size} relative to its current position on channel {channel}")

    # Wait for 2 seconds
    time.sleep(2)

    # Stop the device
    kim101.move_stop(channel)
    print(f"Stopped KIM101 on channel {channel}")

    # Disconnect from the device
    kim101.disconnect(channel)
    print(f"Disconnected from KIM101 with serial number: {serial_number}")

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the TLKIM101 class from the tlkim101.py file provided.
2. Defines a main function that:
    - Connects to the KIM101 with the given serial number.
    - Homes the device for the specified channel.
    - Moves the device to an absolute position for the specified channel.
    - Waits for 2 seconds.
    - Moves the device relative to its current position for the specified channel.
    - Waits for 2 seconds.
    - Stops the device for the specified channel.
    - Disconnects from the KIM101.
Make sure to replace the dll_path variable with the correct path to your DLL file and serial_number with your KIM101's serial number. Typically the dll files are located in `C:\Program Files\Thorlabs\Kinesis`.

