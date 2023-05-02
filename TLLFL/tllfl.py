import serial
import time

class TLLFL:
    """A class to communicate with the Thorlabs Fiber laser."""

    def __init__(self, port):
        """Initialize a new Laser object with the specified port."""
        self.ser = serial.Serial(port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

    def send_command(self, command):
        """Send a command to the laser and return the response."""
        try:
            self.ser.write((command + '\r').encode())
            time.sleep(0.1)
            response = self.ser.read_all().decode()
            return response.strip()
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            return None

    def get_id(self):
        """Return the laser's ID."""
        return self.send_command("id?")

    def get_commands(self):
        """Return a list of available commands for the laser."""
        return self.send_command("?")

    def set_target_temp(self, temp):
        """Set the target temperature of the laser and return the response."""
        return self.send_command(f"target={temp}")

    def get_target_temp(self):
        """Return the target temperature of the laser."""
        return self.send_command("target?")

    def get_actual_temp(self):
        """Return the actual temperature of the laser."""
        return self.send_command("temp?")

    def set_current(self, current):
        """Set the current for the laser in mA and return the response."""
        return self.send_command(f"current={current}")

    def get_current(self):
        """Return the current of the laser."""
        return self.send_command("current?")

    def get_power(self):
        """Return the power of the laser."""
        return self.send_command("power?")

    def get_enable(self):
        """Return the enable status of the laser. 0 is disabled 1 is enabled"""
        return self.send_command("enable?")

    def set_enable(self, enable):
        """Set the enable status of the laser and return the response."""
        return self.send_command(f"enable={enable}")

    def get_specs(self):
        """Return the specifications of the laser."""
        return self.send_command("specs?")

    def set_step(self, step):
        """Set the step value for the laser and return the response."""
        return self.send_command(f"step={step}")

    def get_step(self):
        """Return the step value of the laser."""
        return self.send_command("step?")

    def save_parameters(self):
        """Save the current parameters of the laser and return the response."""
        return self.send_command("save")

    def get_status(self):
        """Return the status word of the laser."""
        return self.send_command("statword?")

    def close(self):
        """Close the serial connection to the laser."""
        self.ser.close()
