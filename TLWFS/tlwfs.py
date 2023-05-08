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


class TLWFS(DLLWrapper):
    def __init__(self, dll_path: str):
        super().__init__(dll_path)

        self._bind_functions([
                ("WFS_init", [ViRsrc, ViBoolean, ViBoolean, ViPSession], ViStatus),
                ("WFS_close", [ViSession], ViStatus),
                ("WFS_errorMessage", [ViSession, ViStatus, ctypes.POINTER(ViChar)], ViStatus),
                ("WFS_GetInstrumentInfo", [ViSession, ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar), ctypes.POINTER(ViChar)], ViStatus),
                ("WFS_TakeSpotfieldImage", [ViSession], ViStatus), 
                ("WFS_GetSpotfieldImage", [ViSession, ctypes.POINTER(ctypes.c_uint8), ViPInt32, ViPInt32], ViStatus), 
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
        status = self._dll.WFS_init(ViRsrc(resource_name.encode()),
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
        status = self._dll.WFS_close(ViSession(instrument_handle))
        self.__test_for_error(ViSession(instrument_handle), status)
        return None
    
    def identification_query(self, instrument_handle: int) -> Tuple[str, str, str, str]:
        """
        Returns the device identification information.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :return: A tuple containing the manufacturer name, device name, serial number of the WFS, and serial number of the camera.
        :rtype: Tuple[str, str, str, str]

        :raises NameError: If there is an error during the identification query operation.
        """
        manufacturer_name = ctypes.create_string_buffer(256)
        device_name = ctypes.create_string_buffer(256)
        serial_number = ctypes.create_string_buffer(256)
        serial_number_cam = ctypes.create_string_buffer(256)

        status = self._dll.WFS_GetInstrumentInfo(
            ViSession(instrument_handle),
            manufacturer_name,
            device_name,
            serial_number,
            serial_number_cam
        )

        self.__test_for_error(ViSession(instrument_handle), status)

        return (
            manufacturer_name.value.decode(),
            device_name.value.decode(),
            serial_number.value.decode(),
            serial_number_cam.value.decode()
        )

    def take_spotfield_image(self, instrument_handle: int) -> None:
        """
        Receives a spotfield image from the WFS camera into a driver buffer.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :raises NameError: If there is an error during the take spotfield image operation.
        """
        status = self._dll.WFS_TakeSpotfieldImage(ViSession(instrument_handle))
        self.__test_for_error(ViSession(instrument_handle), status)

    def get_spotfield_image(self, instrument_handle: int) -> Tuple[bytes, int, int]:
        """
        Returns the reference to a spotfield image taken by functions TakeSpotfieldImage() or TakeSpotfieldImageAutoExpos() and the image size.

        :param instrument_handle: The instrument handle returned by <Initialize> to select the desired instrument driver session.
        :type instrument_handle: int

        :return: A tuple containing the reference to the image buffer, the image height (rows) in pixels, and the image width (columns) in pixels.
        :rtype: Tuple[bytes, int, int]

        :raises NameError: If there is an error during the get spotfield image operation.
        """
        image_buf = ctypes.POINTER(ctypes.c_uint8)()
        rows = ViInt32()
        columns = ViInt32()

        status = self._dll.WFS_GetSpotfieldImage(
            ViSession(instrument_handle),
            ctypes.byref(image_buf),
            ctypes.byref(rows),
            ctypes.byref(columns),
        )

        self.__test_for_error(ViSession(instrument_handle), status)

        # Convert the image buffer to bytes.
        buffer_size = rows.value * columns.value
        image_data = bytes(ctypes.cast(image_buf, ctypes.POINTER(ctypes.c_uint8 * buffer_size)).contents)

        return image_data, rows.value, columns.value

    
    def __test_for_error(self, instrument_handle, status):
        if status < 0:
            self.__throw_error(instrument_handle, status)
            

    def __throw_error(self,instrument_handle, status):
        error_message = ctypes.create_string_buffer(256)
        if status < 0:
            self._dll.WFS_error_message(instrument_handle,
                                         status, 
                                         error_message)
            raise NameError(error_message.value.decode())





