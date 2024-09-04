from cp210x import (cp210x, cp2104)
import serial
import time

class SerialBase(serial.Serial):
    def __init__(self, gpio_control: cp210x, *args, **kwargs):
        self.current_port = None
        self.N_PORTS = 8
        self.gpio = gpio_control

        super().__init__(*args, **kwargs)

    def set_port(self, port):
        assert 0 <= port < self.N_PORTS
        if port == self.current_port:
            return
        # GPIOs are in reverse order LSB/MSB
        pins = [0]*self.gpio.N_GPIO
        pins[1] = (port // 4) % 2 == 1
        pins[2] = (port // 2) % 2 == 1
        pins[3] = port % 2 == 1

        self.gpio.write(pins)
        self.current_port = port
        self.flush()



class MuxedSerial():
    def __init__(self, serial: SerialBase, index: int):
        self.serial = serial
        self.index = index
    
    def write(self, *args, **kwargs):
        self.serial.set_port(self.index)
        self.serial.write(*args, **kwargs)

    def read(self, *args, **kwargs):
        self.serial.set_port(self.index)
        self.serial.read(*args, **kwargs)

if __name__ == "__main__":
    gpio_ctrl = cp2104()
    ser = SerialBase(gpio_ctrl, "/dev/ttyUSB0")
    serials = [MuxedSerial(ser, i) for i in range(ser.N_PORTS)]
    while True:
        for port in serials:
            port.write(b"hej")
            time.sleep(0.5)
        
