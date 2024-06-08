import cv2
from servo import Servo
from faceTracking import Camera, CaffeModel

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
    
if __name__ == '__main__':
    main()