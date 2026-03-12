# ETH008C Relay Controller

Python controller for the **Devantech ETH008C Ethernet Relay Module**.

This project provides a simple Python implementation to communicate with the ETH008C relay board via **TCP/IP** using the binary command protocol defined by Devantech.

This release represents the **first working version (v1.0)** of the controller.

---

# Features

- Connect to an ETH008C relay module via TCP socket
- Read module information (Module ID, Hardware Version, Firmware Version)
- Turn individual relays **ON** or **OFF**
- Set the state of **all relays at once**
- Read the current relay output state

---

# Hardware

This software is designed for the following device:

**Devantech ETH008C**

- 8 Relay Outputs
- Ethernet TCP/IP interface
- Default Port: **17494**

Official documentation:  
https://www.robot-electronics.co.uk/htm/eth008tech.htm

---

# Command Protocol

The ETH008C communicates using a **binary command protocol**.

| Hex  | Dec | Description |
|-----|-----|-------------|
| `0x10` | 16 | Get module information |
| `0x20` | 32 | Activate relay |
| `0x21` | 33 | Deactivate relay |
| `0x23` | 35 | Set all relay outputs |
| `0x24` | 36 | Get relay output states |
| `0x77` | 119 | Get serial number |
| `0x78` | 120 | Get supply voltage |
| `0x79` | 121 | Password entry |
| `0x7A` | 122 | Get unlock time |
| `0x7B` | 123 | Log out |

---

# Relay Timing

The **third byte** of a relay command defines the ON duration.

| Value | Meaning |
|------|--------|
| `0` | Relay remains permanently in the selected state |
| `1 - 255` | Pulsed mode in **100 ms intervals** |

Examples:

| Value | Time |
|------|------|
| `1` | 100 ms |
| `10` | 1 second |
| `255` | 25.5 seconds |

---

# Requirements

- Python **3.x**
- No external dependencies

Only the standard library is used:
- socket


---

# Configuration

Before running the program, adjust the connection parameters in the script.

Example:

```python
eth008c = ETH008C("192.168.0.200", 17494)


| Parameter | Description |
|----------|--------------|
| IP Address | IP address of the ETH008C module |
| Port | Default: **17494** |
| Password | Optional, only required if authentication is enabled |

---

# Usage

Run the script:

```bash
python eth008c.py

The program will:
1.Connect to the relay module
2.Retrieve module information
3.Switch several relays
4.Set all relay states
5.Read the current relay state
6.Close the connection

---

# Example Output

TH008C Relay Controller Example
--------------------------------
Connecting to relay module...

Module ID: 19
Hardware version: 4
Firmware version: 1

Switching relays...

Relay states: b'...'

Connection closed.

---

# Example Code

eth008c = ETH008C("192.168.0.200", 17494)

# Switch relays
eth008c.relais1 = True
eth008c.relais2 = False

# Set all relays at once
eth008c.set_all_relays([
    True,
    False,
    True,
    False,
    True,
    False,
    True,
    False
])

# Read relay states
states = eth008c.get_relay_states()
print(states)

eth008c.close()


---


# Project Status

This repository currently contains the first functional version (v1.0) of the ETH008C relay controller.

Future versions may include improvements such as:
-Refactored project structure
-Separation of controller and example scripts
-Improved API design
-Cleaner relay state handling
-Additional error handling

---

# Disclaimer


This project was created for educational and practical purposes when working with the Devantech ETH008C relay module.

Before controlling real hardware, always verify:
-Correct wiring of the relay board
-Voltage and current ratings of the relays
-Safety of the connected loads
The author is not responsible for any damage caused by improper use.