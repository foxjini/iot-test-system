from . import dht11, flame, hcsr04, keypad, pressure, push_button, reed_switch

GENERATORS = {
    "pressure": pressure.generate,
    "keypad": keypad.generate,
    "reed_switch": reed_switch.generate,
    "flame": flame.generate,
    "dht11": dht11.generate,
    "hcsr04": hcsr04.generate,
    "push_button": push_button.generate,
}
