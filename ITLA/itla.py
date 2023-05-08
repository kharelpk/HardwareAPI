import serial
import time

class ITLA:
    """
    A class for controlling pure photonics ITLA laser. RS-232 communication is used to control the laser.
    """

    def __init__(self, address:str, baudrate=9600, timeout=1):
        """
        Initialize the ITLA laser object.

        :param address: serial port name
        :param baudrate: baudrate of the serial port
        :param timeout: timeout of the serial port
        """

        self.address = address
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

        # List of registers used for controlling the ITLA
        self.WRITE = 0x01
        self.READ = 0x00
        self.REG_Resena = 0x32
        self.REG_Nop = 0x00
        self.REG_Power = 0x31
        self.REG_Opsl = 0x50
        self.REG_Opsh = 0x51
        self.REG_fcf1 = 0x35
        self.REG_fcf2 = 0x36
        self.REG_lfl1 = 0x52
        self.REG_lfl2 = 0x53
        self.REG_lfh1 = 0x54
        self.REG_lfh2 = 0x55
        self.REG_Ctemp = 0x43
        self.REG_Currents = 0x57
        self.REG_CleanMode = 0x90


    def connect(self) -> int:
        """
        Connect to the laser via serial port.
        """
        try:
            self.ser = serial.Serial(self.address, self.baudrate, timeout=self.timeout)
            return 0
        except serial.SerialException:
            print("Could not open serial port")
            return -1

    def disconnect(self) -> int:
        """
        Disconnect from the laser.
        """
        try:
            self.ser.close()
            return 0
        except serial.SerialException:
            print("Could not close serial port")
            return -1



    def _issue_command(self,register:int, data:int, rw:int) -> int:
        """
        Issue a command to the laser.
        :param register: register number
        :param data: data to be written to the register
        :param rw: read (0) or write(1)
        """

        data_bytes = '{0:016b}'.format(data)
        byte2 = int(data_bytes[0:8],2) #int(data/256)
        byte3 = int(data_bytes[8:16],2) #int(data-byte2*256)
        byte0 = int(self._checksum(rw, register, byte2, byte3))*16+rw

        # Send the command
        self._send_command(byte0, register, byte2, byte3)

        # Receive the command
        response = self._receive_response()

        # Check for AEA
        if (response[0]&0x03) == 0x02:
            print("AEA flag")

        # Decode the response
        self._decode_response(response)

        return 256*response[2]+response[3]

    def _decode_response(self, response: list) -> int:
        """
        Decode the response from the laser.
        :param response: response from the laser
        """
        if response[0] == 0xFF:
            print("Error in response")
            return -1
        else:
            return response[2]*256+response[3]

    def _send_command(self, byte0:int, byte1:int, byte2:int, byte3:int)->None:
        """
        Send a command to the laser.
        :param byte0: read or write
        :param byte1: register number
        :param byte2: third byte of data
        :param byte3: fourth byte of data
        """
        cmd = bytes([byte0,byte1,byte2,byte3])
        self.ser.write(cmd)


    def _receive_response(self) -> int:
        """
        Receive a response with 4 bytes from the laser.
        """
        tstart = time.time()
        while self.ser.inWaiting() < 4:
            if time.time()-tstart > self.timeout:
                print("Timeout")
                break
            time.sleep(0.0001)

        try:
            byte0 = ord(self.ser.read(1))
            byte1 = ord(self.ser.read(1))
            byte2 = ord(self.ser.read(1))
            byte3 = ord(self.ser.read(1))
        except:
            print("Could not read response")
            byte0 = 0xFF
            byte1 = 0xFF
            byte2 = 0xFF
            byte3 = 0xFF
        if self._checksum(byte0, byte1, byte2, byte3) == (byte0)>>4:
            print("Checksum OK")
            return [byte0, byte1, byte2, byte3]
        else:
            print("Checksum Error!")
            return [0xFF, 0xFF, 0xFF, 0xFF]

    def _wait_until_no_operation(self) -> int:
        """
        Wait until the laser is not in operation.
        """
        register = self.REG_Nop
        data=[]

        while data != 16:
            print("Waiting for laser to be ready")
            data = self._issue_command(register,0,0)
            time.sleep(1)
        print("Laser ready")
        return data


    def _checksum(self,byte0, byte1, byte2, byte3) -> int:
        """
        Calculate the checksum of the command. This is in the operating guide
        :param byte0: read or write
        :param register: register number
        :param byte2: third byte of data
        :param byte3: fourth byte of data
        """
        bip8=(byte0 & 0x0f) ^ byte1 ^ byte2 ^ byte3 # & means AND, ^ means XOR
        bip4 =((bip8 & 0xf0)>>4) ^ (bip8 & 0x0f)
        return bip4


    # For now we'll write the commands directly to the serial port. In the future we can use the command dictionary to write commands.
    def set_enable_output(self, value:int) -> int:
        """
        Turn on the laser. Soft enable bit is bit3 so data is 8.
        :param value: 0 or 1
        """

        register = self.REG_Resena

        if value == 1:
            data = 8
        elif value == 0:
            data = 0
        else:
            return -1
        try:
            self._issue_command(register, data,self.WRITE)
            return 0
        except:
            return -1



    def set_power(self, power: int) -> int:
        """
        Set the power of the laser.
        :param power: power in dBm
        """

        register = self.REG_Power
        data = 100*power # per operating guide

        if power >self.min_power and power<=self.max_power:
            try:
                self._issue_command(register, data,self.WRITE)
                return 0
            except:
                return -1
        else:
            print("Power out of range")
            return -1

    def get_power(self) -> int:
        """
        Get the power of the laser in dBm.
        """
        register = self.REG_Power
        return self._issue_command(register,0,self.READ)/100.0

    def set_frequency_THz(self, frequency: float) -> int:
        """
        Set the frequency of the laser.
        :param frequency: frequency in THz
        """
        if frequency >self.min_frequency and frequency<=self.max_frequency:
            register1 = self.REG_fcf1
            register2 = self.REG_fcf2
            data_THz = int(frequency)
            data_GHz = int((frequency-data_THz)*10000) # per operating guide fcf2 has data in 10*GHz
            self._issue_command(register1, data_THz,self.WRITE)
            self._issue_command(register2, data_GHz,self.WRITE)
            return 0
        else:
            print(f"Frequency out of range (min: {self.min_frequency} THz, max: {self.max_frequency} THz)")
            return -1

    def get_frequency_THz(self) -> float:
        """
        Set the frequency of the laser.
        """
        register1 = self.REG_fcf1
        register2 = self.REG_fcf2
        data_THz=self._issue_command(register1, 0,self.READ)
        data_GHz = self._issue_command(register2, 0,self.READ)
        return data_THz+data_GHz/10000

    def set_wavelength_nm(self, wavelength: int) -> int:
        """
        Set the wavelength of the laser.
        :param wavelength: wavelength in nm
        """
        frequency_THz=299792458/(wavelength*1e3)
        return self.set_frequency_THz(frequency_THz)

    def get_wavelength_nm(self, wavelength:int) -> int:
        """
        Get the wavelength of the laser.
        """
        frequency_THz=self.get_frequency_THz()
        return 299792458/(frequency_THz*1e12)*1e9

    def get_temperature(self) -> float:
        """
        Get the temperature of the laser in degrees C.
        """
        register = self.REG_Ctemp
        return self._issue_command(register,0,self.READ)/100.0

    def get_current(self) -> float:
        """
        Get the temperature of the laser in degrees C encoded at 100*C.
        """
        register = self.REG_Currents
        return self._issue_command(register,0,self.READ)/100.0


    def get_min_power(self) -> float:
        """
        Get the minimum power of the laser in dBm.
        """
        register = self.REG_Opsl
        return self._issue_command(register,0,self.READ)/100.0

    def get_max_power(self) -> float:
        """
        Get the maximum power of the laser in dBm.
        """
        register = self.REG_Opsh
        return self._issue_command(register,0,self.READ)/100.0

    def get_min_frequency_THz(self)-> float:
        """
        Get the minimum frequency of the laser in THz.
        """
        register1 = self.REG_lfl1
        register2 = self.REG_lfl2
        data_THz = self._issue_command(register1,0,self.READ)
        data_GHz = self._issue_command(register2,0,self.READ)
        return data_THz+data_GHz/10000.0

    def get_max_frequency_THz(self)-> float:
        """
        Get the maximum frequency of the laser in THz.
        """
        register1 = self.REG_lfh1
        register2 = self.REG_lfh2
        data_THz = self._issue_command(register1,0,self.READ)
        data_GHz = self._issue_command(register2,0,self.READ)
        return data_THz+data_GHz/10000.0

    def set_mode(self, mode: int) -> int:
        """
        Select low noise mode.
        :param mode: mode of the laser 0: standard operation, 1: no-dither operation, 2: whisper-mode operation
        """
        register = self.REG_CleanMode
        try:
            self._issue_command(register, mode,self.WRITE)
            return 0
        except:
            return -1
