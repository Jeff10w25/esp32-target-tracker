import numpy as np

class ImageFOV:
    def __init__(self, width: int, height: int, fovX: int, fovY: int) -> None:
        self.width = width
        self.height = height
        self.fovX = fovX
        self.fovY = fovY
        self.centerX = self.width/2
        self.centerY = self.height/2
        
    def posToAngle(self, pos: tuple[int], lowerThreshold: int, upperThreshold: int) -> tuple[int]:
        """ Calculate servo motor's angle based on the position of the tracked object """
        if pos == (0, 0):
            return 0, 0
        
        percentDiffX = (pos[0] - self.centerX)/self.width
        percentDiffY = (pos[1] - self.centerY)/self.height
        anglePan = np.round(self.fovX * percentDiffX)
        angleTilt = np.round(self.fovY * percentDiffY)
        
        if abs(anglePan) >= lowerThreshold or abs(angleTilt) >= upperThreshold:
            # print(f"{anglePan}, {angleTilt}")
            anglePan = self.setThreshold(anglePan, upperThreshold)
            angleTilt = self.setThreshold(angleTilt, upperThreshold)
            return anglePan, angleTilt
        else:
            return 0, 0
        
    @staticmethod
    def setThreshold(angleIn: int, upper: int) -> int:    
        """ Set the maximum angle that servo motor can move """
        if abs(angleIn) > upper and angleIn >= 0:
            angleOut = ImageFOV.expo(upper)
        elif abs(angleIn)  > upper and angleIn < 0:
            angleOut = -(ImageFOV.expo(upper))
        else: 
            angleOut = ImageFOV.expo(angleIn)
        return angleOut
    