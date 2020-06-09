from time import sleep
from micropython import const
from adafruit_bus_device.spi_device import SPIDevice

try:
    from struct import unpack
except ImportError:
    from ustruct import unpack
# Conversion factors
_ADXL345_MG2G_MULTIPLIER = 0.004  # 4mg per lsb
_STANDARD_GRAVITY = 9.80665  # earth standard gravity
#Registers
_REG_DATAX0 = const(0x32)  # X-axis data 0
_REG_DATAX1 = const(0x33)  # X-axis data 1
_REG_DATAY0 = const(0x34)  # Y-axis data 0
_REG_DATAY1 = const(0x35)  # Y-axis data 1
_REG_DATAZ0 = const(0x36)  # Z-axis data 0
_REG_DATAZ1 = const(0x37)  # Z-axis data 1  
_REG_POWER_CTL = const(0x2D)  # Power-saving features control
_REG_INT_ENABLE = const(0x2E)  # Interrupt enable control


class ADXL34X:
#Initialise sensor
    def __init__(self, spi, cs):
        self._buffer = bytearray(6)
        self._device = SPIDevice(spi, cs, baudrate=500000, polarity=0, phase=1)
        self._write_register_byte(_REG_POWER_CTL, 0x08)
        self._write_register_byte(_REG_INT_ENABLE, 0x0)
        print('init done')

#Read acceleration
    def acceleration(self):
        print(unpack("<hhh", self._read_register(_REG_DATAX0, 6)))

#Write data to sensor
    def _read_register(self, register, length):
        self._buffer[0] = register & 0xFF
        with self._device as device:
            device.write(self._buffer, start=0, end=1)
            device.readinto(self._buffer, start=0, end=length)
            return self._buffer[0:length]

#Read data from sensor
    def _write_register_byte(self, register, value):
        self._buffer[0] = register & 0xFF
        self._buffer[1] = value & 0xFF
        with self._device as device:
            device.write(self._buffer, start=0, end=2)

    # def _write_u8(self, address, val):
        # # Write an 8-bit unsigned value to the specified 8-bit address.
        # with self._device as device:
            # self._buffer[0] = (address | 0x80) & 0xFF
            # self._buffer[1] = val & 0xFF
            # device.write(self._buffer, end=2)  # pylint: disable=no-member