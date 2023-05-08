### **Compact CCD Spectrometer**
This Thorlabs compact spectrometer can be controlled via USB communication.

### **Prerequisite**
Please download and install the Thorlabs [CCS Series Spectrometer](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3482) software, which installs .dll files necessary to communicate with the spectrometer. This means you'll also need a computer running on Windows OS. Make sure to choose the right 32-bit or 64-bit version.

### **Example**
Below, we provide an example showing you how to communicate with your spectrometer. The API is implemented as a wrapper on top of Thorlabs .dll.

```python
import time
from tlccs import TLCCS

def main():
    dll_path = "path/to/your/dll/file.dll"  # Replace with the path to your DLL file. TLCCS_64.dll for 64-bit system and TLCCS_32.dll for 32-bit system.

    resource_name = "USB0::0x1313::0x8089::M00417163::INSTR"  # Replace with your spectrometer's resource name
    tlccs = TLCCS(dll_path)

    # Initialize the spectrometer
    instrument_handle = tlccs.init(resource_name)
    print(f"Initialized spectrometer with handle: {instrument_handle}")

    # Identification query
    manufacturer, device, serial, firmware, driver_revision = tlccs.identification_query(instrument_handle)
    print(f"Manufacturer: {manufacturer}\nDevice: {device}\nSerial: {serial}\nFirmware: {firmware}\nDriver Revision: {driver_revision}")

    # Set integration time
    integration_time = 0.1  # seconds
    tlccs.set_integration_time(instrument_handle, integration_time)
    print(f"Set integration time to {integration_time} seconds")

    # Start a single scan
    tlccs.start_scan(instrument_handle)
    print("Started a single scan")

    # Get scan data
    data = tlccs.get_scan_data(instrument_handle)
    print(f"Scan data: {data}")

    # Get wavelength data
    data_set = 0  # Use factory adjustment data
    wavelength_data, minimum_wavelength, maximum_wavelength = tlccs.get_wavelength_data(instrument_handle, data_set)
    print(f"Wavelength data: {wavelength_data}\nMinimum wavelength: {minimum_wavelength} nm\nMaximum wavelength: {maximum_wavelength} nm")

    # Close the spectrometer
    tlccs.close(instrument_handle)
    print(f"Closed spectrometer with handle: {instrument_handle}")

if __name__ == "__main__":
    main()

```

This example code does the following:

1. Imports the necessary modules and the TLCCS class from the tlccs.py file provided.
2. Defines a main function that:
    - Initializes the spectrometer with the given resource name.
    - Performs an identification query to get the spectrometer's details.
    - Sets the integration time for the spectrometer.
    - Starts a single scan.
    - Gets the scan data.
    - Gets the wavelength data.
    - Closes the spectrometer.

Make sure to replace the dll_path variable with the correct path to your DLL file. Typically, TLCCS_64.dll can be found inside C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLCCS_64.dll in 64-bit windows system and C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\TLCCS_32.dll for 32-bit systems.

