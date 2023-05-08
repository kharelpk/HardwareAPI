import serial
import time

SUPPORTED_SWEEP_SPEEDS = [50, 60, 80, 100, 120, 150, 160, 200, 300, 400]

class TLX3:
    def __init__(self, com_port):
        self.com_port = com_port
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(
                port=self.com_port,
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
            print(f"Connected to TLX3 at {self.com_port}")
        except Exception as e:
            print(f"Error connecting to TLX3: {str(e)}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print(f"Disconnected from TLX3 at {self.com_port}")

    def send_command(self, command):
        if not self.connection:
            print("Error: Not connected to TLX3.")
            return

        command = command.strip() + '\r'
        self.connection.write(command.encode())
        time.sleep(0.1)
        response = self.connection.readline().decode().strip()
        return response

    def set_laser_on(self,value):
        response = self.send_command(f"LASer:ON: {value}")
        return response

    def get_laser_status(self):
        response = self.send_command("LASer:STATus?")
        return response

    def get_laser_power(self):
        response = self.send_command("LASer:POWer?")
        return response
    
    def get_maximum_wavelength(self):
        response = self.send_command("LASer:RANGE:MAX?")
        return response
    
    def get_minimum_wavelength(self):
        response = self.send_command("LASer:RANGE:MIN?")
        return response
    
    def set_wavelength_offset(self,offset):
        # step is in pm
        assert type(offset) == int
        assert offset >=-10000 and offset <= 10000

        response = self.send_command(f"LASer:STep: {offset}")
        return response
    
    def set_continuous_laser_sweep(self, start_wavelegth, stop_wavelength, sweep_count, speed):
        # sweep_count is in number of steps: 0  is infinite sweeps
        # step is in pm
        assert sweep_count>=0 and sweep_count<=65535
        assert speed in SUPPORTED_SWEEP_SPEEDS

        response = self.send_command(f"LASer:SWeep:Cont: {start_wavelegth},{stop_wavelength},{sweep_count},{speed}")
        return response
    
    def set_laser_sweep_reporting(self, enable_reporting):
        response = self.send_command(f"LASer:SWeep:Report: {1 if enable_reporting else 0}")
        return response

    def get_laser_sweep_status(self):
        response = self.send_command("LASer:SWeep:STATus?")
        return response
    
    def set_stepped_laser_sweep(self, start_wavelegth, stop_wavelength, step_size,sweep_count, dwell_time):
        # wavelength is in pm
        # step is in pm
        # sweep_count is in number of steps: 0  is infinite sweeps
        # dwell_time is in ms
        assert step_size>=1 and step_size<=10000
        assert sweep_count>=0 and sweep_count<=65535

        response = self.send_command(f"LASer:SWeep:STEPped: {start_wavelegth},{stop_wavelength},{step_size},{sweep_count},{dwell_time}")
        return response

    def set_stop_sweep(self):
        response = self.send_command("LASer:SWeep:STOP")
        return response
    
    def set_wavelength(self, wavelength):
        # wavelength is in pm
        response = self.send_command(f"LASer:WAVElength: {wavelength}")
        return response
    
    def get_wavelength(self):
        response = self.send_command("LASer:WAVElength?")
        return response
    
    def get_bootloader_version(self):
        response = self.send_command("SYS:BVER?")
        return response
    
    def get_application_version(self):
        response = self.send_command("SYS:AVER?")
        return response
    
    def get_laser_version(self):
        response = self.send_command("SYS:LVER?")
        return response
    
    def get_part_name(self):
        response = self.send_command("SYS:PARTNAME?")
        return response
    
    def get_product_name(self):
        response = self.send_command("SYS:PRODNAME?")
        return response
    
    def get_serial_number(self):
        response = self.send_command("SYS:SERNUM?")
        return response
    
