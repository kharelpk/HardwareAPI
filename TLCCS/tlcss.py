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

NUM_PIXELS= 3648


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


class TLCCS(DLLWrapper):
    def __init__(self, dll_path: str):
        super().__init__(dll_path)

        self._bind_functions([
                ("tlccs_init", [ViRsrc, ViBoolean, ViBoolean, ViPSession], ViStatus),
                ("tlccs_close", [ViSession], ViStatus),
                ("tlccs_errorMessage", [ViSession, ViStatus, ctypes.POINTER(ViChar)], ViStatus),
                ("tlccs_identificationQuery", [ViSession, ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar)], ViStatus),
                ("tlccs_setIntegrationTime", [ViSession, ViReal64], ViStatus), 
                ("tlccs_startScan", [ViSession], ViStatus),  
                ("tlccs_getScanData", [ViSession, ctypes.POINTER(ViReal64)], ViStatus), 
                ("tlccs_getWavelengthData", [ViSession, ViInt16, ctypes.POINTER(ViReal64), ViPReal64, ViPReal64], ViStatus)
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
        status = self._dll.tlccs_init(ViRsrc(resource_name.encode()),
                                      ViBoolean(id_query),
                                      ViBoolean(reset_device),
                                      ctypes.byref(instrument_handle))
        
        self.__test_for_error(instrument_handle, status)
        return instrument_handle.value

    def identification_query(self, instrument_handle: int) -> Tuple[str, str, str, str, str]:
        """
        Returns the device identification information.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :return: A tuple containing the manufacturer name, device name, serial number, firmware revision, and instrument driver revision of the device.
        :rtype: Tuple[str, str, str, str, str]

        :raises NameError: If there is an error during the identification query operation.
        """
        manufacturer_name = ctypes.create_string_buffer(256)
        device_name = ctypes.create_string_buffer(256)
        serial_number = ctypes.create_string_buffer(256)
        firmware_revision = ctypes.create_string_buffer(256)
        instrument_driver_revision = ctypes.create_string_buffer(256)  # Added buffer

        status = self._dll.tlccs_identificationQuery(
            ViSession(instrument_handle),
            manufacturer_name,
            device_name,
            serial_number,
            firmware_revision,
            instrument_driver_revision  # Added buffer as argument
        )

        self.__test_for_error(ViSession(instrument_handle), status)

        return (
            manufacturer_name.value.decode(),
            device_name.value.decode(),
            serial_number.value.decode(),
            firmware_revision.value.decode(),
            instrument_driver_revision.value.decode()  # Added value to the return tuple
        )
    def close(self, instrument_handle: int) -> None:
        """
        Terminates the instrument driver session and deallocates any resources that were allocated by the init operation.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :raises NameError: If there is an error during the close operation.
        """
        status = self._dll.tlccs_close(ViSession(instrument_handle))
        self.__test_for_error(ViSession(instrument_handle), status)
        return None
    
    def set_integration_time(self, instrument_handle: int, integration_time: float) -> None:
        """
        Sets the optical integration time in seconds [s].

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param integration_time: The optical integration time for the CCS in seconds [s]. Valid range: CCS_SERIES_MIN_INT_TIME (1.0E-5) ... CCS_SERIES_MAX_INT_TIME (6.0E+1). Default value: 1.0E-3.
        :type integration_time: float

        :raises NameError: If there is an error during the set integration time operation.

        .. note:: This function sets the optical integration time in seconds [s].
        """
        status = self._dll.tlccs_setIntegrationTime(
            ViSession(instrument_handle),
            ViReal64(integration_time)
        )

        self.__test_for_error(ViSession(instrument_handle), status)
        return None
    

    def start_scan(self, instrument_handle: int) -> None:
        """
        Triggers the CCS to take one single scan.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :raises NameError: If there is an error during the start scan operation.

        .. note:: The scan data can be read out with the function 'Get Scan Data'. Use 'Get Device Status' to check the scan status.
        """
        status = self._dll.tlccs_startScan(
            ViSession(instrument_handle)
        )

        self.__test_for_error(ViSession(instrument_handle), status)
        return None
    
    def get_scan_data(self, instrument_handle: int) -> List[float]:
        """
        Reads out the processed scan data.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :return: A list containing the processed scan data.
        :rtype: List[float]

        :raises NameError: If there is an error during the get scan data operation, or if the raw scan data is overexposed and proper data processing is not possible.

        .. note:: When the raw scan data is overexposed, so that a proper data processing is not possible, the function returns VI_ERROR_SCAN_DATA_INVALID and all data points are set to zero (0.0).
        """
        scan_data = (ViReal64 * NUM_PIXELS)()

        status = self._dll.tlccs_getScanData(
            ViSession(instrument_handle),
            scan_data
        )

        self.__test_for_error(ViSession(instrument_handle), status)
        return list(scan_data)
    
    def get_wavelength_data(self, instrument_handle: int, data_set: int) -> Tuple[List[float], float, float]:
        """
        Returns data for the pixel-wavelength correlation, including maximum and minimum wavelengths.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int
        :param data_set: Specifies which calibration data set has to be used for generating the wavelength data array.
        :type data_set: int

        :return: A tuple containing the wavelength data array, the minimum wavelength, and the maximum wavelength.
        :rtype: Tuple[List[float], float, float]

        :raises NameError: If there is an error during the get wavelength data operation.

        .. note:: The value returned in Wavelength_Data_Array[0] is the wavelength at pixel 1, this is also the minimum wavelength, the value returned in Wavelength_Data_Array[1] is the wavelength at pixel 2 and so on until Wavelength_Data_Array[CCS_SERIES_NUM_PIXELS-1] which provides the wavelength at pixel CCS_SERIES_NUM_PIXELS (3648). This is the maximum wavelength.
        """
        wavelength_data_array = (ViReal64 * NUM_PIXELS)()
        minimum_wavelength = ViReal64()
        maximum_wavelength = ViReal64()

        status = self._dll.tlccs_getWavelengthData(
            ViSession(instrument_handle),
            ViInt16(data_set),
            wavelength_data_array,
            ctypes.byref(minimum_wavelength),
            ctypes.byref(maximum_wavelength)
        )

        self.__test_for_error(ViSession(instrument_handle), status)
        return list(wavelength_data_array), minimum_wavelength.value, maximum_wavelength.value

    def __test_for_error(self, instrument_handle, status):
        if status < 0:
            self.__throw_error(instrument_handle, status)
            

    def __throw_error(self,instrument_handle, status):
        error_message = ctypes.create_string_buffer(512)
        if status < 0:
            self._dll.tlccs_errorMessage(instrument_handle,
                                         status, 
                                         error_message)
            raise NameError(error_message.value.decode())
