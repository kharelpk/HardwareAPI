Copy code
### **Thorlabs Power Meter**
This Thorlabs Power Meter can be controlled via USB communication.

### **Prerequisite**
Please download and install the Thorlabs [Power Meter](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=PM100x), which installs .dll files necessary to communicate with the power meter.

### **Example**

```python
import time
from tlpm import TLPM

def main():
    dll_path = "path/to/your/dll/file.dll"  # Replace with the path to your DLL file
    resource_name = "USB0::0x1313::0x8072::P2000000::INSTR"  # Replace with your power meter's resource name
    tlpm = TLPM(dll_path)

    # Initialize the power meter
    instrument_handle = tlpm.init(resource_name, id_query=True, reset_device=True)
    print(f"Initialized power meter with handle: {instrument_handle}")

    # Identification query
    manufacturer, device, serial, firmware = tlpm.identification_query(instrument_handle)
    print(f"Manufacturer: {manufacturer}\nDevice: {device}\nSerial: {serial}\nFirmware: {firmware}")

    # Set average time for measurement value generation
    avg_time = 0.5
    tlpm.set_avg_time(instrument_handle, avg_time)
    print(f"Set average time to {avg_time} seconds")

    # Set the wavelength
    wavelength = 780
    tlpm.set_wavelength(instrument_handle, wavelength)
    print(f"Set wavelength to {wavelength} nm")

    # Set power auto range
    auto_range = True
    tlpm.set_power_auto_range(instrument_handle, auto_range)
    print(f"Set power auto range to {auto_range}")

    # Measure power
    power = tlpm.meas_power(instrument_handle)
    print(f"Measured power: {power} W")

    # Close the power meter
    tlpm.close(instrument_handle)
    print(f"Closed power meter with handle: {instrument_handle}")

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the TLPM class from the tlpm.py file provided.
2. Defines a main function that:
    - Initializes the power meter with the given resource name.
    - Performs an identification query to get the power meter's details.
    - Sets the average time for measurement value generation.
    - Sets the wavelength.
    - Sets the power auto range mode.
    - Measures the power.
    - Closes the power meter.

Make sure to replace the `dll_path` variable with the correct path to your DLL file and `resource_name` with your power meter's resource name.

