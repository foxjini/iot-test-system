from . import buzzer, dc_motor, led, neopixel, relay, servo, solenoid

APPLIERS = {
    "led": led.apply,
    "dc_motor": dc_motor.apply,
    "solenoid": solenoid.apply,
    "neopixel": neopixel.apply,
    "buzzer": buzzer.apply,
    "servo": servo.apply,
    "relay": relay.apply,
}
