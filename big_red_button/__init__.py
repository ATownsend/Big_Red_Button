def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class big_red_button:
    def __init__(self, lightArray, button, sleepTime = 0.001):
        import math
        self.sleepTime = 0.001
        self.button = button
        #light animation pattern examples (4x4 lit and 4x4 blank)
        #[[1,1],
        # [1,1]],
        #[[0,0],
        # [0,0]],
        self.lightArray = lightArray
        self.lightAnimationPattern = [ [[  0,  0], [  1,  1]],    [[0.5,  0], [0.5,0.5]],    [[  1,0.5], [  1,  1]],    [[  1,  1], [0.5,0.5]],     [[0.5,  1], [  1,  1]],     [[  0,0.5], [0.5,0.5]] ]
        self.lightPattern =[]
    def setAnimationPattern(self, lightAnimationPattern):
        self.lightAnimationPattern = lightAnimationPattern
    def setToggleLights(self, lightPattern = None):
    	if lightPattern == None : lightPattern = self.currentLightPattern
        if self.toggle == True:
            self.setLights([lightPattern[0], [0,0]])
        elif self.toggle == False:
            self.setLights([[0,0], lightPattern[1]])
    def setLights(self, lightPattern = self.currentLightPattern):
        for vertical in [0,1]:
            for horizontal in [0,1]:
                self.lightArray[vertical][horizontal].duty_cycle = self.lightValue(lightPattern[vertical][horizontal])

    @threaded
    def runLights(self, lightAnimationPattern = None, sleepTime=None ):
    	if lightAnimationPattern == None: lightAnimationPattern = self.lightAnimationPattern
    	if sleepTime == None: sleepTime = self.sleepTime
        while True:
            currentState = self.toggle
            for lightArray in lightAnimationPattern:
                if currentState != self.toggle:
                    break
                time.sleep(sleepTime)
                self.setLights(lightArray)
    def lightValue(self, brightness):
        lightValue = math.floor(65535*brightness)
        return lightValue

    @threaded
    def pressButton(self):
        self.button.wait_for_press()
        self.toggle = not self.toggle

    @threaded
    def releaseButton(self):
        self.button.wait_for_release()