### **Thorlabs Fiber Laser**
This Thorlabs Fiber Laser can be controlled via serial communication.

### **Prerequisite**
Please install the [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) package by running the following command:

```shell
pip install pyserial
```


### **Example**
Below we show an example code to communicate the the Fiber laser.

```python
import time
from tllfl import TLLFL


def main():
    port = "COM3"  # Replace with the appropriate COM port for your Thorlabs Fiber Laser
    laser = TLLFL(port)

    # Set laser current and enable the laser
    laser_current = 200
    laser.set_current(laser_current)
    print(f"Set laser current to {laser_current} mA")

    laser.set_enable(1)
    print("Laser enabled")

    # Wait for 5 seconds
    time.sleep(5)

    # Get actual temperature, current, and power
    actual_temp = laser.get_actual_temp()
    print(f"Actual temperature: {actual_temp} °C")

    current = laser.get_current()
    print(f"Current: {current} mA")

    power = laser.get_power()
    print(f"Power: {power} mW")

    # Disable the laser
    laser.set_enable(0)
    print("Laser disabled")

    # Close the serial connection
    laser.close()

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the Laser class from the tllfl.py file provided.

2. Defines a main function that:
Assumes you have your Thorlabs Fiber Laser connected to a serial port.
    - Sets the target temperature.
    - Gets the current target temperature.
    - Sets the laser current.
    - Enables the laser.
    - Waits for 5 seconds, and then gets the actual temperature, current, and power.
    - Disables the laser.
    - Closes the serial connection.
    - Make sure to replace the port variable with the appropriate COM port for your Thorlabs Fiber Laser.
