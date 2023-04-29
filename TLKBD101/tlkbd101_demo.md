### **Thorlabs KBD101 Brushless DC Motor**
This Thorlabs KBD101 Brushless DC Motor can be controlled via USB communication.

### **Prerequisite**
Please download and install the Thorlabs [Kinesis Software](https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=Motion_Control), which installs .dll files necessary to communicate with the motor. Make sure to choose the right 32-bit or 64-bit version. 

### **Example**

```python
from tlkbd101 import TLKBD101

def main():
    serial_number = "12345678"  # Replace with your KBD101 device's serial number
    dll_path = "path/to/your/dll/files"  # Replace with the path to your Thorlabs Kinesis DLL files

    motor = TLKBD101(serial_number, dll_path)

    # Connect to the KBD101 device
    motor.connect()

    # Home the KBD101 device
    motor.home()

    # Set motor parameters (counts per revolution)
    motor.set_motor_params(40000.0)

    # Set velocity parameters in real units (acceleration and max velocity)
    motor.set_velocity_parameters_real_units(5.0, 20.0)

    # Move the motor to the given position in real units
    target_position = 10.0
    motor.move_to_position_real_units(target_position)

    # Get the current position of the motor
    current_position = motor.get_position()
    print(f"Current position: {current_position}")

    # Disconnect from the KBD101 device
    motor.disconnect()

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the TLKBD101 class from the tlkbd101.py file provided.
2. Defines a main function that:
    - Creates an instance of the TLKBD101 class with the given serial number and path to the DLL files.
    - Connects to the KBD101 device.
    - Homes the KBD101 device.
    - Sets motor parameters (counts per revolution).
    - Sets velocity parameters in real units (acceleration and max velocity).
    - Moves the motor to the given position in real units.
    - Gets the current position of the motor.
    - Disconnects from the KBD101 device.

Make sure to replace the serial_number variable with your KBD101 device's serial number and dll_path with the correct path to your Thorlabs Kinesis DLL files. Typically the dll files are located in `C:\Program Files\Thorlabs\Kinesis`.

