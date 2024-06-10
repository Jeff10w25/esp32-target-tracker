import numpy as np

class ImageFOV:
    def __init__(self, width: int, height: int, fovX: int, fovY: int) -> None:
        self.width = width
        self.height = height
        self.fovX = fovX
        self.fovY = fovY
        self.centerX = self.width/2
        self.centerY = self.height/2
        
    def posToAngle(self, pos: list[int], threshold: int) -> tuple[int]:
        
        if pos == (0, 0):
            return 0, 0
        
        percentDiffX = (pos[0] - self.centerX)/self.width
        percentDiffY = (pos[1] - self.centerY)/self.height
        anglePan = np.round(self.fovX * percentDiffX)
        angleTilt = np.round(self.fovY * percentDiffY)
        
        if abs(anglePan) >= threshold or abs(angleTilt) >= threshold:
            # print(f"{anglePan}, {angleTilt}")
            return anglePan, angleTilt
        else:
            return 0, 0