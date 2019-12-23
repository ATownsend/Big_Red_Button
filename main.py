#!/usr/bin/python3
from board import SCL, SDA
import busio
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

stopLightAnimationPattern = [ [[  0,  0], [  1,  1]],    [[0.5,  0], [0.5,0.5]],    [[  1,0.5], [  1,  1]],    [[  1,  1], [0.5,0.5]],     [[0.5,  1], [  1,  1]],     [[  0,0.5], [0.5,0.5]] ]
highLightAnimationPattern = [ [[0.5,  1], [0.5,  1]],    [[  1,0.5], [0.5,  1]],    [[0.5,  1], [  1,0.5]],    [[  1,0.5], [  1,0.5]]]

lightButtons = {
    'leftHighButton'  : big_red_button([[pca.channels[12],pca.channels[13]],[pca.channels[14],pca.channels[15]]],Button(pin=12), highLightAnimationPattern),
    'leftRunButton'   : big_red_button([[pca.channels[8],pca.channels[9]],[pca.channels[10],pca.channels[11]]],Button(pin=16), stopLightAnimationPattern),
    'rightHighButton' : big_red_button([[pca.channels[4],pca.channels[5]],[pca.channels[6],pca.channels[7]]],Button(pin=20), highLightAnimationPattern),
    'rightRunButton'  : big_red_button([[pca.channels[0],pca.channels[1]],[pca.channels[2],pca.channels[3]]],Button(pin=21), stopLightAnimationPattern)
}


for key in lightButtons:
    lightButtons[key].runLights()



