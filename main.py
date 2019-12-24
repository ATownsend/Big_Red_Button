#!/usr/bin/python3
from board import SCL, SDA
import busio
import time
from gpiozero import Button
from big_red_button import big_red_button
import argparse
from adafruit_pca9685 import PCA9685
import json
import sh
import atexit
import signal



# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)
# Create PCA9685 class instance.
pca = PCA9685(i2c_bus)
# Set the PWM frequency to 60hz.
pca.frequency = 60
processKeeper = {}
thread = None



parser = argparse.ArgumentParser(description='Set Parameters for Runing lights')
parser.add_argument('--ButtonToRun', choices=['leftHighButton','leftRunButton','rightHighButton', 'rightRunButton'], default=None,required=False, help='Which Button to Run')
parser.add_argument('--AnimationPattern', type=str, default=None,required=False, help='Animation Pattern to run on button')


args = parser.parse_args()

stopLightAnimationPattern = [ [[  0,  0], [  1,  1]],    [[0.5,  0], [0.5,0.5]],    [[  1,0.5], [  1,  1]],    [[  1,  1], [0.5,0.5]],     [[0.5,  1], [  1,  1]],     [[  0,0.5], [0.5,0.5]] ]
highLightAnimationPattern = [ [[0.5,  1], [0.5,  1]],    [[  1,0.5], [0.5,  1]],    [[0.5,  1], [  1,0.5]],    [[  1,0.5], [  1,0.5]]]

lightButtons = {
    'leftHighButton'  : big_red_button([[pca.channels[12],pca.channels[13]],[pca.channels[14],pca.channels[15]]],Button(pin=12), highLightAnimationPattern, 'leftHighButton'),
    'leftRunButton'   : big_red_button([[pca.channels[8],pca.channels[9]],[pca.channels[10],pca.channels[11]]],Button(pin=16), stopLightAnimationPattern, 'leftRunButton'),
    'rightHighButton' : big_red_button([[pca.channels[4],pca.channels[5]],[pca.channels[6],pca.channels[7]]],Button(pin=20), highLightAnimationPattern, 'rightHighButton'),
    'rightRunButton'  : big_red_button([[pca.channels[0],pca.channels[1]],[pca.channels[2],pca.channels[3]]],Button(pin=21), stopLightAnimationPattern, 'rightRunButton')
}

def runButton(button, animation):
    lightButtons[button].setAnimationPattern(animation)
    lightButtons[button].setOutput()
    thread = lightButtons[button].runLights()

def process_line(line, stdin, process):
    values = line.split(",")
    lightButtons[values[0]].setToggle(bool(values[1]))

def testLights(lights):
    lightArray = lights.keys()
    lightsFirst = [[0.5,0][0,0]]
    lightsSecond = [[1,0.5][0,0]]
    lightsThird = [[1,1][0,0]]

    for light in lights:
        lights[light].setLights(lightsFirst)
        time.sleep(0.2)
        lights[light].setLights(lightsSecond)
        time.sleep(0.2)
        lights[light].setLights(lightsThird)

    lightsFirst = [[0,0.5][0,0]]
    lightsSecond = [[0.5,1][0,0]]
    lightsThird = [[1,1][0,0]]
    for light in reversed(lightButtons):
        lights[light].setLights(lightsFirst)
        time.sleep(0.2)
        lights[light].setLights(lightsSecond)
        time.sleep(0.2)
        lights[light].setLights(lightsThird)

    

def main():
    testLights(lightButtons)
for key in lightButtons:
        processKeeper[key] = sh.python3("main.py","--ButtonToRun", key ,"--AnimationPattern" ,json.dumps(lightButtons[key].getAnimationPattern()), _out=process_line, _bg=True)
    processKeeper['leftHighButton'].wait()

def killSubprocesses():
    for key in processKeeper:
        processKeeper[key].kill()

def killThreads():
    for button in lightbuttons:
        lightbuttons[button].end()
    killSubprocesses()

signal.signal(signal.SIGINT, killThreads)
signal.signal(signal.SIGTERM, killThreads)
atexit.register(killSubprocesses)

if __name__ == "__main__":
    if args.ButtonToRun == None:
        main()
    else:
        animationPattern = json.loads(args.AnimationPattern)
        runButton(args.ButtonToRun, animationPattern)
