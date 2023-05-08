import ctypes
from typing import List, Any, Tuple


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

class TLLK220(DLLWrapper):
    def __init__(self, dll_path:str):
        super().__init__(dll_path)

        self._bind_functions([
            ("List", [ctypes.c_char_p], ctypes.c_int),
            ("Open", [ctypes.c_char_p, ctypes.c_int, ctypes.c_int], ctypes.c_int),
            ("SetEnable", [ctypes.c_int, ctypes.c_int], ctypes.c_int),
            ("SetTargetTemp", [ctypes.c_int, ctypes.c_int], ctypes.c_int),
            ("Close", [ctypes.c_int], ctypes.c_int),
        ])
        
    def list(self) -> List[Tuple[str, str]]:
        """
        List all connected LK220 devices.

        :return: The LK220 device list, each device item is a tuple of (serialNumber, COM)
        :rtype: List[Tuple[str, str]]
        """
        serial_no = ctypes.create_string_buffer(1024)
        result = self._dll.List(ctypes.byref(serial_no))
        self.__test_for_error(result)
        try:
            devices_str = serial_no.value.decode("utf-8", "ignore").rstrip('\x00').split(',')
            devices = [(devices_str[i], devices_str[i + 1]) for i in range(0, len(devices_str), 2) if devices_str[i]]
        except Exception as e:
            return [result]
        return devices
    
    def open(self, serial_no: str, n_baud: int, timeout: int) -> int:
        """
        Open the port for the LK220 device.

        :param serial_no: The serial number of the LK220 device.
        :param n_baud: Bit per second of the port.
        :param timeout: Timeout value in seconds.
        :return: A non-negative handle number if the port is opened successfully; a negative number if it fails.
        :rtype: int
        """
        result = self._dll.Open(ctypes.c_char_p(serial_no.encode()), ctypes.c_int(n_baud), ctypes.c_int(timeout))
        self.__test_for_error(result)
        return result

    def set_enable(self, hdl: int, value: int) -> int:
        """
        Enable or disable the LK220 chiller.

        :param hdl: The handle of the port.
        :param value: 0 to disable the chiller, 1 to enable it.
        :return: 0 if successful; 0xEA for CMD_NOT_DEFINED; 0xEB for timeout.
        :rtype: int
        """
        result = self._dll.SetEnable(ctypes.c_int(hdl), ctypes.c_int(value))
        self.__test_for_error(result)
        return result

    def set_target_temp(self, hdl: int, value: int) -> int:
        """
        Set the target temperature for the LK220 chiller.

        :param hdl: The handle of the port.
        :param value: The target temperature value.
        :return: 0 if successful; 0xEA for CMD_NOT_DEFINED; 0xEB for timeout.
        :rtype: int
        """
        result = self._dll.SetTargetTemp(ctypes.c_int(hdl), ctypes.c_int(value))
        self.__test_for_error(result)
        return result
    
    def close(self, hdl: int) -> int:
        """
        Close the currently opened port.

        :param hdl: The handle of the port.
        :return: 0 if successful; a negative number if it fails.
        :rtype: int
        """
        result = self._dll.Close(ctypes.c_int(hdl))
        self.__test_for_error(result)
        return result


    def __test_for_error(self, result):
        if result < 0:
            raise Exception("Command execution failed. " + str(result))
