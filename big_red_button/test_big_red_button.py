#Unit Testing
import pytest
from big_red_button import big_red_button
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from gpiozero import Button, LED

class TestBigRedButton:

    def create_square_light(self, light):
        self.stopLightAnimationPattern = [ [[  0,  0], [  1,  1]],    [[0.5,  0], [0.2,0.2]],    [[  1,0.5], [  1,  1]],    [[  1,  1], [0.2,0.2]],     [[0.5,  1], [  1,  1]],     [[  0,0.5], [0.2,0.2]] ]
        i2c_bus = busio.I2C(SCL, SDA)
        # Create PCA9685 class instance.
        pca = PCA9685(i2c_bus)
        # Set the PWM frequency to 60hz.
        pca.frequency = 60
        if self.lightButtons == None:
            self.lightButtons = {
                'leftHighButton'  : big_red_button([[pca.channels[12],pca.channels[13]],[pca.channels[14],pca.channels[15]]],Button(pin=12), stopLightAnimationPattern, 'leftHighButton'),
                'leftRunButton'   : big_red_button([[pca.channels[8],pca.channels[9]],[pca.channels[10],pca.channels[11]]],Button(pin=16), stopLightAnimationPattern, 'leftRunButton'),
                'rightHighButton' : big_red_button([[pca.channels[4],pca.channels[5]],[pca.channels[6],pca.channels[7]]],Button(pin=20), stopLightAnimationPattern, 'rightHighButton'),
                'rightRunButton'  : big_red_button([[pca.channels[0],pca.channels[1]],[pca.channels[2],pca.channels[3]]],Button(pin=21), stopLightAnimationPattern, 'rightRunButton')
            }
        return self.lightButtons[light]


    #Tests
    def test_create_class(self, light = "leftHighButton"):
        testlight = self.create_square_light(light)
        if testlight != None:
            pass
    def test_set_lights(self, light = "leftHighButton"):
        testlight = self.create_square_light(light)
        assert testlight.setLights == stopLightAnimationPattern[0]

    def test_toggle(self, light = "leftHighButton"):
        testlight = self.create_square_light(light)
        assert testlight.setToggle == True
        assert testlight.setToggleLights == [stopLightAnimationPattern[0][0],[0,0]]
        assert testlight.setToggle == False
        assert testlight.setToggleLights == [[1,1],stopLightAnimationPattern[0][1]]

    def test_light_value(self, light = "leftHighButton"):
        testlight = self.create_square_light(light)
        assert testlight.lightValue(1) == 65535
        assert testlight.lightValue(0) == 0
        assert testlight.lightValue(0.5) == 32767
#    def test_thread_exit(self, light = "leftHighButton"):
#        testlight = self.create_square_light(light)


        
