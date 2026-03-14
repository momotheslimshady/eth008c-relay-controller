from eth008c import ETH008C


def main():

    print("ETH008C Relay Controller Example")
    print("--------------------------------")

    controller = ETH008C("192.168.0.200")

    module_id, hw, fw = controller.get_module_info()

    print("Module ID:", module_id)
    print("Hardware version:", hw)
    print("Firmware version:", fw)

    print("\nSwitching relays...")

    controller.relay_on(1)
    controller.relay_off(2)

    controller.set_all_relays([
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False
    ])

    states = controller.get_relay_states()

    print("Relay states:", states)

    controller.close()

    print("\nConnection closed.")


if __name__ == "__main__":
    main()