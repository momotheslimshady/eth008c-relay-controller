

"""

ETH008C Relay Controller - Version 1.0

First working implementation of a Python controller for the
Devantech ETH008C Ethernet relay module.

========================

This Python program allows control of an ETH008C Ethernet relay module
with 8 relays via TCP/IP.

The program communicates directly with the relay board using the binary
command protocol defined by Devantech.

Main Features
-------------
- Connect to an ETH008C relay module via TCP socket
- Read module information (module ID, hardware version, firmware version)
- Turn individual relays ON or OFF
- Set all relay states simultaneously
- Read the current relay state

ETH008C Binary Command Reference
------------------------------
HEX   DEC  Description
0x10  16   Get module information
0x20  32   Activate relay
0x21  33   Deactivate relay
0x23  35   Set all relay outputs
0x24  36   Get relay outputs
0x77  119  Get serial number
0x78  120  Get supply voltage
0x79  121  Password entry
0x7A  122  Get unlock time
0x7B  123  Log out

Relay Commands Used
-------------------
0x10 (16)  - Get module information
0x20 (32)  - Activate relay
0x21 (33)  - Deactivate relay
0x23 (35)  - Set all relay outputs
0x24 (36)  - Get relay output states
0x79 (121) - Password entry (optional)

Relay Timing
------------
The third byte of a command specifies the ON duration:

0      -> Relay remains permanently in the selected state
1–255  -> Pulsed mode in 100 ms intervals
         (1 = 100 ms, 255 = 25.5 seconds)

Example Usage
-------------
Example connection and relay control:

    eth008c = ETH008C("192.168.0.200", 17494)

    eth008c.relais1 = True
    eth008c.relais2 = False

    states = eth008c.get_relay_states()
    print(states)

    eth008c.close()

Configuration
-------------
Before running the program, adjust the following parameters:

- IP address of the ETH008C module
- TCP port (default: 17494)
- Password (if authentication is enabled)

Requirements
------------
Python 3.x
Standard libraries only:
- socket
"""
import socket


class ETH008C:
    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.relays = [Relay(i + 1) for i in range(8)]

        self._connect()
        if self.password:
            self._send_password()

    def _connect(self):
        # Establishes a connection to the module.
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))

    def _send_password(self, password):
        # Sends the password to the module.
        

        command = bytearray([0x79])
        for char in password:
            command.append(ord(char))
        self._send_command(command)

    def _send_command(self, command, data=None):
        # Sends a command to the module.
        
        # Ensure command is a bytes object
        if not isinstance(command, bytes):
            command = bytes(command)  

        # Prepare data to send (if provided)
        if data is not None:
            if not isinstance(data, bytes):
                data = bytes([data])  
            command += data

        self._sock.sendall(command)
        response = self._sock.recv(1024)
        return response

    def get_module_info(self):
        # Send command 0x10 (16) and return the received 3 bytes (module ID, hardware version, firmware version)
        command = bytearray([0x10])
        response = self._send_command(command)
        return response

    # Define relay properties
    @property
    def relais1(self):
        return self.relays[0]

    @relais1.setter
    def relais1(self, value):
        self._control_relay(1, value)

    @property
    def relais2(self):
        return self.relays[1]

    @relais2.setter
    def relais2(self, value):
        self._control_relay(2, value)

    @property
    def relais3(self):
        return self.relays[2]

    @relais3.setter
    def relais3(self, value):
        self._control_relay(3, value)

    @property
    def relais4(self):
        return self.relays[3]

    @relais4.setter
    def relais4(self, value):
        self._control_relay(4, value)

    @property
    def relais5(self):
        return self.relays[4]

    @relais5.setter
    def relais5(self, value):
        self._control_relay(5, value)

    @property
    def relais6(self):
        return self.relays[5]

    @relais6.setter
    def relais6(self, value):
        self._control_relay(6, value)

    @property
    def relais7(self):
        return self.relays[6]

    @relais7.setter
    def relais7(self, value):
        self._control_relay(7, value)

    @property
    def relais8(self):
        return self.relays[7]

    @relais8.setter
    def relais8(self, value):
        self._control_relay(8, value)


    def set_all_relays(self, states):
        # Check if states list has 8 elements (True/False)
        if not len(states) == 8:
            raise ValueError("Invalid number of states, expected 8")

        # Convert list of booleans to a single byte (all on = 255, all off = 0)
        data = int(''.join(str(int(x)) for x in states), 2)

        # Send command 0x23 (35) with the data byte
        self._send_command(0x23, data)

    def get_relay_states(self):
        # Send command 0x24 (36) and return the received 1 byte (relay states)
        response = self._send_command(0x24)
        return response

    def close(self):
        # Closes the connection to the module.
        self._sock.close()

    def _control_relay(self, relay_number, state):
        if state:
            self.relays[relay_number - 1].turn_on_relay(relay_number)
        else:
            self.relays[relay_number - 1].turn_off_relay(relay_number)

class Relay:
    def __init__(self, relay_number):
        self.relay_number = relay_number

    def turn_on_relay(self, relay_number, duration=0):
        # Turns on the specified relay for the specified duration (in seconds).
        if not (1 <= relay_number <= 8 and 0 <= duration <= 255):
            raise ValueError("Ungültige Relaisnummer oder Dauer")

        # Send command 0x20 (32) with the relay number and duration.
        command = bytearray([0x20, relay_number])  
        command.append(duration)  
        eth008c._send_command(command)  
    def turn_off_relay(self, relay_number, duration=0):
        
        # Turns off the specified relay for the given duration (in seconds).
        
        if not (1 <= relay_number <= 8 and 0 <= duration <= 255):
            raise ValueError("Invalid relay number or duration")

        # Send command 0x21 (33) with relay number and duration
        command = bytearray([0x21, relay_number])  
        command.append(duration)  
        eth008c._send_command(command)  

if __name__ == "__main__":

    print("ETH008C Relay Controller Example")
    print("--------------------------------")
    print("Connecting to relay module...\n")

    eth008c = ETH008C("192.168.0.200", 17494)

    # Retrieve module information
    module_info = eth008c.get_module_info()

    print(f"Module ID: {module_info[0]}")
    print(f"Hardware version: {module_info[1]}")
    print(f"Firmware version: {module_info[2]}")
    print()

    # Example: control individual relays
    print("Switching relays...")

    eth008c.relais1 = False
    eth008c.relais2 = True
    eth008c.relais3 = False
    eth008c.relais4 = True
    eth008c.relais5 = False
    eth008c.relais6 = True
    eth008c.relais7 = False
    eth008c.relais8 = True

    # Example: set all relays at once
    eth008c.set_all_relays([True, False, True, False, True, False, True, False])

    relay_states = eth008c.get_relay_states()
    print(f"Relay states: {relay_states}")

    eth008c.close()

    print("\nConnection closed.")