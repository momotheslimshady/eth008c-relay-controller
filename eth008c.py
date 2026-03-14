

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
    """
    Main controller class for the ETH008C relay module.
    """

    def __init__(self, host, port=17494, password=None):
        self.host = host
        self.port = port
        self.password = password

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.host, self.port))

        if self.password:
            self._send_password(self.password)

    def _send_password(self, password):
        command = bytearray([0x79])
        for char in password:
            command.append(ord(char))

        self._send_command(command)

    def _send_command(self, command):
        if not isinstance(command, bytes):
            command = bytes(command)

        self._sock.sendall(command)
        return self._sock.recv(1024)

    # ------------------------------------------------------------------

    def get_module_info(self):
        """
        Returns:
            tuple: (module_id, hardware_version, firmware_version)
        """
        response = self._send_command([0x10])
        return response[0], response[1], response[2]

    # ------------------------------------------------------------------

    def relay_on(self, relay, duration=0):
        """
        Activate relay.

        relay: 1-8
        duration: 0 = permanent
                  1-255 = pulse (100ms steps)
        """
        command = [0x20, relay, duration]
        return self._send_command(command)

    def relay_off(self, relay, duration=0):
        """
        Deactivate relay.
        """
        command = [0x21, relay, duration]
        return self._send_command(command)

    # ------------------------------------------------------------------

    def set_all_relays(self, states):
        """
        Set all relay outputs.

        states: list of 8 booleans
        """
        if len(states) != 8:
            raise ValueError("Expected list of 8 relay states")

        value = int("".join(str(int(x)) for x in states), 2)

        command = [0x23, value]
        return self._send_command(command)

    # ------------------------------------------------------------------

    def get_relay_states(self):
        """
        Returns the current relay states as a byte.
        """
        return self._send_command([0x24])

    # ------------------------------------------------------------------

    def close(self):
        self._sock.close()