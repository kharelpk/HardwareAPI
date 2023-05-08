import serial
import time

class CBEAM:
    """ Class used to communicate with the CBEAM CNC machine from Openbuilds."""
    def __init__(self, address, baudrate=115200, timeout=5):
        """
        Initialize the CBEAM class.

        :param address: Serial communication address
        :param baudrate: Baud rate for serial communication (default: 115200)
        :param timeout: Timeout for serial communication (default: 5 seconds)
        """
        self.address = address
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def connect(self):
        """
        Connect to the CBEAM device using the serial communication address.

        :return: True if the connection was successful, False otherwise.
        """
        try:
            self.serial_connection = serial.Serial(self.address, self.baudrate)
            time.sleep(2)  # Wait for the GRBL to initialize
            self.serial_connection.flushInput()  # Flush startup text
            return True
        except Exception as e:
            print(f"Error connecting to GRBL: {e}")
            return False

    def disconnect(self):
        """Disconnect from the CBEAM device."""
        if self.serial_connection is not None:
            self.serial_connection.close()

    def _send_command(self, command):
        """
        Send a command to the CBEAM device.

        :param command: Command to send
        """
        if self.serial_connection is None:
            print("No connection to GRBL. Please connect first.")
            return

        command = command.strip() + "\n"
        self.serial_connection.write(command.encode())
        response = self.serial_connection.readline().decode().strip()
        print(f"GRBL response: {response}")

    def wait_for_move_complete(self):
        """Wait for the CBEAM device to complete a move."""
        if self.serial_connection is None:
            print("No connection to GRBL. Please connect first.")
            return

        while True:
            self.serial_connection.write(b"?")
            response = self.serial_connection.readline().decode().strip()
            if "Idle" in response:
                break
            time.sleep(0.1)

    def run_gcode(self, filename):
        """
        Execute G-code from a file on the CBEAM device.

        :param filename: Path to the G-code file
        """
        with open(filename, 'r') as gcode_file:
            # Read lines from the G-code file
            for line in gcode_file:
                # Remove comments and whitespace
                stripped_line = line.split(';')[0].strip()
                if not stripped_line:
                    continue

                # Send the G-code command to the CNC machine
                self.serial_connection.write((stripped_line + '\n').encode('ascii'))

                # Wait for the CNC machine to acknowledge the command
                response = self.serial_connection.readline().decode('ascii').strip()
                print(f'Sent: {stripped_line}, Received: {response}')

                # Add a short delay to ensure smooth communication
                time.sleep(0.1)

    def set_unlock(self):
        """Unlock the CBEAM device."""
        self._send_command("$X")

    def set_position_X(self, value:float):
        """
        Set the X position of the CBEAM device.

        :param value: X position value
        """
        self._send_command(f"G0 X{float(value)}")

    def set_position_Y(self, value:float):
        """
        Set the Y position of the CBEAM device.

        :param value: Y position value
        """
        self._send_command(f"G0 Y{float(value)}")

    def set_position_Z(self, value:float):
        """
        Set the Z position of the CBEAM device.

        :param value: Z position value
        """
        self._send_command(f"G0 Z{float(value)}")

    def set_grbl_command(self, command:str):
        """
        Send a custom GRBL command to the CBEAM device.

        :param command: GRBL command string
        """
        self._send_command(command)

    def set_home(self, *args):
        """Set the CBEAM device to the home position."""
        self._send_command("$H")
