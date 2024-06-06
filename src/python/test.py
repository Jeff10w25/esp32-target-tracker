import cv2
import servo

def main():
    # Replace the URL with the IP camera's stream URL
    url = "http://192.168.1.33/"

    win_name = "live Cam Testing"
    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)

    # Create a VideoCapture object
    cap = cv2.VideoCapture(url)

    # Check if the IP camera stream is opened successfully
    if not cap.isOpened(): 
        print("Failed to open the IP camera stream")
        exit()
        

    # Face detection model prototxt and caffe
    model_proto = "model/deploy.prototxt"
    model_name = "model/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    net = cv2.dnn.readNetFromCaffe(model_proto, model_name)

    # Face detection model parameters
    in_width = 300
    in_height = 300
    mean = [104, 117, 123]
    conf_threshold = 0.7

    # Image processing modes
    class modes:
        PREVIEW = 0
        BLUR = 1
        CANNY = 2
        FACEDETECT = 3

    alive = True
    image_filter = modes.PREVIEW

    # Read and display video frames
    while alive:
        # Read a frame from the video stream
        has_frame, frame = cap.read()
        
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]

        
        if image_filter == modes.PREVIEW:
            result = frame
        elif image_filter == modes.CANNY:
            result = cv2.Canny(frame, 70, 120)
        elif image_filter == modes.BLUR:
            result = cv2.blur(frame, (13,13))
        elif image_filter == modes.FACEDETECT:
            result = frame
            # Create a 4D blob from a frame.
            blob = cv2.dnn.blobFromImage(result, 1.0, (in_width, in_height), mean, swapRB = False, crop = False)
            # Run a model
            net.setInput(blob)
            detections = net.forward()
            
            for i in range(detections.shape[2]):
                confidence = float(detections[0, 0, i, 2])
                if confidence > conf_threshold:
                    x_left_bottom = int(detections[0, 0, i, 3] * frame_width)
                    y_left_bottom = int(detections[0, 0, i, 4] * frame_height)
                    x_right_top = int(detections[0, 0, i, 5] * frame_width)
                    y_right_top = int(detections[0, 0, i, 6] * frame_height)
                    
                    middle_pt = [(x_left_bottom + x_right_top)/2, (y_left_bottom + y_right_top)/2]
                    middle_txt = "Middle point: %d, %d" % (middle_pt[0], middle_pt[1])
                    
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
                    
                    # Middle position text box
                    cv2.rectangle(result, (0, 0), (200, 20), (255, 255, 255), cv2.FILLED)
                    cv2.putText(result, middle_txt, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        try:            
            cv2.imshow(win_name, result)
        except Exception as err:
            print(err)

        # check for user's input on the keyboard
        key = cv2.waitKey(1) & 0xFF     
        
        if key == 27:   # Esc
            alive = False
        elif key == ord('c') or key == ord('C'):
            image_filter = modes.CANNY       
        elif key == ord('b') or key == ord('B'):
            image_filter = modes.BLUR       
        elif key == ord('p') or key == ord('P'):
            image_filter = modes.PREVIEW      
        elif key == ord('f') or key == ord('F'):
            image_filter = modes.FACEDETECT
    
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':  
    main()