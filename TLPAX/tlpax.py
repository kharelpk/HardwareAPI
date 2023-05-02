# Uses SCPI commands to communicate with the PAX1000 polarimeter from Thorlabs.

import pyvisa

class TLPAX:
    """
    A Python class for controlling the Thorlabs PAX1000 polarimeter using SCPI commands.
    """
    def __init__(self, resource_name):
        """
        Initialize the TLPAX object.

        :param resource_name: The VISA resource name for the PAX1000 polarimeter.
        :type resource_name: str
        """
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)
        self.instrument.timeout = 5000 # in milliseconds
        
    def send_command(self, command):
        """
        Send a command to the instrument.

        :param command: The SCPI command to send.
        :type command: str
        """
        self.instrument.write(command)
        
    def query(self, command):
        """
        Query the instrument and return the response.

        :param command: The SCPI query command to send.
        :type command: str
        :return: The response from the instrument.
        :rtype: str
        """
        return self.instrument.query(command)
    
    def get_identification(self):
        """
        Get the identification information of the instrument.

        :return: A list containing the manufacturer, model, serial number, and firmware version.
        :rtype: list
        """
        idn = self.query("*IDN?")
        return idn.split(",")

    def reset(self):
        """
        Reset the instrument to its default state.
        """
        self.send_command("*RST")

    def operation_complete(self):
        """
        Set the Operation Complete bit in the Standard Event Register.
        """
        self.send_command("*OPC")
        
    def wait_to_continue(self):
        """
        Wait until all previous commands are executed.
        """
        self.send_command("*WAI")
        
    def self_test(self):
        """
        Perform the instrument's self-test and return the result.

        :return: The self-test result.
        :rtype: str
        """
        return self.query("*TST?")
    
    def close(self):
        """
        Close the connection to the instrument.
        """
        self.instrument.close()

    def set_averaging_mode(self, mode):
        """
        Set the averaging mode for the polarimeter.

        :param mode: Averaging mode to be set. Modes range from 1 to 9.
        :type mode: int       
        #  Set averaging mode:
        # 1 = H512 (half waveplate
        # rotation with 512 point FFT)
        # 2 = H1024
        # 3 = H2048
        # 4 = F512
        # 5 = F1024 (one full waveplate
        # rotation with 1024 point FFT)
        # 6 = F2048
        # 7 = D512
        # 8 = D1024
        # 9 = D2048 (two waveplate rotations with 2048 point FFT)
        """

        self.send_command(f"SENS:CALC:MODE {mode}")

    def get_averaging_mode(self):
        """
        Get the currently set averaging mode.

        :return: The current averaging mode.
        :rtype: str
        """
        return self.query("SENS:CALC:MODE?")

    def set_wavelength(self, wavelength):
        """
        Set the wavelength for the polarimeter.

        :param wavelength: Wavelength in meters.
        :type wavelength: float
        """
        # Wavelength is in m
        self.send_command(f"SENS:CORR:WAV {wavelength}")

    def get_wavelength(self):
        """
        Get the currently set wavelength.

        :return: The current wavelength in meters.
        :rtype: str
        """
        return self.query("SENS:CORR:WAV?")

    def set_power_range_upper(self, value):
        """
        Set the most positive signal level for the sensor input.

        :param value: The most positive signal level.
        :type value: float
        """
        self.send_command(f"SENS:POW:RANG:UPP {value}")

    def get_power_range_upper(self):
        """
        Get the most positive signal level for the sensor input.

        :return: The most positive signal level.
        :rtype: str
        """
        return self.query("SENS:POW:RANG:UPP?")

    def set_power_range_auto(self, value):
        """
        Set the power range to the value that provides the most dynamic range without overloading.

        :param value: 0 or "OFF" to disable, 1 or "ON" to enable, 2 or "ONCE" to perform once.
        :type value: int or str
        """
        self.send_command(f"SENS:POW:RANG:AUTO {value}")

    def get_power_range_auto(self):
        """
        Get the auto-ranging setting.

        :return: The auto-ranging setting.
        :rtype: str
        """
        return self.query("SENS:POW:RANG:AUTO?")

    def set_power_range_index(self, index):
        """
        Set the power range index.

        :param index: The power range index (1 to 16).
        :type index: int
        """
        self.send_command(f"SENS:POW:RANG:IND {index}")

    def get_power_range_index(self):
        """
        Get the currently active power range index.

        :return: The active power range index.
        :rtype: str
        """
        return self.query("SENS:POW:RANG:IND?")

    def get_power_range_nominal(self, index=None):
        """
        Get the most positive signal level for the specified power range index.

        :param index: The power range index (1 to 16), optional. If not provided, defaults to the currently active index.
        :type index: int, optional
        :return: The most positive signal level for the specified power range index.
        :rtype: str
        """
        if index is None:
            return self.query("SENS:POW:RANG:NOM?")
        else:
            return self.query(f"SENS:POW:RANG:NOM? {index}")

    def get_latest_primary_measurement_data(self):
        """
        Get the latest completed primary measurement data set.

        :return: Latest completed primary measurement data set.
        :rtype: str
        """
        # Returns latest completed primary measurement data set:
        # revs, timestamp, paxOpMode, paxFlags, paxTIARange,adcMin, adcMax, revTime, misAdj, theta, eta, DOP, Ptotal
        return self.query("SENS:DATA:PRIM:LAT?")

    def get_calibration_string(self):
        """
        Get the device's calibration string.

        :return: The device's calibration string.
        :rtype: str
        """
        return self.query("CAL:STR?")

    def set_waveplate_rotation_state(self, state):
        """
        Enable or disable waveplate rotation.

        :param state: 0 or "OFF" to disable, 1 or "ON" to enable.
        :type state: int or str
        """
        self.send_command(f"INP:ROT:STAT {state}")

    def get_waveplate_rotation_state(self):
        """
        Get the waveplate motor state.

        :return: The waveplate motor state.
        :rtype: str
        """
        return self.query("INP:ROT:STAT?")

    def set_waveplate_rotation_velocity(self, velocity):
        """
        Set the waveplate's rotation velocity.

        :param velocity: The waveplate rotation velocity in 1/s.
        :type velocity: float
        """
        self.send_command(f"INP:ROT:VEL {velocity}")

    def get_waveplate_rotation_velocity(self):
        """
        Get the waveplate rotation velocity.

        :return: The waveplate rotation velocity in 1/s.
        :rtype: str
        """
        return self.query("INP:ROT:VEL?")

    def get_waveplate_rotation_velocity_limits(self):
        """
        Get the maximum waveplate rotation velocity limits for operation with and without external power supply.

        :return: The maximum waveplate rotation velocity limits.
        :rtype: str
        """
        return self.query("INP:ROT:VEL:LIM?")