import math
import threading
import time
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class big_red_button:
    def __init__(self, lightArray, button, lightAnimationPattern = None, name = None, sleepTime = 0.27):
        self.name = name
        self.toggle = False
        self.sleepTime = sleepTime
        self.button = button
        self.running = False
        self.output = False
        #light animation pattern examples (4x4 lit and 4x4 blank)
        #[[1,1],
        # [1,1]],
        #[[0,0],
        # [0,0]],
        self.lightArray = lightArray
        if lightAnimationPattern == None:
            lightAnimationPattern = [ [[  0,  0], [  1,  1]],    [[0.5,  0], [0.5,0.5]],    [[  1,0.5], [  1,  1]],    [[  1,  1], [0.5,0.5]],     [[0.5,  1], [  1,  1]],     [[  0,0.5], [0.5,0.5]] ]
        self.setAnimationPattern(lightAnimationPattern)
        self.lightPattern =[]

    def setAnimationPattern(self, lightAnimationPattern):
        self.lightAnimationPattern = lightAnimationPattern
    def getAnimationPattern(self):
        return self.lightAnimationPattern
    def setToggleLights(self, lightPattern = None):
        if lightPattern == None : lightPattern = self.currentLightPattern
        if self.toggle == True:
            lightPattern = [lightPattern[0], [0,0]]
        elif self.toggle == False:
            lightPattern = [[0,0], lightPattern[1]]
        return lightPattern
    def setLights(self, lightPattern = None):
        if lightPattern == None: lightPattern = self.currentLightPattern
        for vertical in [0,1]:
            for horizontal in [0,1]:
                self.lightArray[vertical][horizontal].duty_cycle = self.lightValue(lightPattern[vertical][horizontal])
    def setToggle(toggle = None):
        if toggle == None: self.toggle = not self.toggle
        else: self.toggle=toggle
    def setOutput(self):
        self.output = True

    @threaded
    def runLights(self, lightAnimationPattern = None, sleepTime=None ):
        if lightAnimationPattern == None: lightAnimationPattern = self.lightAnimationPattern
        if sleepTime == None: sleepTime = self.sleepTime
        self.running = True
        self.pressButton()
        while self.running == True:
            currentState = self.toggle
            for lightArray in lightAnimationPattern:
                if currentState != self.toggle:
                    break
                time.sleep(sleepTime)
                self.setLights(self.setToggleLights(lightArray))
    def lightValue(self, brightness):
        lightValue = math.floor(65535*brightness)
        return lightValue

    @threaded
    def pressButton(self):
        self.running = True
        while self.running == True:
            self.button.wait_for_press()
            self.toggle = not self.toggle
            if self.output : print(self.name + "," + str(self.toggle))
            self.button.wait_for_release()
    def end(self):
        self.running = False