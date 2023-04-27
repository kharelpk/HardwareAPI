import ctypes
from typing import List, Any, Tuple

# Define the ctypes for the required data types
ViStatus = ctypes.c_long
ViRsrc = ctypes.c_char_p
ViBoolean = ctypes.c_int
ViSession = ctypes.c_long
ViPSession = ctypes.POINTER(ctypes.c_long)
ViPUInt32 = ctypes.POINTER(ctypes.c_uint32)
ViUInt32 = ctypes.c_uint32
ViChar = ctypes.c_char
ViReal64 = ctypes.c_double
ViPReal64 = ctypes.POINTER(ctypes.c_double)
ViInt16 = ctypes.c_int16
ViInt32 = ctypes.c_int32
ViPInt32 = ctypes.POINTER(ctypes.c_int32)
ViReal32 = ctypes.c_float
ViUInt16 = ctypes.c_uint16


class DLLWrapper:
    def __init__(self, dll_path: str):
        self._dll = ctypes.CDLL(dll_path)

    def _bind_functions(self, function_bindings: List[Tuple[str, List[Any], Any]]) -> None:
        for name, argtypes, restype in function_bindings:
            self._bind_function(name, argtypes, restype)

    def _bind_function(self, name: str, argtypes: List[Any], restype: Any) -> None:
        # Bind the function with ctypes
        func = getattr(self._dll, name)
        func.argtypes = argtypes
        func.restype = restype


class TLUP(DLLWrapper):
    def __init__(self, dll_path: str):
        super().__init__(dll_path)

        self._bind_functions([
            ("TLUP_init", [ViRsrc, ViBoolean, ViBoolean, ViPSession], ViStatus),
            ("TLUP_close", [ViSession], ViStatus),
            ("TLUP_errorMessage", [ViSession, ViStatus, ctypes.POINTER(ViChar)], ViStatus),
            ("TLUP_findRsrc", [ViSession, ViPUInt32], ViStatus),
            ("TLUP_getRsrcInfo", [ViSession, ViUInt32, ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViBoolean)], ViStatus),
            ("TLUP_measDeviceTemperature", [ViSession, ViPReal64], ViStatus),
            ("TLUP_switchLedOutput", [ViSession , ViBoolean], ViStatus),
            ("TLUP_setLedCurrentSetpoint", [ViSession, ViReal64],ViStatus),
        ])

    def init(self, resource_name: str, id_query: bool, reset_device: bool) -> int:
        """
        Initializes the instrument driver session and performs the following initialization actions:
        1. Opens a session to the Default Resource Manager resource and a session to the selected device using the Resource Name.
        2. Performs an identification query on the Instrument.
        3. Resets the instrument to a known state.
        4. Sends initialization commands to the instrument.
        5. Returns an instrument handle which is used to differentiate between different sessions of this instrument driver.

        :param resource_name: Specifies the interface of the device that is to be initialized.
        :type resource_name: str
        :param id_query: Performs an In-System Verification. Checks if the resource matches the BP2 vendor and product id.
        :type id_query: bool
        :param reset_device: Performs Reset operation and places the instrument in a pre-defined reset state.
        :type reset_device: bool
        :return: The instrument handle that is used in all subsequent calls to distinguish between different sessions of this instrument driver.
        :rtype: int

        :raises NameError: If there is an error during initialization.
        """
        instrument_handle = ViSession()
        status = self._dll.TLUP_init(ViRsrc(resource_name.encode()),
                                      ViBoolean(id_query),
                                      ViBoolean(reset_device),
                                      ctypes.byref(instrument_handle))

        self.__test_for_error(instrument_handle, status)
        return instrument_handle.value
    
    def close(self, instrument_handle: int) -> None:
        """
        Terminates the instrument driver session and deallocates any resources that were allocated by the init operation.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :raises NameError: If there is an error during the close operation.
        """
        status = self._dll.TLUP_close(ViSession(instrument_handle))
        self.__test_for_error(ViSession(instrument_handle), status)
        return None

    
    def find_rsrc(self, instrument_handle: int) -> int:
        """
        Finds all devices attached to the PC and supported by this driver.
        Returns the number of connected devices, including devices that are currently in use.

        :param instrument_handle: Pass 0 to this parameter.
        :type instrument_handle: int
        :return: The number of connected devices that are supported by this driver.
        :rtype: int

        :raises NameError: If there is an error during the resource search.

        Note:
        (1) The function additionally stores information like system name about the found resources internally.
            This information can be retrieved with other functions from the class, e.g. <Get Resource Name> and <Get Resource Information>.
        """
        resource_count = ViUInt32()
        status = self._dll.TLUP_findRsrc(ViSession(instrument_handle),
                                         ctypes.byref(resource_count))

        self.__test_for_error(ViSession(instrument_handle), status)
        return resource_count.value
    
    
    def get_rsrc_info(self, instrument_handle: int, index: int) -> Tuple[str, str, str, bool]:
        """
        Gets information about a resource found with <Find Resources>.
        
        :param instrument_handle: Pass 0 to this parameter.
        :type instrument_handle: int
        :param index: The index of the UP device to get the resource information from.
        :type index: int
        :return: Tuple containing model_name, serial_number, manufacturer, and resource_availability.
        :rtype: Tuple[str, str, str, bool]

        :raises NameError: If there is an error during the resource information retrieval.

        Note:
        (1) The index is zero-based. The maximum index to be used here is one less than the number of UP devices connected.
            The number of UP devices is available by calling <Find Resource>.
        """
        model_name = ctypes.create_string_buffer(256)
        serial_number = ctypes.create_string_buffer(256)
        manufacturer = ctypes.create_string_buffer(256)
        resource_available = ViBoolean()

        status = self._dll.TLUP_getRsrcInfo(ViSession(instrument_handle),
                                            ViUInt32(index),
                                            model_name,
                                            serial_number,
                                            manufacturer,
                                            ctypes.byref(resource_available))

        self.__test_for_error(instrument_handle, status)
        return (model_name.value.decode(),
                serial_number.value.decode(),
                manufacturer.value.decode(),
                bool(resource_available.value))



    def measure_device_temperature(self, instrument_handle: int) -> float:
        """
        Obtains the device internal temperature.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :return: The internal device temperature in the selected temperature unit (default is degree Celsius).
        :rtype: float

        :raises NameError: If there is an error during the measurement of the device temperature.

        Note:
        This function is used to obtain the device internal temperature.
        """
        device_temperature = ViReal64()

        status = self._dll.TLUP_measDeviceTemperature(ViSession(instrument_handle),
                                                      ctypes.byref(device_temperature))

        self.__test_for_error(ViSession(instrument_handle), status)
        return device_temperature.value
    
    def switch_led_output(self, instrument_handle: int, enable_led_output: bool) -> None:
        """
        Enables or disables the LED output.
        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param enable_led_output: True to enable the LED output, False to disable the LED output.
        :type enable_led_output: bool

        :raises NameError: If there is an error during the switching of the LED output.

        Note:
        This function is valid for UP LED.
        """
        status = self._dll.TLUP_switchLedOutput(ViSession(instrument_handle),
                                                ViBoolean(enable_led_output))

        self.__test_for_error(ViSession(instrument_handle), status)
        return None
    

    def set_led_current_setpoint(self, instrument_handle: int, led_current_setpoint: float) -> None:
        """
        Sets the LED current setpoint.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param led_current_setpoint: The LED current setpoint in Ampere.
        :type led_current_setpoint: float

        :raises NameError: If there is an error during the setting of the LED current setpoint.

        Note:
        (1) This function is valid for UP LED.
        """
        status = self._dll.TLUP_setLedCurrentSetpoint(ViSession(instrument_handle),
                                                      ViReal64(led_current_setpoint))

        self.__test_for_error(ViSession(instrument_handle), status)
        return None

    def __test_for_error(self, instrument_handle, status):
        if status < 0:
            self.__throw_error(instrument_handle, status)
            

    def __throw_error(self,instrument_handle, status):
        error_message = ctypes.create_string_buffer(256)
        if status < 0:
            self._dll.TLUP_errorMessage(instrument_handle,
                                         status, 
                                         error_message)
            raise NameError(error_message.value.decode())

