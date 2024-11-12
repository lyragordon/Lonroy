import serial
import time
import random

class LeakDetector:
    def __init__(self, port="COM6", baudrate=115200, timeout=1, debug=False):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        self.debug = debug

        
    def send_command(self, command) -> str:
        """
        Sends a command to the leak tester and returns the response.
        """
        self.ser.write(f"{command}\r".encode('ascii'))
        
        time.sleep(0.1)
        response = self.ser.read_until(b'\r').decode('ascii').strip()
        if self.debug:
            print(f">{command}")
            print(f"<{response}")
        return response

    def get_leak_rate(self) -> float:
        """
        Reads the leak rate using the 'G1<CR>' command.
        """
        #return random.random()
        try:
            val = float(self.send_command("G1"))
        except:
            pass
        return val
    
    def get_leak_rate_unit(self) -> str:
        """
        Reads the leak rate unit using the 'G5<CR>' command.
        """
        leak_rate_unit = {0:"Pa.m3/s",1:"mbarL/s",2:"atmcc/s"}

        #return "UNIT"
        try:
            val = int(self.send_command("G5"))
        except:
            pass
        return leak_rate_unit[val]

    def get_status(self) -> str:
        """
        Reads the leak detector status using the 'S1<CR>' command.
        """
        #return "OK"
        return self.send_command("S1")

    def start_leak_detection(self) -> str:
        """
        Starts leak detection using the 'START<CR>' command.
        """
        code = self.send_command("START")
        if code == "ER01":
            raise ConnectionError(code)
        else:
            return code

    def stop_leak_detection(self):
        """
        Stops leak detection using the 'STOP<CR>' command.
        """
        code = self.send_command("STOP")
        if code == "ER01":
            raise ConnectionError(code)
        else:
            return code

    def zero_leak_rate(self) -> str:
        """
        Zeros the leak detector using the 'ZERO<CR>' command.
        """
        return self.send_command("ZERO")

    # def read_leak_detector_state(self):
    #     """
    #     Reads the leak detector state using the 'S2<CR>' command.
    #     """
    #     return self.send_command("S2")

    # def read_relay_status(self):
    #     """
    #     Reads the relay status using the 'S3<CR>' command.
    #     """
    #     return self.send_command("S3")

    def get_pressure(self) -> float:
        """
        Reads the current leak detector pressure using the 'G3<CR>' command.
        """
        return float(self.send_command("G3"))



    def get_pressure_unit(self) -> str:
        """
        Reads the vacuum unit using the 'G6<CR>' command.
        """
        pressure_unit = {0:"Pa",1:"mbar",2:"atm"}
        return pressure_unit[int(self.send_command("G6"))]

    # def set_alarm_value(self, alarm_num, base, exponent):
    #     """
    #     Sets alarm value (1-4) with a specific base and exponent using the 'U1/U2/U3/U4<CR>' command.
    #     """
    #     if alarm_num not in [1, 2, 3, 4]:
    #         raise ValueError("Alarm number must be 1, 2, 3, or 4.")
    #     command = f"U{alarm_num}{int(base)}{int(exponent)}"
    #     return self.send_command(command)

    def set_filter_mode(self, mode):
        """
        Sets the filtering mode using 'U50<CR>'.
        0 for dynamic, 1 for static.
        """
        if mode not in [0, 1]:
            raise ValueError("Filter mode must be 0 (dynamic) or 1 (static).")
        return self.send_command(f"U50{mode}")

    def set_calibration(self):
        """
        Starts serial port control calibration with the 'EXTCAL<CR>' command.
        """
        return self.send_command("EXTCAL")

    def test_leak(self):
        """
        Tests leak with the 'TESTC<CR>' command.
        """
        return self.send_command("TESTC")

    def set_standard_leak_value(self, base, exponent):
        """
        Sets the standard leakage value using the 'U81508<CR>' command.
        """
        return self.send_command(f"U8{int(base)}{int(exponent)}")

    def set_leak_detection_mode(self, mode):
        """
        Sets the leak detection mode using the 'U91<CR>' command.
        """
        if mode not in [0, 1, 3]:
            raise ValueError("Leak detection mode must be 0 (automatic), 1 (thick), or 3 (essence).")
        return self.send_command(f"U91{mode}")

    def close(self):
        """
        Closes the serial connection.
        """
        self.ser.close()
