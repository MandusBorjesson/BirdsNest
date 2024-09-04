from cp210x import (cp210x, cp2104)
import time

class pelican():
    def __init__(self, gpio_control: cp210x):
        self.gpio = gpio_control

    def enable(self, port):
        self.gpio.set(port, True)

    def disable(self, port):
        self.gpio.set(port, False)


if __name__ == "__main__":
    gpio_ctrl = cp2104()
    board = pelican(gpio_ctrl)
    while True:
        for i in range(gpio_ctrl.N_GPIO):
            board.enable(i)
            time.sleep(0.5)
            board.disable(i)
        
