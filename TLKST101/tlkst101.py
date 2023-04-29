import os
import time
import sys
import ctypes

POLLTIME = 100 # in milliseconds

class TLKST101:
    """
    A class to control the Thorlabs KCube Stepper Motor Controller.
    Needs Thorlabs.MotionControl.KCube.StepperMotor.dll.
    """
    def __init__(self, serial_number, dll_path):
        self.serial_number = str(serial_number)
        self.sn_ptr = ctypes.c_char_p(self.serial_number.encode('ascii'))

        if sys.version_info < (3, 8):
            os.chdir(dll_path)
        else:
            os.add_dll_directory(dll_path)
        self._dll = ctypes.cdll.LoadLibrary("Thorlabs.MotionControl.KCube.StepperMotor.dll")

        self.message_type = ctypes.c_ushort()
        self.message_id = ctypes.c_ushort()
        self.message_data = ctypes.c_ulong()

        self.is_homed = False
        self.is_moving = False

    def build_device_list(self):
        """
        Builds the device list and returns the number of devices found.
        
        :return: Number of devices found.
        :rtype: int
        """
        self._dll.TLI_BuildDeviceList()
        list_size = self._dll.TLI_GetDeviceListSize()
        if list_size == 0:
            print("No devices found")
        return list_size
    
    def connect(self):
        """
        Connects to the device with the specified serial number and loads its settings.
        """
        if self._dll.SCC_Open(self.sn_ptr) == 0:
            print(f"Connected to {self.serial_number}")
            if self._dll.SCC_LoadSettings(self.sn_ptr):
                self._dll.SCC_StartPolling(self.sn_ptr, ctypes.c_int(POLLTIME))
                self._dll.SCC_EnableChannel(self.sn_ptr)
                time.sleep(3)
                self._dll.SCC_ClearMessageQueue(self.sn_ptr)
            else:
                print("Error loading settings")

    def home(self):
        """
        Homes the device and updates the is_homed attribute.
        
        :return: Homing status.
        :rtype: bool
        """
        print(f"Homing {self.serial_number}...")

        try:
            self._dll.SCC_Home(self.sn_ptr)
        except Exception as e:
            print(f"Failed to home: {e}")
        self.wait_for_move(0)  # Removed the first 'self' argument
        print("Homed...")
        self.is_homed = True
        return self.is_homed
    
    def move_to_position_device_units(self, position):
        """
        Moves the device to the specified position in device units.
        
        :param position: Target position in device units.
        :type position: int
        """
        print(f"Moving to position {position}...")
        try:
            self._dll.SCC_MoveToPosition(self.sn_ptr, ctypes.c_int(position))
        except Exception as e:
            print(f"Failed to move: {e}")
        self.wait_for_move(1)

    
    def wait_for_move(self, num):  # Added 'self' as the first argument
        """
        Waits for the device to complete the move operation.
        
        :param num: Expected message ID value.
        :type num: int
        """
        while self.message_id.value != num or self.message_type.value != 2:
            self._dll.SCC_WaitForMessage(self.sn_ptr, ctypes.byref(self.message_type), ctypes.byref(self.message_id), ctypes.byref(self.message_data))

    def get_device_unit_from_real_value(self, real_value, unit_type):
        """
        Converts real-world units to device units for the specified unit type.
        
        :param real_value: Value in real-world units.
        :type real_value: float
        :param unit_type: Unit type (0: Distance, 1: Velocity, 2: Acceleration).
        :type unit_type: int
        :return: Value in device units.
        :rtype: int
        """
        #unit_type: Distance = 0, Velocity = 1, Acceleration = 2
        device_unit = ctypes.c_int()
        retval = self._dll.SCC_GetDeviceUnitFromRealValue(self.sn_ptr, ctypes.c_double(real_value), ctypes.byref(device_unit), ctypes.c_int(unit_type))
        if retval == 0:
            return device_unit.value
        else:
            print(f"Failed to convert Real to Device unit. Error Code {retval}...")

    def move_to_position_real_units(self, position):
        """
        Moves the device to the specified position in real-world units.
        
        :param position: Target position in real-world units.
        :type position: float
        """
        if self.is_homed:
            device_unit = self.get_device_unit_from_real_value(position, 0)
            self.move_to_position_device_units(device_unit)
        else:
            print("Device not homed...")

    def set_velocity_parameters_real_units(self, acceleration, max_velocity):
        """
        Sets the device's velocity parameters using real-world units.
        
        :param acceleration: Acceleration value in real-world units.
        :type acceleration: float
        :param max_velocity: Maximum velocity value in real-world units.
        :type max_velocity: float
        """
        try:
            acceleration_du = self.get_device_unit_from_real_value(acceleration, 2)
            max_velocity_du = self.get_device_unit_from_real_value(max_velocity, 1)
            retval = self._dll.SCC_SetVelParams(self.sn_ptr, ctypes.c_int(acceleration_du), ctypes.c_int(max_velocity_du))
            if retval != 0:
                print(f"Error setting Velocity Parameters, Error Code: {retval}...")
        except Exception as e:
            print(f"Error setting Velocity Parameters: {e}...")

    def set_velocity_parameters_device_units(self, acceleration, max_velocity):
        """
        Sets the device's velocity parameters using device units.
        
        :param acceleration: Acceleration value in device units.
        :type acceleration: int
        :param max_velocity: Maximum velocity value in device units.
        :type max_velocity: int
        """
        try:
            retval = self._dll.SCC_SetVelParams(self.sn_ptr, ctypes.c_int(acceleration), ctypes.c_int(max_velocity))
            if retval != 0:
                print(f"Error setting Velocity Parameters, Error Code: {retval}...")
        except Exception as e:
            print(f"Error setting Velocity Parameters: {e}...")

    def get_position(self):
        """
        Requests and returns the current position of the device.
        
        :return: Current position of the device.
        :rtype: int
        """
        try:
            retval = self._dll.SCC_RequestPosition(self.sn_ptr)
            if retval == 0:
                time.sleep(0.1)
                current_position = self._dll.SCC_GetPosition(self.sn_ptr)
                return current_position
            else:
                print(f"Error Code: {retval}")
        except Exception as e:
            print(f"Error getting position {e}")

    def disconnect(self):
        """
        Disconnects the device and performs necessary cleanup.
        """
        self._dll.SCC_ClearMessageQueue(self.sn_ptr)
        self._dll.SCC_StopPolling(self.sn_ptr)
        self._dll.SCC_Close(self.sn_ptr)

