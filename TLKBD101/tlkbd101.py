import os
import time
import sys
import ctypes

DWORD = ctypes.c_ulong
WORD = ctypes.c_ushort

POLLTIME = 100 # in milliseconds

class TLKBD101:
    """
    A class to control the Thorlabs KBD101 brushless DC motor.
    """
    def __init__(self, serial_number, dll_path):
        """
        :param serial_number: The serial number of the KBD101 device.
        :type serial_number: str
        :param dll_path: The path to the Thorlabs Kinesis DLL files.
        :type dll_path: str
        """
        self.serial_number = str(serial_number)
        self.sn_ptr = ctypes.c_char_p(self.serial_number.encode('ascii'))

        if sys.version_info < (3, 8):
            os.chdir(dll_path)
        else:
            os.add_dll_directory(dll_path)
        self._dll = ctypes.cdll.LoadLibrary("Thorlabs.MotionControl.KCube.BrushlessMotor.dll")

        self.message_type = ctypes.c_ushort()
        self.message_id = ctypes.c_ushort()
        self.message_data = ctypes.c_ulong()

        self.is_homed = False
        self.is_moving = False


        self._dll.TLI_BuildDeviceList.restype = ctypes.c_short
        self._dll.TLI_GetDeviceListSize.restype = ctypes.c_short
        self._dll.TLI_GetDeviceListByTypeExt.argtypes = [ctypes.c_char_p, DWORD, ctypes.c_int]
        self._dll.TLI_GetDeviceListByTypeExt.restype = ctypes.c_short
        self._dll.BMC_Open.argtypes = [ctypes.c_char_p]
        self._dll.BMC_Open.restype = ctypes.c_short
        self._dll.BMC_LoadSettings.argtypes = [ctypes.c_char_p]
        self._dll.BMC_LoadSettings.restype = ctypes.c_bool
        self._dll.BMC_StartPolling.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.BMC_StartPolling.restype = ctypes.c_bool
        self._dll.BMC_EnableChannel.argtypes = [ctypes.c_char_p]
        self._dll.BMC_EnableChannel.restype = ctypes.c_short
        self._dll.BMC_ClearMessageQueue.argtypes = [ctypes.c_char_p]
        self._dll.BMC_ClearMessageQueue.restype = ctypes.c_short
        self._dll.BMC_Home.argtypes = [ctypes.c_char_p]
        self._dll.BMC_Home.restype = ctypes.c_short
        self._dll.BMC_WaitForMessage.argtypes = [ctypes.c_char_p, ctypes.POINTER(WORD), ctypes.POINTER(WORD), ctypes.POINTER(DWORD)]
        self._dll.BMC_WaitForMessage.restype = ctypes.c_bool
        self._dll.BMC_MoveToPosition.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._dll.BMC_MoveToPosition.restype = ctypes.c_short
        self._dll.BMC_GetDeviceUnitFromRealValue.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self._dll.BMC_GetDeviceUnitFromRealValue.restype = ctypes.c_short
        self._dll.BMC_SetVelParams.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        self._dll.BMC_SetVelParams.restype = ctypes.c_short
        self._dll.BMC_RequestPosition.argtypes = [ctypes.c_char_p]
        self._dll.BMC_RequestPosition.restype = ctypes.c_short
        self._dll.BMC_GetPosition.restype = ctypes.c_int
        self._dll.BMC_SetMotorParamsExt.argtypes = [ctypes.c_char_p,ctypes.c_double]
        self._dll.BMC_SetMotorParamsExt.restype = ctypes.c_short
        self._dll.BMC_ClearMessageQueue.argtypes = [ctypes.c_char_p]
        self._dll.BMC_ClearMessageQueue.restype = ctypes.c_short
        self._dll.BMC_StopPolling.argtypes=[ctypes.c_char_p]
        self._dll.BMC_Close.argtypes=[ctypes.c_char_p]

        

    def build_device_list(self):
        """
        Build the device list.

        :return: The number of devices in the device list.
        :rtype: int
        """
        self._dll.TLI_BuildDeviceList()
        list_size = self._dll.TLI_GetDeviceListSize()
        if list_size == 0:
            print("No devices found...")
        else:
            tl_c_buf_size = 255
            dev_id = ctypes.c_int(26)
            s_buf = ctypes.c_buffer(tl_c_buf_size)

            if self._dll.TLI_GetDeviceListByTypeExt(s_buf,tl_c_buf_size, dev_id) != 0:
                print("No devices of type {} found".format(dev_id))
                return
            self.serial_number_list = s_buf.value.decode('ascii').split(',')[0:-1]
       
            if self.serial_number not in self.serial_number_list:
                print(f"No device with serial number {self.serial_number} found...")
                return
        return list_size

    def connect(self):
        """
        Connect to the KBD101 device.
        """
        if self._dll.BMC_Open(self.sn_ptr) == 0:
            print("Connected to {}...".format(self.serial_number))
            if self._dll.BMC_LoadSettings(self.sn_ptr):
                self._dll.BMC_StartPolling(self.sn_ptr, ctypes.c_int(POLLTIME))
                self._dll.BMC_EnableChannel(self.sn_ptr)
                time.sleep(3)
                self._dll.BMC_ClearMessageQueue(self.sn_ptr)
            else:
                print("Failed to Load settings...")

    def home(self):
        """
        Home the KBD101 device.

        :return: Whether the homing is successful.
        :rtype: bool
        """
        print("Homing {}...".format(self.serial_number))
        try:
            self._dll.BMC_Home(self.sn_ptr)
        except Exception as e:
            print("Failed to Home: {}".format(e))
        while self.message_id.value != 0 or self.message_type.value != 2:
            self._dll.BMC_WaitForMessage(self.sn_ptr, ctypes.byref(self.message_type), ctypes.byref(self.message_id), ctypes.byref(self.message_data))
        print("Homed...")
        self.is_homed = True
        return self.is_homed
    
    def move_to_position_device_units(self, position):
        """
        Move the motor to the given position in device units.

        :param position: The position in device units.
        :type position: int
        """
        if self.is_homed:
            print(f"Moving to {position}...")
            try:
                retval = self._dll.BMC_MoveToPosition(self.sn_ptr, ctypes.c_int(position))
                if retval != 0:
                    print(f"Error Moving to Position. Error Code: {retval}...")
            except Exception as e:
                print(f"Error when Moving to {position}: {e}")
                while self.message_id.value != 1 or self.message_type.value != 2:
                    self._dll.BMC_WaitForMessage(self.sn_ptr, ctypes.byref(self.message_type), ctypes.byref(self.message_id), ctypes.byref(self.message_data))
            print("Moved...")

    def get_device_unit_from_real_value(self, real_value, unit_type):
        """
        Convert a real value to device units.

        :param real_value: The real value to convert.
        :type real_value: float
        :param unit_type: The unit type (0: Distance, 1: Velocity, 2: Acceleration).
        :type unit_type: int
        :return: The value in device units.
        :rtype: int
        """
        device_unit = ctypes.c_int()
        retval = self._dll.BMC_GetDeviceUnitFromRealValue(self.sn_ptr, ctypes.c_double(real_value), ctypes.byref(device_unit), ctypes.c_int(unit_type))
        if retval == 0:
            return device_unit.value
        else:
            print(f"Failed to convert Real to Device unit. Error Code {retval}...")

    def move_to_position_real_units(self, position):
        """
        Move the motor to the given position in real units.

        :param position: The position in real units.
        :type position: float
        """
        if self.is_homed:
            device_unit = self.get_device_unit_from_real_value(position, 0)
            self.move_to_position_device_units(device_unit)
        else:
            print("Device not homed...")

    def set_velocity_parameters_real_units(self, acceleration, max_velocity):
        """
        Set the velocity parameters of the motor in real units.

        :param acceleration: The acceleration in real units.
        :type acceleration: float
        :param max_velocity: The maximum velocity in real units.
        :type max_velocity: float
        """
        try:
            acceleration_du = self.get_device_unit_from_real_value(acceleration, 2)
            max_velocity_du = self.get_device_unit_from_real_value(max_velocity, 1)
            retval = self._dll.BMC_SetVelParams(self.sn_ptr, ctypes.c_int(acceleration_du), ctypes.c_int(max_velocity_du))
            if retval != 0:
                print(f"Error setting Velocity Parameters, Error Code: {retval}...")
        except Exception as e:
            print(f"Error setting Velocity Parameters: {e}...")

    def set_velocity_parameters_device_units(self, acceleration, max_velocity):
        """
        Set the velocity parameters of the motor in device units.

        :param acceleration: The acceleration in device units.
        :type acceleration: int
        :param max_velocity: The maximum velocity in device units.
        :type max_velocity: int
        """
        try:
            retval = self._dll.BMC_SetVelParams(self.sn_ptr, ctypes.c_int(acceleration), ctypes.c_int(max_velocity))
            if retval != 0:
                print(f"Error setting Velocity Parameters, Error Code: {retval}...")
        except Exception as e:
            print(f"Error setting Velocity Parameters: {e}...")
    
    def get_position(self):
        """
        Get the current position of the motor.

        :return: The current position of the motor in device units.
        :rtype: int
        """
        try:
            retval = self._dll.BMC_RequestPosition(self.sn_ptr)
            if retval == 0:
                time.sleep(0.1)
                current_position = self._dll.BMC_GetPosition(self.sn_ptr)
                return current_position
            else:
                print(f"Error Code: {retval}")
        except Exception as e:
            print(f"Error getting position {e}")

    def set_motor_params(self, counts_per_rev):
        """
        Set the motor parameters (counts per revolution).

        :param counts_per_rev: The counts per revolution.
        :type counts_per_rev: float
        """
        try:
            retval = self._dll.BMC_SetMotorParamsExt(self.sn_ptr, ctypes.c_double(counts_per_rev))
            if retval == 0:
                print("Motor Parameters Set...")
            else:
                print("Failed to set motor parameters, Error code: {}...".format(retval))
        except Exception as e:
            print(e)

    def disconnect(self):
        """
        Disconnect from the KBD101 device.
        """
        self._dll.BMC_ClearMessageQueue(self.sn_ptr)
        self._dll.BMC_StopPolling(self.sn_ptr)
        self._dll.BMC_Close(self.sn_ptr)


    