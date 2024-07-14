import cv2
from servo import Servo
from camera import Camera
from colorDetection import ColorDetect
from faceDetection import CaffeModel
from angle import ImageFOV
from pyfirmata import ArduinoMega

def main():
    # Setup camera
    URL = "http://192.168.1.38/"
    WINDOW_NAME = "Esp32 live cam"
    
    esp32 = Camera(URL, WINDOW_NAME)
    
    # Setup modes
    DEFAULT = 0
    FACE = 1
    COLOR = 2
    
    # Face detection model prototxt and caffe
    MODEL_NAME = "model/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    MODEL_PROTO = "model/deploy.prototxt"

    # Face detection model parameters
    IN_WIDTH = 300
    IN_HEIGHT = 300
    MEAN = [104, 117, 123]
    CONF_THRESHOLD = 0.7
    
    faceDetect = CaffeModel(MODEL_PROTO, MODEL_NAME, IN_WIDTH, IN_HEIGHT, MEAN, CONF_THRESHOLD)

    # Select color
    orange = [7, 20, 120]  # orange in BGR colorspace
    colorDetect = ColorDetect(orange)

    # Select the pin and port
    PIN1 = 9
    PIN2 = 10   
    PORT = 'COM5'
    
    # Select the board used to control servo motor
    
    # board = Arduino(port)   
    BOARD = ArduinoMega(PORT)

    servoPan = Servo("servoPan", "MG90S", PIN1, BOARD)
    servoTilt = Servo("servoTilt", "MG90S", PIN2, BOARD)

    startPan = 90
    startTilt = 60
    
    # image640_480_fov = ImageFOV(640, 480, 45, 40)
    image640_480_fov = ImageFOV(640, 480, 15, 13)
    
    mode = DEFAULT
    
    while True:
        # while key != Esc and check for user's input on the keyboard
        key = cv2.waitKey(1) & 0xFF 
        if key == 27: 
            break
        elif key == ord('d') or key == ord('D'):
            mode = DEFAULT
        elif key == ord('f') or key == ord('F'):
            mode = FACE
        elif key == ord('c') or key == ord('C'):
            mode = COLOR
        
        frame = esp32.readFrame()
        # frame = esp32.changeBrightness(frame, 10)\
        
        if mode == FACE: 
            result_img, mid_point = faceDetect.detectionAndCentroid(frame)
            result_out = esp32.changeBrightness(result_img, 30)
            
            esp32.printFrame(result_out)
            
        elif mode == COLOR:
            lowerLimit, upperLimit = colorDetect.getLimits()
            frameBlur = cv2.GaussianBlur(frame, (11, 11), 0)
            mask, maskImg = colorDetect.createMask(frameBlur, lowerLimit, upperLimit)
            result_img, mid_point = colorDetect.createColorBbox(frame, maskImg)
            result_out = esp32.changeBrightness(result_img, 30)
            
            maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            esp32.printTwoFrame(result_out, maskBGR)
        
        else:
            esp32.printFrame(frame)
            mid_point = (0, 0)
            
        if mid_point != (0, 0):
            anglePan, angleTilt = image640_480_fov.posToAngle(mid_point, 1, 5)
            startPan = servoPan.moveAngle(startPan, anglePan)
            startTilt = servoTilt.moveAngle(startTilt, angleTilt)
        
    esp32.destroy()
    
if __name__ == '__main__':
    main()