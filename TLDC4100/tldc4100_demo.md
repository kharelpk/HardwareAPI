### **DC4100 4-Channel LED Driver**
This Thorlabs DC4100 4-Channel LED Driver can be controlled via USB communication.

### **Prerequisite**
Please download and install the Thorlabs [DC4100 LED Driver Software](https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=DC4100), which installs .dll files necessary to communicate with the LED driver.

### **Example**

```python
import time
from tldc4100 import TLDC4100

def main():
    dll_path = "path/to/your/dll/file.dll"  # Replace with the path to your DLL file. TLDC4100_64.dll for 64-bit system and TLDC4100_32.dll for 32-bit system.
    resource_name = "ASRL1::INSTR"  # Replace with your LED driver's resource name
    tldc4100 = TLDC4100(dll_path)

    # Initialize the LED driver
    instrument_handle = tldc4100.init(resource_name, id_query=True, reset_device=True)
    print(f"Initialized LED driver with handle: {instrument_handle}")

    # Identification query
    manufacturer, device, serial, firmware = tldc4100.identification_query(instrument_handle)
    print(f"Manufacturer: {manufacturer}\nDevice: {device}\nSerial: {serial}\nFirmware: {firmware}")

    # Get LED head information
    channel = 0
    serial_number, name, led_head_type = tldc4100.get_head_info(instrument_handle, channel)
    print(f"LED Head Info (Channel {channel}):")
    print(f"Serial Number: {serial_number}\nName: {name}\nType: {led_head_type}")

    # Turn on the LED
    tldc4100.set_led_on_off(instrument_handle, channel, True)
    print(f"Turned on the LED on channel {channel}")

    # Set percental brightness
    brightness = 50.0
    tldc4100.set_percental_brightness(instrument_handle, channel, brightness)
    print(f"Set brightness to {brightness}% on channel {channel}")

    # Wait for 5 seconds
    time.sleep(5)

    # Turn off the LED
    tldc4100.set_led_on_off(instrument_handle, channel, False)
    print(f"Turned off the LED on channel {channel}")

    # Close the LED driver
    tldc4100.close(instrument_handle)
    print(f"Closed LED driver with handle: {instrument_handle}")

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the TLDC4100 class from the tldc4100.py file provided.
2. Defines a main function that:
    - Initializes the LED driver with the given resource name.
    - Performs an identification query to get the LED driver's details.
    - Gets the LED head information for the specified channel.
    - Turns on the LED for the specified channel.
    - Sets the percental brightness for the specified channel.
    - Waits for 5 seconds.
    - Turns off the LED for the specified channel.
    - Closes the LED driver.

Make sure to replace the `dll_path` variable with the correct path to your DLL file and `resource_name` with your LED driver's resource name.
