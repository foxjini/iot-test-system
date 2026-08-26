from . import (
    dht11,
    flame,
    hcsr04,
    illuminance,
    keypad,
    object_detector,
    pressure,
    push_button,
    qr_scanner,
    reed_switch,
)

GENERATORS = {
    "pressure": pressure.generate,
    "keypad": keypad.generate,
    "reed_switch": reed_switch.generate,
    "flame": flame.generate,
    "dht11": dht11.generate,
    "hcsr04": hcsr04.generate,
    "push_button": push_button.generate,
    "illuminance": illuminance.generate,
    "qr_scanner": qr_scanner.generate,
    "object_detector": object_detector.generate,
}
