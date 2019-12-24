#!/usr/bin/python3
from board import SCL, SDA
import busio
import time
from gpiozero import Button, LED
from big_red_button import big_red_button
import argparse
from adafruit_pca9685 import PCA9685
import json
import sh
import atexit
import signal


###############################
#                             #
# Attach to PCA9685 Controller#
#                             #
###############################
# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)
# Create PCA9685 class instance.
pca = PCA9685(i2c_bus)
# Set the PWM frequency to 60hz.
pca.frequency = 60
processKeeper = {}
thread = None

###############################
#                             #
# Animations                  #
#                             #
###############################
stopLightAnimationPattern = [ [[  0,  0], [  1,  1]],    [[0.5,  0], [0.5,0.5]],    [[  1,0.5], [  1,  1]],    [[  1,  1], [0.5,0.5]],     [[0.5,  1], [  1,  1]],     [[  0,0.5], [0.5,0.5]] ]
highLightAnimationPattern = [ [[0.5,  1], [0.5,  1]],    [[  1,0.5], [0.5,  1]],    [[0.5,  1], [  1,0.5]],    [[  1,0.5], [  1,0.5]]]

###############################
#                             #
# AssignLights and Buttons    #
#                             #
###############################
smallRedButton = Button(pin=25)
keySwitch = [Button(pin=23),Button(pin=24)]
bigRedButton = Button(pin=18)
ledArray = []
ledArray.append(LED(5))
ledArray.append(LED(6))
ledArray.append(LED(13))
ledArray.append(LED(19))
ledArray.append(LED(26))
lightButtons = {
    'leftHighButton'  : big_red_button([[pca.channels[12],pca.channels[13]],[pca.channels[14],pca.channels[15]]],Button(pin=12), highLightAnimationPattern, 'leftHighButton'),
    'leftRunButton'   : big_red_button([[pca.channels[8],pca.channels[9]],[pca.channels[10],pca.channels[11]]],Button(pin=16), stopLightAnimationPattern, 'leftRunButton'),
    'rightHighButton' : big_red_button([[pca.channels[4],pca.channels[5]],[pca.channels[6],pca.channels[7]]],Button(pin=20), highLightAnimationPattern, 'rightHighButton'),
    'rightRunButton'  : big_red_button([[pca.channels[0],pca.channels[1]],[pca.channels[2],pca.channels[3]]],Button(pin=21), stopLightAnimationPattern, 'rightRunButton')
}



###############################
#                             #
# Command Line Arguments      #
#                             #
###############################
parser = argparse.ArgumentParser(description='Set Parameters for Runing lights')
parser.add_argument('--ButtonToRun', choices=['leftHighButton','leftRunButton','rightHighButton', 'rightRunButton'], default=None,required=False, help='Which Button to Run')
parser.add_argument('--AnimationPattern', type=str, default=None,required=False, help='Animation Pattern to run on button')
args = parser.parse_args()




###############################
#                             #
# Functions                   #
#                             #
###############################
def runButton(button, animation):
    lightButtons[button].setAnimationPattern(animation)
    lightButtons[button].setOutput()
    thread = lightButtons[button].runLights()

def process_line(line, stdin, process):
    values = line.split(",")
    lightButtons[values[0]].setToggle(bool(values[1]))


###############################
#                             #
# Self Test Integration       #
#                             #
###############################
def testLights(lights, lightBank):
    lightArray = list(lights.keys())
    lightsBlank = [0,0]
    lightsFirst = [0.5,0]
    lightsSecond = [1,0.5]
    lightsFull = [1,1]

    #Blank the lights
    for light in lightArray:
        lights[light].setLights([lightsBlank,lightsBlank])

    #Crawl the top
    for light in lightArray:
        lights[light].setLights([lightsFirst,lightsBlank])
        time.sleep(0.2)
        lights[light].setLights([lightsSecond,lightsBlank])
        time.sleep(0.2)
        lights[light].setLights([lightsFull,lightsBlank])

    #Crawl the Bottom
    for light in reversed(lightArray):
        lights[light].setLights([lightsFull, list(reversed(lightsFirst))])
        time.sleep(0.2)
        lights[light].setLights([lightsFull, list(reversed(lightsSecond))])
        time.sleep(0.2)
        lights[light].setLights([lightsFull, list(reversed(lightsFull))])

    for light in lightBank:
        light.on()
        time.sleep(1)
        light.off()


    




###############################
#                             #
# Termination Routines        #
#                             #
###############################
def killSubprocesses():
    for key in processKeeper:
        processKeeper[key].kill()

def killThreads(signal = None, other = None):
    for button in lightbuttons:
        lightbuttons[button].end()
    killSubprocesses()

#Catch attempts to terminate so we can kill our threads and Subprocesses
signal.signal(signal.SIGINT, killThreads)
signal.signal(signal.SIGTERM, killThreads)
atexit.register(killSubprocesses)




###############################
#                             #
# Main                        #
#                             #
###############################
def main():
    testLights(lightButtons, ledArray)
    for key in lightButtons:
        processKeeper[key] = sh.python3("main.py","--ButtonToRun", key ,"--AnimationPattern" ,json.dumps(lightButtons[key].getAnimationPattern()), _out=process_line, _bg=True)
    processKeeper['leftHighButton'].wait()

if __name__ == "__main__":
    if args.ButtonToRun == None:
        main()
    else:
        animationPattern = json.loads(args.AnimationPattern)
        runButton(args.ButtonToRun, animationPattern)
