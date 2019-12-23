class squarebutton:
    def __init__(self, topLeftLight, topRightLight, bottomLeftLight, bottomRightLight, waitCycles=4, leftWaitCycles = 1, rightWaitCycles = 2 ):
        self.lights = [[0,0],[0,0]]
        self.topLeftLight = topLeftLight
        self.topRightLight = topRightLight
        self.bottomLeftLight = bottomLeftLight
        self.bottomRightLight = bottomRightLight
        self.active = False
        self.previousActive = False
        self.casinoRestoreState = False
        self.leftWaitCycles = leftWaitCycles
        self.rightWaitCycles = rightWaitCycles
        self.waitCycles = waitCycles

    def setCasino(self, leftWaitCycles, rightWaitCycles):
        self.leftWaitCycles = leftWaitCycles
        self.rightWaitCycles = rightWaitCycles
        self.casinoRestoreState = self.active
        self.active="casino"
    def setLights(self, lightArray):
        self.lights = lightArray
    def setStatus(self, status = False):
        if status :
           self.setTop()
        else:
           self.setBottom()
    def runLights(self, cycleCount = 0):
        if cycleCount % self.waitCycles == 0 or self.active != self.previousActive:
            if self.active=="go":
                if self.goCycle > 4:
                    self.goCycle = 1
                else:
                    self.goCycle += 1
                self.lights[1][0]=0
                self.lights[1][1]=0
                self.lights[0][1] = self.lights[0][0]
                if self.goCycle == 1:
                    self.lights[0][0] = 0.1
                elif self.goCycle == 2:
                    self.lights[0][0] = 1
                elif self.goCycle == 3:
                    self.lights[0][0] = 0.1
                elif self.goCycle == 4:
                    self.lights[0][0] = 0
            if self.active=="stop":
                if self.lights[1][1]==0.5:
                    self.lights[0][0]=0
                    self.lights[0][1]=0
                    self.lights[1][0]=1
                    self.lights[1][1]=1
                else:
                    self.lights[0][0]=0
                    self.lights[0][1]=0
                    self.lights[1][0]=0.5
                    self.lights[1][1]=0.5
            if self.active=="top":
                self.setTop()
            elif self.active=="bottom":
                self.setBottom()

        if self.active == "casino":
            print("casino not open yet")
            self.active = self.casinoRestoreState
            self.casinoRestoreState = False
        self.topLeftLight.duty_cycle = self.lightValue(self.lights[0][0])
        self.topRightLight.duty_cycle = self.lightValue(self.lights[0][1])
        self.bottomLeftLight.duty_cycle = self.lightValue(self.lights[1][0])
        self.bottomRightLight.duty_cycle = self.lightValue(self.lights[1][1])
        self.previousActive = self.active


    def lightValue(self, brightness):
        import math
        lightValue = math.floor(65535*brightness)
        return lightValue

    def setTop(self):
        self.lights = [[1,1],[0,0]]
        self.active = "top"
        return self.lights
    def setBottom(self):
        self.lights = [[0,0],[1,1]]
        self.active="bottom"
        return self.lights
    def toggle(self):
        if self.active == "top":
            self.active = "bottom"
        elif self.active == "bottom":
            self.active = "top"
        elif self.active == "go":
            self.active = "stop"
        elif self.active == "stop":
            self.active = "go"
        elif self.active == "casino":
            self.active = "casino-stop"
        elif self.active == "casino-stop":
            print("Casino Stopped")
        else:
            self.active = "top"

    def go(self):
        self.active="go"
        if hasattr(self, 'goCycle'):
            print("CycleInProgress")
        else:
           self.goCycle=0
    def stop(self):
        self.active="stop"
