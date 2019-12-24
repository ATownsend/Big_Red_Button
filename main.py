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

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)
# Create PCA9685 class instance.
pca = PCA9685(i2c_bus)
# Set the PWM frequency to 60hz.
pca.frequency = 60






parser = argparse.ArgumentParser(description='Set Parameters for Runing lights')
parser.add_argument('--ButtonToRun', choices=['leftHighButton','leftRunButton','rightHighButton', 'rightRunButton'], default=None,required=False, help='Which Button to Run')
parser.add_argument('--AnimationPattern', type=str, default=None,required=False, help='Animation Pattern to run on button')


args = parser.parse_args()

stopLightAnimationPattern = [ [[  0,  0], [  1,  1]],    [[0.5,  0], [0.5,0.5]],    [[  1,0.5], [  1,  1]],    [[  1,  1], [0.5,0.5]],     [[0.5,  1], [  1,  1]],     [[  0,0.5], [0.5,0.5]] ]
highLightAnimationPattern = [ [[0.5,  1], [0.5,  1]],    [[  1,0.5], [0.5,  1]],    [[0.5,  1], [  1,0.5]],    [[  1,0.5], [  1,0.5]]]

lightButtons = {
    'leftHighButton'  : big_red_button([[pca.channels[12],pca.channels[13]],[pca.channels[14],pca.channels[15]]],Button(pin=12), highLightAnimationPattern),
    'leftRunButton'   : big_red_button([[pca.channels[8],pca.channels[9]],[pca.channels[10],pca.channels[11]]],Button(pin=16), stopLightAnimationPattern),
    'rightHighButton' : big_red_button([[pca.channels[4],pca.channels[5]],[pca.channels[6],pca.channels[7]]],Button(pin=20), highLightAnimationPattern),
    'rightRunButton'  : big_red_button([[pca.channels[0],pca.channels[1]],[pca.channels[2],pca.channels[3]]],Button(pin=21), stopLightAnimationPattern)
}

def runButton(button, animation):
    lightButtons[button].setAnimationPattern(animation)
    lightButtons[button].setOutput()
    lightButtons[button].runLights()


def process_line(line, stdin, process):
    print("TODO, " + line)

def main():
    processKeeper = {}
    for key in lightButtons:
        #lightButtons[key].runLights()
        processKeeper[key] = sh.python("main.py", key ,json.dump(lightButtons[key].getAnimationPattern()), _out=process_line, _bg=True)
    while true:
        print("This Needs to be changed to a wait")
        #TODO: monitor Subprocess

    #for when I make casino mode or connect it to tasks/smartthings
    #processKeeper[key].kill()

    #process = sh.python("test.py", _out=process_line)
    #process.wait()




if __name__ == "__main__":
    if args.ButtonToRun == None:
        main()
    else:
        animationPattern = json.loads(args.AnimationPattern)
        runButton(args.ButtonToRun, animationPattern)








