#!/usr/bin/python3
from board import SCL, SDA
import busio
from squarebutton import squarebutton
import time
from gpiozero import Button
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)
# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)
# Set the PWM frequency to 60hz.
pca.frequency = 60
print("testing")
lightArray = []
lightArray.append(pca.channels[12])
lightArray.append(pca.channels[13])
lightArray.append( pca.channels[8])
lightArray.append(pca.channels[9])
lightArray.append( pca.channels[4])
lightArray.append( pca.channels[5])
lightArray.append( pca.channels[0])
lightArray.append( pca.channels[1])
lightArray.append( pca.channels[3])
lightArray.append( pca.channels[2])
lightArray.append( pca.channels[7])
lightArray.append( pca.channels[6])
lightArray.append( pca.channels[11])
lightArray.append( pca.channels[10])
lightArray.append( pca.channels[15])
lightArray.append( pca.channels[14])

for i in range (0,19):
    time.sleep(0.1)
    if i < 16:
        lightArray[i].duty_cycle = 0x1fff
    if i > 0 and i < 17:
        lightArray[i-1].duty_cycle = 0xffff
    if i > 1 and i < 18:
        lightArray[i-2].duty_cycle = 0x1fff
    if i > 2:
        lightArray[i-3].duty_cycle = 0x0000

print("loop complete")

print("Configure Lights And Buttons")
lightButtons = {}
lightButtons["rightRun"] = {
    "button": Button(pin=21),
    "lights": squarebutton(pca.channels[0],pca.channels[1],pca.channels[2],pca.channels[3],15),
    "pressed": False
}

lightButtons["rightHigh"] = {
    "button": Button(pin=20),
    "lights": squarebutton(pca.channels[4],pca.channels[5],pca.channels[6],pca.channels[7],15),
    "pressed": False
}

lightButtons["leftRun"] = {
    "button": Button(pin=16),
    "lights": squarebutton(pca.channels[8],pca.channels[9],pca.channels[10],pca.channels[11],15),
    "pressed": False
}

lightButtons["leftHigh"] = {
    "button": Button(pin=12),
    "lights": squarebutton(pca.channels[12],pca.channels[13],pca.channels[14],pca.channels[15],15),
    "pressed": False
}


smallRedButton = Button(pin=25)
keySwitchFirst = Button(pin=23)
keyswitchSecond = Button(pin=24)
bigRedButton = Button(pin=18)
lightButtons["rightRun"]["lights"].go()
lightButtons["rightHigh"]["lights"].setTop()
lightButtons["leftRun"]["lights"].go()
lightButtons["leftHigh"]["lights"].setTop()


print("Run Test")
lightButtons["rightRun"]["lights"].go()
for i in range(0,200):
     time.sleep(0.001)
     lightButtons["rightRun"]["lights"].runLights(i)

print("Stop Test")
lightButtons["rightRun"]["lights"].stop()
for i in range(0,200):
     time.sleep(0.001)
     lightButtons["rightRun"]["lights"].runLights(i)
print("Test Complete")

print("Running")

sleepTime = 0.001
while True:
    for i in range(0,1000):
        time.sleep(sleepTime)
        for button in lightButtons:
            if lightButtons[button]["button"].is_pressed and lightButtons[button]["pressed"] == False:
                lightButtons[button]["pressed"]=True
                lightButtons[button]["lights"].toggle()
            elif lightButtons[button]["button"].is_pressed == False:
                lightButtons[button]["pressed"]=False
            lightButtons[button]["lights"].runLights(i)
