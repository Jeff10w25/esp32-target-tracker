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
            
    def readFrame(self) -> tuple[bool, any]:
        """ Returns boolean and frame that was read """
        return self.cap.read()
            
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

class CaffeModel:
    def __init__(self, modelProto: str, modelName: str, widthIn: int, heightIn: int, mean: int, confThreshold: int) -> None:
        self.modelName = modelName
        self.modelProto = modelProto
        self.widthIn = widthIn
        self.heightIn = heightIn
        self.mean = mean
        self.confThreshold = confThreshold
        self.setup()

    def setup(self) -> None:
        try:
            self.net = cv2.dnn.readNetFromCaffe(self.modelProto, self.modelName)
        except Exception as e:
            print(f"Error loading model. {e}")
            
    def setBlob(self, frame: any) -> None:
        
        self.blob = cv2.dnn.blobFromImage(frame, 1.0, (self.widthIn, self.heightIn), self.mean, swapRB = False, crop = False)
        self.net.setInput(self.blob)
        self.detections = self.net.forward()
        
    def detectionAndCentroid(self, frame: any) -> tuple:
        """ Detect object(s) and draw rectangle with confidence percentage around them """
        """ And returns the centroid of the rectangle """
        self.setBlob(frame)
        
        middlePoint = (0, 0)
        
        result = frame
        frameHeight = result.shape[0]
        frameWidth = result.shape[1]
        
        for i in range(self.detections.shape[2]): 
            confidence: float = self.detections[0, 0, i, 2]
            if confidence > self.confThreshold:
                x_left_bottom = int(self.detections[0, 0, i, 3] * frameWidth)
                y_left_bottom = int(self.detections[0, 0, i, 4] * frameHeight)
                x_right_top = int(self.detections[0, 0, i, 5] * frameWidth)
                y_right_top = int(self.detections[0, 0, i, 6] * frameHeight)
                    
                middlePoint = [(x_left_bottom + x_right_top)/2, (y_left_bottom + y_right_top)/2]
                middleText = "Middle point: {}, {}".format(int(middlePoint[0]), int(middlePoint[1]))
                    
                # Green outline surrounding faces
                cv2.rectangle(result, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (0, 255, 0))
                label = "Confidence: %.4f" % confidence
                label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                # Confidence text box
                cv2.rectangle(result, (x_left_bottom, y_left_bottom - label_size[1]),
                                    (x_left_bottom + label_size[0], y_left_bottom + base_line),
                                    (255, 255, 255), cv2.FILLED)
                cv2.putText(result, label, (x_left_bottom, y_left_bottom),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                    
                # Middle point position text box
                cv2.rectangle(result, (0, 0), (200, 20), (255, 255, 255), cv2.FILLED)
                cv2.putText(result, middleText, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        return result, middlePoint
        
# class ImageProcessing:
#     def __init__(self) -> None:
#         pass
#     pass

# Test run
if __name__ == '__main__':

    # Setup camera
    URL = "http://192.168.1.40/"
    WINDOW_NAME = "Esp32 live cam"
    
    esp32 = Camera(URL, WINDOW_NAME)
    
    # Face detection model prototxt and caffe
    MODEL_NAME = "model/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    MODEL_PROTO = "model/deploy.prototxt"

    # Face detection model parameters
    IN_WIDTH = 300
    IN_HEIGHT = 300
    MEAN = [104, 117, 123]
    CONF_THRESHOLD = 0.7
    
    faceDetect = CaffeModel(MODEL_PROTO, MODEL_NAME, IN_WIDTH, IN_HEIGHT, MEAN, CONF_THRESHOLD)

    while True:
        # while key != Esc
        has_frame, frame = esp32.readFrame()
        result_img, mid_point = faceDetect.detectionAndCentroid(frame)
        resultss = esp32.changeBrightness(result_img, 20)
        # esp32.printFrame(result_img)
        esp32.printFrame(resultss)
        
        # check for user's input on the keyboard
        key = cv2.waitKey(1) & 0xFF 
        if key == 27: 
            break
        
    esp32.destroy()