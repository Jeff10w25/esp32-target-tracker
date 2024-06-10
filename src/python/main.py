import cv2
from servo import Servo
from camera import Camera
from faceDetection import CaffeModel
from angle import ImageFOV
from pyfirmata import ArduinoMega

def main():
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
    
    mid_point = [320, 240]
    
    # image_fov = ImageFOV(640, 480, 45, 40)
    image640_480_fov = ImageFOV(640, 480, 19, 16)
    
    while True:
        # while key != Esc
        frame = esp32.readFrame()
        # frame = esp32.changeBrightness(frame, 10)
        result_img, mid_point = faceDetect.detectionAndCentroid(frame)
        resultss = esp32.changeBrightness(result_img, 30)
        
        # esp32.printFrame(result_img)
        esp32.printFrame(resultss)
        
        anglePan, angleTilt = image640_480_fov.posToAngle(mid_point, 1)
        
        startPan = servoPan.moveAngle(startPan, anglePan)
        startTilt = servoTilt.moveAngle(startTilt, angleTilt)
        
        # check for user's input on the keyboard
        key = cv2.waitKey(1) & 0xFF 
        if key == 27: 
            break
        
    esp32.destroy()
    
if __name__ == '__main__':
    main()