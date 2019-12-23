#!/usr/bin/python3
from board import SCL, SDA
import busio
from squarebutton import squarebutton
import time
from gpiozero import Button
from big_red_button import big_red_button
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)
# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)
# Set the PWM frequency to 60hz.
pca.frequency = 60





leftRunButton = big_red_button([pca.channels[8],pca.channels[9],pca.channels[10],pca.channels[11]],Button(pin=16))
leftRunButton.setLights([[1,1],[1,1]])