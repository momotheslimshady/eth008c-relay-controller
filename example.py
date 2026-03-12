from eth008c import ETH008C

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