import serial
import time


class EDFA300S:
    """
    Class to control the EDFA 300s from Thorlabs.
    """

    def __init__(self, port):
        """
        Initialize the EDFA class.

        :param str port: Serial port of the device.
        """
        self.ser = serial.Serial(port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

    def send_command(self, command):
        """
        Send a command to the device and return the response.

        :param str command: Command to send.
        :return: Response from the device.
        :rtype: str
        """
        self.ser.write((command + '\r').encode())
        time.sleep(0.1)
        response = self.ser.read_all().decode()
        return response.strip()

    def help(self):
        """
        Get the help information of the device.

        :return: Help information.
        :rtype: str
        """
        return self.send_command("Help")

    def enable_laser(self):
        """
        Enable the laser.

        :return: Response from the device.
        :rtype: str
        """
        return self.send_command("le")

    def disable_laser(self):
        """
        Disable the laser.

        :return: Response from the device.
        :rtype: str
        """
        return self.send_command("ld")

    def set_laser_diode_current(self, current):
        """
        Set the laser diode current.

        :param float current: Laser diode current to set (in mA).
        :return: Response from the device.
        :rtype: str
        """
        return self.send_command(f"sloc {current}")

    def get_laser_diode_current(self):
        """
        Get the current laser diode current.

        :return: Laser diode current.
        :rtype: str
        """
        return self.send_command("gloc")

    def get_status(self):
        """
        Get the status of the device.

        :return: Status information.
        :rtype: str
        """
        return self.send_command("stat")

    def run_pid_power_control(self, power):
        """
        Run the PID power control.

        :param float power: Power setpoint (in dBm).
        :return: Response from the device.
        :rtype: str
        """
        return self.send_command(f"runpwr {power}")

    def run_pid_gain_control(self, gain):
        """
        Run the PID gain control.

        :param float gain: Gain setpoint (in dB).
        :return: Response from the device.
        :rtype: str
        """
        return self.send_command(f"rungain {gain}")

    def close(self):
        """
        Close the serial connection to the device.
        """
        self.ser.close()
