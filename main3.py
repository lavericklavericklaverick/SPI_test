print('Loading modules')
import board
import busio
import digitalio
import laverick3

# create a spi object
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# allocate a CS pin and set the direction
cs = digitalio.DigitalInOut(board.D24)
cs.direction = digitalio.Direction.OUTPUT
print(spi)
# create accel object with the above
accel = laverick3.ADXL34X(spi, cs)

accel.acceleration()

