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


class TLLCC25(DLLWrapper):
    def __init__(self, dll_path: str):
        super().__init__(dll_path)

        self._bind_functions([
            ("List", [ctypes.POINTER(ctypes.c_ubyte)], ctypes.c_int),
            ("GetPorts", [ctypes.POINTER(ctypes.c_ubyte)], ctypes.c_int),
            ("Open", [ctypes.c_char_p, ctypes.c_int, ctypes.c_int], ctypes.c_int),
            ("SetOutputMode", [ctypes.c_int, ctypes.c_int], ctypes.c_int),
            ("GetOutputMode", [ctypes.c_int, ctypes.POINTER(ctypes.c_int)], ctypes.c_int),
            ("SetVoltage1", [ctypes.c_int, ctypes.c_double], ctypes.c_int),
            ("SetVoltage2", [ctypes.c_int, ctypes.c_double], ctypes.c_int),
            ("Close", [ctypes.c_int], ctypes.c_int),
        ])

    def list(self) -> List[Tuple[str, str]]:
        """
        List all connected LCC25 devices.

        :return: The LCC25 device list, each device item is a tuple of (serialNumber, COM)
        :rtype: List[Tuple[str, str]]
        """
        serial_no = ctypes.create_string_buffer(1024)
        result = self._dll.List(ctypes.byref(serial_no))
        self._test_for_error(result)
        try:
            devices_str = serial_no.value.decode("utf-8", "ignore").rstrip('\x00').split(',')
            devices = [(devices_str[i], devices_str[i + 1]) for i in range(0, len(devices_str), 2) if devices_str[i]]
        except Exception as e:
            return [result]
        return devices


    
    def get_ports(self) -> str:
        """
        List all the possible ports on this computer.

        :return: A string containing the serial numbers and device descriptors, separated by commas.
                Returns a non-negative number if successful, indicating the number of devices in the list.
                Returns a negative number if unsuccessful.
        :rtype: str
        """
        serial_no = ctypes.create_string_buffer(1024)
        result = self._dll.GetPorts(ctypes.byref(serial_no))
        self._test_for_error(result)

        return serial_no.value.decode()
    
    def open(self, serial_no: str, n_baud: int, timeout: int) -> int:
        """
        Open the port for the specified device.

        :param serial_no: Serial number of the device to be opened.
                        Use the get_ports() function to get the list of available devices first.
        :type serial_no: str
        :param n_baud: Bit per second of the port like 115200.
        :type n_baud: int
        :param timeout: Timeout value in seconds.
        :type timeout: int
        :return: A non-negative number if successful, indicating the handle number returned.
                Returns a negative number if unsuccessful.
        :rtype: int
        """
        result = self._dll.Open(ctypes.c_char_p(serial_no.encode()), 
                                ctypes.c_int(n_baud), 
                                ctypes.c_int(timeout))
        self._test_for_error(result)

        return result

    def set_output_mode(self, hdl: int, mode: int) -> int:
        """
        Set the LCC25's output mode.

        Make sure the port was opened successfully before calling this function.
        Make sure this is the correct device by checking the ID string before calling this function.

        :param hdl: Handle of the port.
        :type hdl: int
        :param mode: LCC25 output mode (0: modulation, 1: voltage1, 2: voltage2).
        :type mode: int
        :return: 0 if successful, 0xEA if the command is not defined, or 0xEB if there's a timeout.
        :rtype: int
        """
        result = self._dll.SetOutputMode(ctypes.c_int(hdl), ctypes.c_int(mode))
        self._test_for_error(result)

        return result
    
    def get_output_mode(self, hdl: int) -> int:
        """
        Return the current output mode.

        Make sure the port was opened successfully before calling this function.
        Make sure this is the correct device by checking the ID string before calling this function.

        :param hdl: Handle of the port.
        :type hdl: int
        :return: A tuple containing the status and output mode. The status is 0 if successful, 0xEA if the command is not defined,
                or 0xEB if there's a timeout. The output mode is the LCC25 output mode (0: modulation, 1: voltage1, 2: voltage2).
        :rtype: Tuple[int, int]
        """
        output_mode = ctypes.c_int()
        result = self._dll.GetOutputMode(ctypes.c_int(hdl), ctypes.byref(output_mode))
        self._test_for_error(result)

        return output_mode.value
    

    def set_voltage1(self, hdl: int, vol: float) -> int:
        """
        Set the LCC25's voltage1 value.

        Make sure the port was opened successfully before calling this function.
        Make sure this is the correct device by checking the ID string before calling this function.

        :param hdl: Handle of the port.
        :type hdl: int
        :param vol: LCC25 voltage1 value, should be between 0 and 25.
        :type vol: float
        :return: 0 if successful, 0xEA if the command is not defined, or 0xEB if there's a timeout.
        :rtype: int
        """
        result = self._dll.SetVoltage1(ctypes.c_int(hdl), ctypes.c_double(vol))
        self._test_for_error(result)

        return result

    def set_voltage2(self, hdl: int, vol: float) -> int:
        """
        Set the LCC25's voltage2 value.

        Make sure the port was opened successfully before calling this function.
        Make sure this is the correct device by checking the ID string before calling this function.

        :param hdl: Handle of the port.
        :type hdl: int
        :param vol: LCC25 voltage2 value, should be between 0 and 25.
        :type vol: float
        :return: 0 if successful, 0xEA if the command is not defined, or 0xEB if there's a timeout.
        :rtype: int
        """
        result = self._dll.SetVoltage2(ctypes.c_int(hdl), ctypes.c_double(vol))
        self._test_for_error(result)

        return result

    def close(self, hdl: int) -> int:
        """
        Close the currently opened port.

        :param hdl: Handle of the port.
        :type hdl: int
        :return: 0 if successful, negative number if unsuccessful.
        :rtype: int
        """
        result = self._dll.Close(ctypes.c_int(hdl))
        self._test_for_error(result)

        return result



    def _test_for_error(self, result):
        if result < 0:
            raise Exception("Command execution failed. " + str(result))
