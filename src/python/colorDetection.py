import cv2
import numpy as np
from PIL import Image

class ColorDetect:
    def __init__(self, color: tuple[int]) -> None:
        self.color = color

    def getLimits(self) -> tuple[int]:
        c = np.uint8([[self.color]])  # BGR values
        hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
        hue = hsvC[0][0][0] 

        # Handle red hue wrap-around
        if hue >= 165:  # Upper limit for divided red hue
            lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
            upperLimit = np.array([180, 255, 255], dtype=np.uint8)
        elif hue <= 15:  # Lower limit for divided red hue
            lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
            upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        else:
            lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
            upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

        return lowerLimit, upperLimit
    
    @staticmethod
    def createMask(frame: any, lowerLims: int, upperLims: int) -> tuple[any]:
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvImage, lowerLims, upperLims)
        maskImg = Image.fromarray(mask)
        
        return mask, maskImg
    
    @staticmethod
    def createColorBbox(frame: any, maskImg: Image) -> tuple:
        bbox = maskImg.getbbox()
        middlePoint = (320, 240)
        
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            middlePoint = (np.round(x1 + x2)/2, np.round(y1 + y2)/2)
            middleText = "Middle point: {}, {}".format(middlePoint[0], middlePoint[1])
                    
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            
            cv2.rectangle(frame, (0, 0), (200, 20), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, middleText, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        
        return frame, middlePoint
        
if __name__ == '__main__':
    
    from camera import Camera
    # Setup camera
    URL = "http://192.168.1.38/"
    WINDOW_NAME = "Webcam w/ mask test"
    
    # esp32 = Camera(URL, WINDOW_NAME)
    
    webcam = Camera(URL, WINDOW_NAME)
    yellow = [7, 20, 120]  # yellow in BGR colorspace
    colorDetect = ColorDetect(yellow)

    while True:
        frame = webcam.readFrame()
        lowerLimit, upperLimit = colorDetect.getLimits()
        print(lowerLimit, upperLimit)
        frameBlur = cv2.GaussianBlur(frame, (13, 13), 0)
        mask, maskImg = colorDetect.createMask(frameBlur, lowerLimit, upperLimit)
        result, midPoint = colorDetect.createColorBbox(frame, maskImg)
        
        maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        webcam.printTwoFrame(result, maskBGR)

        # check for user's input on the keyboard
        key = cv2.waitKey(1) & 0xFF 
        if key == 27: 
            break
        
    webcam.destroy()