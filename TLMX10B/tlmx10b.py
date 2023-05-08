import serial

class MX10B:
    def __init__(self, port):
        self.serial_port = serial.Serial(port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
    
    def send_command(self, command):
        command = command + '\n'
        self.serial_port.write(command.encode('ascii'))
        
    def read_response(self):
        response = self.serial_port.readline().decode('ascii').strip()
        return response
    

    ### RF Amplifier Commands ###
        
    def set_crossing_point_analog(self, n):
        if -1.0 <= n <= 1.0:
            command = f"AMP:CROSSing:ANAlog:{n}"
            self.send_command(command)
        else:
            raise ValueError("N must be a floating-point value between -1.0 and 1.0.")
    
    def get_crossing_point_analog(self):
        command = "AMP:CROSSing:ANAlog?"
        self.send_command(command)
        response = self.read_response()
        return float(response)
    
    def set_crossing_point_digital(self, n):
        if -1.0 <= n <= 1.0:
            command = f"AMP:CROSSing:DIGital:{n}"
            self.send_command(command)
        else:
            raise ValueError("N must be a floating-point value between -1.0 and 1.0.")
    
    def get_crossing_point_digital(self):
        command = "AMP:CROSSing:DIGital?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def set_gain(self, n):
        if 10.0 <= n <= 23.0:
            command = f"AMP:GAIN:{n}"
            self.send_command(command)
        else:
            raise ValueError("N must be a floating-point value between 10.0 and 23.0.")
    
    def get_gain(self):
        command = "AMP:GAIN?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def set_amplifier_mode(self, mode):
        if mode in [0, 1]:
            command = f"AMP:MODE:{mode}"
            self.send_command(command)
        else:
            raise ValueError("Mode must be 0 (Digital) or 1 (Analog).")

    def get_amplifier_mode(self):
        command = "AMP:MODE?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_amplifier_power(self, state):
        if state in [0, 1]:
            command = f"AMP:POWer:{state}"
            self.send_command(command)
        else:
            raise ValueError("State must be 0 (Off) or 1 (On).")

    def get_amplifier_power_status(self):
        command = "AMP:POWer?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_amplifier_status(self):
        command = "AMP:SETpoint?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_amplifier_swing(self, n):
        command = f"AMP:SWING:{n}"
        self.send_command(command)

    def get_amplifier_swing(self):
        command = "AMP:SWING?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def set_amplifier_swing_vpi(self):
        command = "AMP:SWING:VPI"
        self.send_command(command)

    ### Laser Commands ###

    def set_ITU_channel_number(self, n):
        command = f"LASer:CHANnel:{n}"
        self.send_command(command)

    def get_ITU_channel_number(self):
        command = "LASer:CHANnel?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_dither_on(self):
        command = "LASer:Dither:1"
        self.send_command(command)

    def set_dither_off(self):
        command = "LASer:Dither:0"
        self.send_command(command)

    def get_dither_status(self):
        command = "LASer:Dither?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_fine_tuning_frequency_offset(self, n):
        assert -30000 <= n <= 30000, "N must be an integer between -30,000 and 30,000. Units is MHz."
        command = f"LASer:FINE:{n}"
        self.send_command(command)

    def get_fine_tuning_frequency_offset(self):
        command = "LASer:FINE?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_optical_laser_frequency(self):
        # Output is in GHz
        command = "LASer:FREQuency?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_nominal_laser_frequency(self):
        command = "LASer:FREQ_NOMinal?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_reported_optical_output_power(self):
        # Units is in dBm
        command = "LASer:OOP?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def set_laser_power_on(self):
        command = "LASer:POWer:1"
        self.send_command(command)


    def set_laser_power_off(self):
        command = "LASer:POWer:0"
        self.send_command(command)

    def get_laser_power_status(self):
        command = "LASer:POWer?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def select_c_band_laser(self):
        command = "LASer:SELect:Cband"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def select_l_band_laser(self):
        command = "LASer:SELect:Lband"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def select_1310nm_laser(self):
        command = "LASer:SELect:1310"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_selected_laser(self):
        command = "LASer:SELect?"
        self.send_command(command)
        response = self.read_response()
        return response
    
    def get_laser_status(self):
        command = "LASer:SETpoint?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_measured_optical_output_power_dBm(self):
        command = "LASer:TAP:DBM?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_measured_optical_output_power_mW(self):
        command = "LASer:TAP:MW?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_nominal_laser_wavelength(self):
        command = "LASer:WAVE_NOMinal?"
        self.send_command(command)
        response = self.read_response()
        return int(response)
    
    ## Mach zehnder commands ##

    def get_calibration_status(self):
        command = "MZM:CALibrating?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_dither_amplitude(self, n):
        assert 20<= n <= 2000, "n must be an integer between 20 and 2000. Units of mVpp."
        command = f"MZM:Dither:AMPLitude:{n}"
        self.send_command(command)

    def get_dither_amplitude(self):
        command = "MZM:Dither:AMPLitude?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_dither_frequency(self, n):
        assert 1000 <= n <= 10000, "n must be an integer between 1000 and 10000. Units of Hz."
        command = f"MZM:Dither:FREQuency:{n}"
        self.send_command(command)

    def get_dither_frequency(self):
        command = "MZM:Dither:FREQuency?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_hold_ratio(self, n):
        assert 250 <= n <= 10000, "n must be an integer between 250 and 10000."
        command = f"MZM:HOLD:Ratio:{n}"
        self.send_command(command)

    def get_hold_ratio(self):
        command = "MZM:HOLD:Ratio?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_hold_voltage(self, n):
        assert -10000 <= n <= 10000, "n must be an integer between -10000 and 10000. Units of mV."
        command = f"MZM:HOLD:Voltage:{n}"
        self.send_command(command)

    def get_hold_voltage(self):
        command = "MZM:HOLD:Voltage?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_mzm_bias_mode(self, n):
        # add comments on what each mode does
        assert 0 <= n <= 9, "n must be an integer between 0 and 9."
        command = f"MZM:MODE:{n}"
        self.send_command(command)

    def get_mzm_bias_mode(self):
        command = "MZM:MODE?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def trigger_mzm_calibration(self):
        command = "MZM:RESET"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_mzm_status(self):
        command = "MZM:SETpoint?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_post_mzm_power_dBm(self):
        command = "MZM:TAP:DBM?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_post_mzm_power_mW(self):
        command = "MZM:TAP:MW?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_mzm_bias_voltage(self):
        command = "MZM:Voltage?"
        self.send_command(command)
        response = self.read_response()
        return float(response)
 
    ## System commands ##

    def get_system_bootloader_version(self):
        command = "SYStem:BOOTloader?"
        self.send_command(command)
        response = self.read_response()
        return response

    def get_system_firmware_version(self):
        command = "SYStem:FIRMware?"
        self.send_command(command)
        response = self.read_response()
        return response

    def get_system_hardware_version(self):
        command = "SYStem:HARDware?"
        self.send_command(command)
        response = self.read_response()
        return response

    def get_system_model_number(self):
        command = "SYStem:MODEL?"
        self.send_command(command)
        response = self.read_response()
        return response

    def trigger_restart(self):
        command = "SYStem:RESTART"
        self.send_command(command)

    def get_system_serial_number(self):
        command = "SYStem:SERial?"
        self.send_command(command)
        response = self.read_response()
        return response

    def trigger_sleep(self):
        command = "SYStem:SLEEP"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def trigger_wake(self):
        command = "SYStem:WAKE"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_system_wavelength(self, n):
        assert n in [1310, 1550, 1590], "n must be an integer of 1310, 1550, or 1590. Units in nm."
        command = f"SYStem:WAVElength:{n}"
        self.send_command(command)

    def get_system_wavelength(self):
        command = "SYStem:WAVElength?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_red_led_brightness(self, n):
        assert 0 <= n <= 100, "n must be an integer between 0 and 100."
        command = f"RGB:RED:{n}"
        self.send_command(command)

    def get_red_led_brightness(self):
        command = "RGB:RED?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_green_led_brightness(self, n):
        assert 0 <= n <= 100, "n must be an integer between 0 and 100."
        command = f"RGB:GREEN:{n}"
        self.send_command(command)

    def get_green_led_brightness(self):
        command = "RGB:GREEN?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_blue_led_brightness(self, n):
        assert 0 <= n <= 100, "n must be an integer between 0 and 100."
        command = f"RGB:BLUE:{n}"
        self.send_command(command)

    def get_blue_led_brightness(self):
        command = "RGB:BLUE?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_white_led_brightness(self, n):
        assert 0 <= n <= 100, "n must be an integer between 0 and 100."
        command = f"RGB:WHITE:{n}"
        self.send_command(command)

    def get_white_led_brightness(self):
        command = "RGB:WHITE?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_leds_power_mode(self, n):
        command = f"RGB:POWer:{n}"
        self.send_command(command)

    def get_led_power_status(self):
        command = "RGB:POWer?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    ## VOA commands ##
    def set_optical_attenuation(self, n):
        assert 1.0 <= n <= 20.0, "n must be a float between 1.0 and 20.0. Units in dB."
        command = f"VOA:ATTen:{n}"
        self.send_command(command)

    def get_optical_attenuation(self):
        command = "VOA:ATTen?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_attenuation_error(self):
        command = "VOA:ERRor?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_measured_attenuation(self):
        command = "VOA:MEASured?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def set_voa_mode_constant_output(self):
        command = "VOA:MODE:1"
        self.send_command(command)

    def set_voa_mode_constant_attenuation(self):
        command = "VOA:MODE:0"
        self.send_command(command)

    def get_voa_mode(self):
        command = "VOA:MODE?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def set_optical_output_dbm(self, n):
        assert -20.0 <= n <= 20.0, "n must be a float between -20.0 and 20.0. Units in dBm."
        command = f"VOA:OUTput:DBM:{n}"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_optical_output_dbm(self):
        command = "VOA:OUTput:DBM?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def set_optical_output_mw(self, n):
        assert 0.01 <= n <= 100.0, "n must be a float between 0.01 and 100.0. Units in mW."
        command = f"VOA:OUTput:MW:{n}"
        self.send_command(command)

    def get_optical_output_mw(self):
        command = "VOA:OUTput:MW?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def set_voa_power_on(self):
        command = "VOA:POWer:1"
        self.send_command(command)

    def set_voa_power_off(self):
        command = "VOA:POWer:0"
        self.send_command(command)

    def get_voa_power_status(self):
        command = "VOA:POWer?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_voa_status(self):
        command = "VOA:SETpoint?"
        self.send_command(command)
        response = self.read_response()
        return int(response)

    def get_optical_power_output_dbm(self):
        command = "VOA:TAP:DBM?"
        self.send_command(command)
        response = self.read_response()
        return float(response)

    def get_optical_power_output_mw(self):
        command = "VOA:TAP:MW?"
        self.send_command(command)
        response = self.read_response()
        return float(response)



# Example usage:
# instrument = Instrument("COM3")  # Replace "COM3" with the correct port for your system
# instrument.set_crossing_point_analog(0.5)
# crossing_point = instrument.get_crossing_point_analog()
# print("Crossing point:", crossing_point)
