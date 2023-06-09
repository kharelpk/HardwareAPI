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


class TLDC4100(DLLWrapper):
    def __init__(self, dll_path: str):
        super().__init__(dll_path)

        self._bind_functions([
            ("TLDC4100_init", [ViRsrc, ViBoolean, ViBoolean, ViPSession], ViStatus),
            ("TLDC4100_close", [ViSession], ViStatus),  
            ("TLDC4100_error_message", [ViSession, ViStatus, ctypes.POINTER(ViChar)], ViStatus), 
            ("TLDC4100_identificationQuery", [ViSession, ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar)], ViStatus),
            ("TLDC4100_getHeadInfo", [ViSession, ViInt32, ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ViPInt32], ViStatus),
            ("TLDC4100_setLedOnOff", [ViSession, ViInt32, ViBoolean], ViStatus),
            ("TLDC4100_setPercentalBrightness", [ViSession, ViInt32, ViReal32], ViStatus)

        ])

    def init(self, resource_name: str, id_query: bool, reset_device: bool) -> int:
        """
        Initializes the instrument driver session and performs the following initialization actions:
        1. Opens a session to the Default Resource Manager resource and a session to the selected device using the Resource Name.
        2. Performs an identification query on the Instrument.
        3. Resets the instrument to a known state.
        4. Sends initialization commands to the instrument.
        5. Returns an instrument handle which is used to differentiate between different sessions of this instrument driver.

        :param resource_name: Specifies the interface of the device that is to be initialized. The ASRL keyword is used for serial communication. Default Value:  "ASRL1::INSTR"
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
        status = self._dll.TLDC4100_init(ViRsrc(resource_name.encode()),
                                      ViBoolean(id_query),
                                      ViBoolean(reset_device),
                                      ctypes.byref(instrument_handle))
        
        self._test_for_error(instrument_handle, status)
        return instrument_handle.value


    def close(self, instrument_handle: int) -> None:
        """
        Terminates the instrument driver session and deallocates any resources that were allocated by the init operation.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :raises NameError: If there is an error during the close operation.
        """
        status = self._dll.TLDC4100_close(ViSession(instrument_handle))
        self._test_for_error(instrument_handle, status)
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

        status = self._dll.TLDC4100_identificationQuery(
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

    def get_head_info(self, instrument_handle: int, channel: int) -> Tuple[str, str, int]:
        """
        Returns the LED head identification information for the specified channel.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param channel: The LED channel. The channel index is zero-based (first channel has index zero).
                        Range: 0 ... 3
                        Default: 0
        :type channel: int

        :return: A tuple containing the serial number, name, and type of the connected LED head.
        :rtype: Tuple[str, str, int]

        :raises NameError: If there is an error during the get_head_info operation.
        """
        serial_number = ctypes.create_string_buffer(256)
        name = ctypes.create_string_buffer(256)
        led_head_type = ViInt32()

        status = self._dll.TLDC4100_getHeadInfo(
            ViSession(instrument_handle),
            ViInt32(channel),
            serial_number,
            name,
            ctypes.byref(led_head_type)
        )

        self.__test_for_error(ViSession(instrument_handle), status)

        return (
            serial_number.value.decode(),
            name.value.decode(),
            led_head_type.value
        )
    
    def set_led_on_off(self, instrument_handle: int, channel: int, led_on_off: bool) -> None:
        """
        Sets one or all LED(s) on or off.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param channel: The LED channel. The channel index is zero-based (first channel has index zero). You may pass ALL_CHANNELS (-1) to specify all channels at once.
                        Range: -1 ... 3
                        Default: 0
        :type channel: int
        :param led_on_off: This parameter specifies the LED output. On switches the LED on, off switches the LED off.
        :type led_on_off: bool

        :raises NameError: If there is an error during the set_led_on_off operation.
        """
        status = self._dll.TLDC4100_setLedOnOff(
            ViSession(instrument_handle),
            ViInt32(channel),
            ViBoolean(led_on_off)
        )

        self.__test_for_error(ViSession(instrument_handle), status)
        return None
    
    def set_percental_brightness(self, instrument_handle: int, channel: int, brightness: float) -> None:
        """
        Sets the percental brightness for one or all LED channel(s). The maximum brightness current is defined due to the user limit current.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param channel: The LED channel. The channel index is zero-based (first channel has index zero). You may pass ALL_CHANNELS (-1) to set the percental brightness for all channels with one command.
                        Range: -1 ... 3
                        Default: 0
        :type channel: int
        :param brightness: The percental brightness.
                           Range: 0.0..100.0 (%)
                           Default: 0.0 (%)
        :type brightness: float

        :raises NameError: If there is an error during the set_percental_brightness operation.
        """
        status = self._dll.TLDC4100_setPercentalBrightness(
            ViSession(instrument_handle),
            ViInt32(channel),
            ViReal32(brightness)
        )

        self.__test_for_error(ViSession(instrument_handle), status)
        return None


    def __test_for_error(self, instrument_handle, status):
        if status < 0:
            self.__throw_error(instrument_handle, status)
            

    def __throw_error(self,instrument_handle, status):
        error_message = ctypes.create_string_buffer(512)
        if status < 0:
            self._dll.TLDC4100_error_message(instrument_handle,
                                         status, 
                                         error_message)
            raise NameError(error_message.value.decode())
