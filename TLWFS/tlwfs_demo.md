
### **Shack-Hartmann Wavefront Sensor**
This Thorlabs wavefront sensor can be controlled via USB communication. 

### **Prerequisite**
Please download and install the Thorlabs [WFS Software](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=WFS), which installs .dll files necessary to communicate with the wavefront sensor. This means you'll also need a computer running on Windows OS.

### **Example**
Below, we provide an example showing you how to communicate with your wavefront sensor using a high-level API in python. The API is implemented as a wrapper on top of Thorlabs .dll.


```python
import time
from tlwfs import TLWFS

def main():
    dll_path = "path/to/your/dll/file.dll"  # Replace with the path to your DLL file. TLWFS_64.dll for 64-bit system and TLWFS_32.dll for 32-bit system.
    resource_name = "ASRL1::INSTR"  # Replace with your wavefront sensor's resource name
    tlwfs = TLWFS(dll_path)

    # Initialize the wavefront sensor
    instrument_handle = tlwfs.init(resource_name, id_query=True, reset_device=True)
    print(f"Initialized wavefront sensor with handle: {instrument_handle}")

    # Identification query
    manufacturer, device, serial, firmware = tlwfs.identification_query(instrument_handle)
    print(f"Manufacturer: {manufacturer}\nDevice: {device}\nSerial: {serial}\nFirmware: {firmware}")

    # Take a spotfield image
    tlwfs.take_spotfield_image(instrument_handle)
    print("Took a spotfield image")

    # Get the spotfield image
    image_data, rows, columns = tlwfs.get_spotfield_image(instrument_handle)
    print(f"Retrieved spotfield image with dimensions: {rows}x{columns}")

    # Process the image data as needed...

    # Close the wavefront sensor
    tlwfs.close(instrument_handle)
    print(f"Closed wavefront sensor with handle: {instrument_handle}")

if __name__ == "__main__":
    main()
```

This example code does the following:

1. Imports the necessary modules and the TLWFS class from the tlwfs.py file provided.

2. Defines a main function that:
    
    - Initializes the wavefront sensor with the given resource name.
    - Performs an identification query to get the wavefront sensor's details.
    - Takes a spotfield image using the sensor.
    - Retrieves the spotfield image and its dimensions.
    - Processes the image data as needed (not shown).
    - Closes the wavefront sensor.
Make sure to replace the `dll_path` variable with the correct path to your DLL file. 
Typically, WFS_64.dll can be found inside `C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll` in 64-bit windows system and `C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin\WFS_32.dll` for 32-bit system. 
Replace resource_name with your wavefront sensor's resource name.