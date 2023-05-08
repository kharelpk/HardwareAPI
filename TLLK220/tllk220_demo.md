### **LK220 Thermoelectric Liquid Chiller**
This Thermoelectric liquid chiller from Thorlabs can be controlled via serial communication using usb interface.

### **Prerequisite**
Please install the [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) package by running the following command:

```python
pip install pyserial
```
Also you will need the appropriate .dll files to control this chiller which can be downloaded from [Thorlabs](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=LK220). Since this program currently uses .dll files, this example only works in Windows Os.

### **Example**

```python
from tllk220 import TLLK220

def main():
    dll_path = "path/to/your/dll"  # Replace with the appropriate path to your DLL
    lk220 = TLLK220(dll_path)

    # List connected LK220 devices
    devices = lk220.list()
    print("Connected devices:", devices)

    if not devices:
        print("No devices found. Please check the connections.")
        return

    serial_no = devices[0][0]  # Use the first device's serial number
    n_baud = 115200  # Baud rate
    timeout = 1000   # Timeout in milliseconds

    # Open the device with the given serial number, baud rate, and timeout
    handle = lk220.open(serial_no, n_baud, timeout)
    print(f"Opened device with handle: {handle}")

    # Enable the chiller
    lk220.set_enable(handle, 1)
    print("Chiller enabled")

    # Set target temperature to 20°C
    target_temp = 20
    lk220.set_target_temp(handle, target_temp)
    print(f"Set target temperature to {target_temp}°C")

    # Wait for 10 seconds
    import time
    time.sleep(10)

    # Disable the chiller
    lk220.set_enable(handle, 0)
    print("Chiller disabled")

    # Close the device
    lk220.close(handle)
    print("Device closed")

if __name__ == "__main__":
    main()

```

This example code does the following:

1. Imports the necessary modules and the TLLK220 class from the tllk220.py file provided.

2. Defines a main function that:

    - Assumes you have your TLLK220 connected to a serial port and the DLL is available on your system.
    - Lists the connected LK220 devices.
    - Opens the device with the given serial number, baud rate, and timeout.
    - Enables the chiller.
    - Sets the target temperature.
    - Waits for 10 seconds.
    - Disables the chiller.
    - Closes the device.

Make sure to replace the `dll_path` variable with the appropriate path to your DLL. The required `Thorlabs.LK220.CommandLibrary-win32.dll` is typically found in `C:\Program Files (x86)\Thorlabs\LK220\Sample\Thorlabs_LK220_PythonSDK.`