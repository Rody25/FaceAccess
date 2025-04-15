from gpiozero import LED
from time import sleep

# LED-pinner
green_led = LED(17)  # GPIO 17 (pin 11)
red_led = LED(27)    # GPIO 27 (pin 13)

def led_success():
    print("[LED] Grønn på i 2 sekunder")
    green_led.on()
    sleep(2)
    green_led.off()

def led_fail():
    print("[LED] Rød på i 2 sekunder")
    red_led.on()
    sleep(2)
    red_led.off()
