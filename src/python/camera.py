import cv2

class Camera:
    def __init__(self, url: str, windowName: str) -> None:
        self.windowName = windowName
        self.url = url
        self.setup()
        
    def setup(self) -> None:
        # Create a Window and VideoCapture object
        cv2.namedWindow(self.windowName, cv2.WINDOW_AUTOSIZE)
        self.cap = cv2.VideoCapture(self.url)

        # Check if the IP camera stream is opened successfully
        if not self.cap.isOpened(): 
            print(f"Failed to open the {self.windowName}'s camera stream")
            exit()
            
    def readFrame(self) -> any:
        """ Returns frame that was read """
        hasFrame, frame = self.cap.read()
        if hasFrame:
            return frame
            
    def printFrame(self, frame: any) -> None:
        try:            
            cv2.imshow(self.windowName, frame)
        except Exception as e:
            print(f"Error showing image. {e}")
            
    def changeBrightness(self, frame: any, value: int) -> any:
        """ Increase brightness with positive value and decrease brightness with negative value """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = cv2.add(hsv[:, :, 2], value)
        frameIncBright = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return frameIncBright       

    def destroy(self) -> None:
        self.cap.release()
        cv2.destroyAllWindows()