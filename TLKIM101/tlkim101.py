import os
import time
import sys
import ctypes

POLLTIME = 100 # in milliseconds
NUM_CHANNELS = 4

FORWARD = 0x01
REVERSE = 0x02

class TLKIM101:
    """
    A class to control the Thorlabs KIM101 and KIM001 Inertial Motor Controller.
    Needs Thorlabs.MotionControl.KCube.IntertialMotor.dll.
    """
    def __init__(self, serial_number, dll_path):
        self.serial_number = str(serial_number)
        self.sn_ptr = ctypes.c_char_p(self.serial_number.encode('ascii'))

        if sys.version_info < (3, 8):
            os.chdir(dll_path)
        else:
            os.add_dll_directory(dll_path)
        self._dll = ctypes.cdll.LoadLibrary("Thorlabs.MotionControl.KCube.IntertialMotor.dll")

        self.message_type = ctypes.c_ushort()
        self.message_id = ctypes.c_ushort()
        self.message_data = ctypes.c_ulong()

        self.is_homed=False
        self.is_moving=False

    def build_device_list(self):
        """
        Builds a device list and returns the number of devices found.

        :return: The number of devices found or False if no devices are found.
        :rtype: int or bool
        """
        self._dll.TLI_BuildDeviceList()
        list_size = self._dll.TLI_GetDeviceListSize()
        if list_size == 0:
            print("No devices found")
            return False
        return list_size

    def connect(self, channel):
        """
        Connects to the device and initializes the specified channel.

        :param channel: The channel number to connect.
        :type channel: int
        """
        if self._dll.KIM_Open(self.sn_ptr) == 0:
            print(f"Connected to {self.serial_number}")
            if self._dll.KIM_LoadSettings(self.sn_ptr):
                self._dll.KIM_StartPolling(self.sn_ptr, ctypes.c_int(POLLTIME))
                self._dll.KIM_EnableChannel(self.sn_ptr, ctypes.c_int16(channel))
                time.sleep(3)
                self._dll.KIM_ClearMessageQueue(self.sn_ptr)
            else:
                print("Error loading settings")

    def home(self, channel):
        """
        Homes the specified channel.

        :param channel: The channel number to home.
        :type channel: int
        :return: True if the channel is homed, False otherwise.
        :rtype: bool
        """
        print(f"Homing channel {channel}...")
        try:
            self._dll.KIM_Home(self.sn_ptr, ctypes.c_int16(channel))
        except Exception as e:
            print(f"Failed to home: {e}")
        self.wait_for_move(channel)  # Removed the first 'self' argument
        print("Homed...")
        self.is_homed = True
        return self.is_homed

    def move_absolute(self, channel, position):
        """
        Moves the specified channel to an absolute position.

        :param channel: The channel number to move.
        :type channel: int
        :param position: The position to move to.
        :type position: int
        """
        print(f"Moving channel {channel} to {position}...")
        try:
            self._dll.KIM_MoveAbsolute(self.sn_ptr, ctypes.c_uint16(channel), ctypes.c_int32(position))
            self.wait_for_move(channel)  # Removed 'self' as the first argument
        except Exception as e:
            print(f"Failed to move: {e}")

    def move_relative(self, channel, step_size):
        """
        Moves the specified channel by a relative step size.

        :param channel: The channel number to move.
        :type channel: int
        :param step_size: The step size to move by.
        :type step_size: int
        """
        print(f"Moving channel {channel} by {step_size}...")
        try:
            self._dll.KIM_MoveRelative(self.sn_ptr, ctypes.c_uint16(channel), ctypes.c_int32(step_size))
            self.wait_for_move(channel)  # Removed 'self' as the first argument
        except Exception as e:
            print(f"Failed to move: {e}")

    def move_jog(self, channel, direction):
        """
        Jogs the specified channel in the given direction.

        :param channel: The channel number to jog.
        :type channel: int
        :param direction: The direction to jog (FORWARD or REVERSE).
        :type direction: int
        """
        # direction is FORWARD or REVERSE
        print(f"Jogging channel {channel} in  {direction}...")
        try:
            self._dll.KIM_MoveJog(self.sn_ptr, ctypes.c_uint16(channel), ctypes.c_ubyte(direction))
        except Exception as e:
            print(f"Failed to jog: {e}")

    def move_stop(self, channel):
        """
        Stops the motion of the specified channel.

        :param channel: The channel number to stop.
        :type channel: int
        """
        print(f"Stopping channel {channel}...")
        try:
            self._dll.KIM_MoveStop(self.sn_ptr, ctypes.c_uint16(channel))
        except Exception as e:
            print(f"Failed to stop: {e}")

    def wait_for_move(self, channel):
        """
        Waits for the specified channel to complete its move.

        :param channel: The channel number to wait for.
        :type channel: int
        """
        while self.message_id.value != 0 or self.message_type.value != 2:
            self._dll.KIM_WaitForMessage(self.sn_ptr, ctypes.byref(self.message_type), ctypes.byref(self.message_id), ctypes.byref(self.message_data))

    def disconnect(self):
        """
        Disconnects from the device and releases the specified channel.

        :param channel: The channel number to disconnect.
        :type channel: int
        """
        self._dll.KIM_ClearMessageQueue(self.sn_ptr)
        self._dll.KIM_StopPolling(self.sn_ptr)
        self._dll.KIM_Close(self.sn_ptr)
        print(f"Disconnected from {self.serial_number}")