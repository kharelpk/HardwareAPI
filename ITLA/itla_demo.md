### **Pure-Photonics ITLA Laser**
This tunable laser in the C and L-band from [Pure-Photonics](https://static1.squarespace.com/static/536bc812e4b03a731bda083a/t/60c80022287dd131335250d1/1623719971473/Feature+Guide+PPCL600-700.pdf) can be controlled via serial communication.

### **Prerequisite**
Please install the [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) package by running the following command:

```python
pip install pyserial
```

### **Example**

```python
import time
from itla import ITLA


def main():
    port = "COM3"  # Replace with the appropriate COM port for your ITLA laser
    itla_laser = ITLA(port)

    # Set laser power on
    itla_laser.set_laser_power_on()
    print("Laser power on")

    # Wait for 5 seconds
    time.sleep(10)

    # Get measured optical output power in dBm
    optical_output_power_dBm = itla_laser.get_measured_optical_output_power_dBm()
    print(f"Measured optical output power: {optical_output_power_dBm} dBm")

    # Set laser power off
    itla_laser.set_laser_power_off()
    print("Laser power off")

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the ITLA class from the itla.py file provided.

2. Defines a main function that:

    - Assumes you have your Pure-Photonics ITLA laser connected to a serial port.
    - Sets the laser power on.
    - Waits for 10 seconds, and then gets the measured optical output power in dBm.
    - Sets the laser power off.

Make sure to replace the port variable with the appropriate COM port for your Pure-Photonics ITLA laser.
