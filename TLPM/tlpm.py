import ctypes
from typing import List, Any, Tuple

# Define the ctypes for the required data types
ViStatus = ctypes.c_long
ViRsrc = ctypes.c_char_p
ViBoolean = ctypes.c_bool
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


class TLPM(DLLWrapper):
    def __init__(self, dll_path: str):
        super().__init__(dll_path)

        self._bind_functions([
                ("TLPM_init", [ViRsrc, ViBoolean, ViBoolean, ViPSession], ViStatus),
                ("TLPM_close", [ViSession], ViStatus),
                ("TLPM_errorMessage", [ViSession, ViStatus, ctypes.POINTER(ViChar)], ViStatus),
                ("TLPM_identificationQuery", [ViSession, ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar)], ViStatus),
                ("TLPM_setAvgTime", [ViSession, ViReal64], ViStatus),
                ("TLPM_setWavelength", [ViSession, ViReal64], ViStatus),
                ("TLPM_setPowerAutoRange", [ViSession, ViBoolean], ViStatus),
                ("TLPM_measPower", [ViSession, ViPReal64], ViStatus)
        ]) 


    def init(self, resource_name: str, id_query: bool, reset_device: bool) -> int:
        """
        Initializes the instrument driver session and performs the following initialization actions:
        1. Opens a session to the Default Resource Manager resource and a session to the selected device using the Resource Name.
        2. Performs an identification query on the Instrument.
        3. Resets the instrument to a known state.
        4. Sends initialization commands to the instrument.
        5. Returns an instrument handle which is used to differentiate between different sessions of this instrument driver.

        :param resource_name: Specifies the interface of the device that is to be initialized. The syntax for the Instrument Descriptor for USB interfaces:
        USB[board]::0x1313::product id::serial number[::interface number][::INSTR]
        :type resource_name: str
        :param id_query: This parameter specifies whether an identification query is performed during initialization.
        :type id_query: bool
        :param reset_device: This parameter specifies whether the instrument is reset during initialization.
        :type reset_device: bool
        :return: The instrument handle that is used in all subsequent calls to distinguish between different sessions of this instrument driver.
        :rtype: int

        :raises NameError: If there is an error during initialization.
        """
        instrument_handle = ViSession()
        status = self._dll.TLPM_init(ViRsrc(resource_name.encode()),
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
        status = self._dll.TLPM_close(ViSession(instrument_handle))
        self.__test_for_error(ViSession(instrument_handle), status)
        return None

    def identification_query(self, instrument_handle: int) -> Tuple[str, str, str, str]:
        """
        Returns the device identification information.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :return: A tuple containing the manufacturer name, device name, serial number, and firmware revision of the device.
        :rtype: Tuple[str, str, str, str]

        :raises NameError: If there is an error during the identification query operation.
        """
        manufacturer_name = ctypes.create_string_buffer(256)
        device_name = ctypes.create_string_buffer(256)
        serial_number = ctypes.create_string_buffer(256)
        firmware_revision = ctypes.create_string_buffer(256)

        status = self._dll.TLPM_identificationQuery(
            ViSession(instrument_handle),
            manufacturer_name,
            device_name,
            serial_number,
            firmware_revision
        )

        self.__test_for_error(ViSession(instrument_handle), status)

        return (
            manufacturer_name.value.decode(),
            device_name.value.decode(),
            serial_number.value.decode(),
            firmware_revision.value.decode()
        )

    def set_avg_time(self, instrument_handle: int, average_time: float) -> None:
        """
        Sets the average time for measurement value generation.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param average_time: The average time in seconds. The value will be rounded to the closest multiple of the device's internal sampling rate.
        :type average_time: float

        :raises NameError: If there is an error during the set average time operation.
        """
        status = self._dll.TLPM_setAvgTime(ViSession(instrument_handle), ViReal64(average_time))
        self.__test_for_error(ViSession(instrument_handle), status)
        return None

    def set_wavelength(self, instrument_handle: int, wavelength: float) -> None:
        """
        Sets the user's wavelength in nanometers (nm).

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param wavelength: The user's wavelength in nanometers (nm). Wavelength set value is used for calculating power.
        :type wavelength: float

        :raises NameError: If there is an error during the set wavelength operation.
        """
        status = self._dll.TLPM_setWavelength(ViSession(instrument_handle), ViReal64(wavelength))
        self.__test_for_error(ViSession(instrument_handle), status)
        return None

    def set_power_auto_range(self, instrument_handle: int, power_auto_range_mode: bool) -> None:
        """
        Sets the power auto range mode.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param power_auto_range_mode: The power auto range mode. Set to True for power auto range enabled and False for power auto range disabled.
        :type power_auto_range_mode: bool

        :raises NameError: If there is an error during the set power auto range operation.
        """
        status = self._dll.TLPM_setPowerAutoRange(ViSession(instrument_handle), ViBoolean(power_auto_range_mode))
        self.__test_for_error(ViSession(instrument_handle), status)
        return None

    def meas_power(self, instrument_handle: int) -> float:
        """
        Obtains power readings from the instrument.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :return: The power in the selected unit.
        :rtype: float

        :raises NameError: If there is an error during the power measurement operation.
        """
        power = ViReal64()
        status = self._dll.TLPM_measPower(ViSession(instrument_handle), ctypes.byref(power))
        self.__test_for_error(ViSession(instrument_handle), status)
        return power.value

    def __test_for_error(self, instrument_handle, status):
        if status < 0:
            self.__throw_error(instrument_handle, status)
            

    def __throw_error(self,instrument_handle, status):
        error_message = ctypes.create_string_buffer(512)
        if status < 0:
            self._dll.TLPM_errorMessage(instrument_handle,
                                         status, 
                                         error_message)
            raise NameError(error_message.value.decode())

