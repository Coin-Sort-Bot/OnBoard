import board
import busio
import adafruit_pca9685
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c, address=0x41)

hat.frequency = 60
led_channel = hat.channels[16]

# Brightness ranges from 0 to 65535
for i in range(65535):
    led_channel.duty_cycle = i
    sleep(.001)
