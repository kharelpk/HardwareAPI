### **Thorlabs PAX1000 Polarimeter**
This Thorlabs Power Meter can be controlled via USB using SCPI communication protocol. 

### **Prerequisite**
1. Download and install the Thorlabs [PAX1000] (https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=1564) software, which includes drivers necessary to communicate with the polarimeter.
2. Install pyvisa package using pip:
```shell
pip install pyvisa
```
3. Install [NI-VISA] (https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#480875) from the National Instruments website. This provides the necessary backend for PyVISA to communicate with the hardware.

### **Example**
Below we show an example, showing how to use pyvisa to obtain data from your polarimeter.

```python
import math
from tlpax import TLPAX

def main():
    # Create an instance of the ThorlabsPAX1000 class
    resource_name = "USB0::0x1313::0x8031::M00547469::0::INSTR"
    polarimeter = TLPAX(resource_name)

    # Identify Thorlabs PAX1000
    print(polarimeter.identify())  # Expected return is 'THORLABS,PAX1000IR2/M,M00547469,1.0.3'

    # Set measurement mode to 9 and enable waveplate rotation
    polarimeter.set_averaging_mode(9)
    polarimeter.set_waveplate_rotation_state("ON")

    # Get measurement
    message = polarimeter.get_latest_primary_measurement_data()
    message = list(map(float, message.split(',')))

    # Convert data to conventional units
    mode = message[2]
    az = message[9] * 180 / math.pi  # in °
    ellip = message[10] * 180 / math.pi  # in °
    DOP = message[11] * 100  # in %
    P = message[12] * 1e3  # in mW

    print(f"Mode: {mode}\naz: {az}\nellip: {ellip}\nDOP: {DOP}\nP: {P}")

    # Compute normalized Stokes parameters
    Psi = message[9]
    Chi = message[10]
    S1 = math.cos(2 * Psi) * math.cos(2 * Chi)  # normalized S1
    S2 = math.sin(2 * Psi) * math.cos(2 * Chi)  # normalized S2
    S3 = math.sin(2 * Chi)  # normalized S3

    print(f"S1: {S1}\nS2: {S2}\nS3: {S3}")

    # Disconnect the device
    polarimeter.disconnect()

if __name__ == "__main__":
    main()

```

This example code does the following:

This script uses the ThorlabsPAX1000 class to interact with the Thorlabs PAX1000 polarimeter. 

1. The script connects to the device and identifies it. 
2. It sets the measurement mode to 9.
3. Enables waveplate rotation. 
4. Gets the latest measurement data and converts the data to conventional units.
5. It then computes the normalized Stokes parameters, and then disconnects from the device. The script's output will display the obtained data and calculated values.

Please look up the tutorials section on how to identify the `resource_name`.

