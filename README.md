# ESP32 Target Tracker

gif gif gif

Face and color tracking ESP32-Camera with 2-axis movement using servo motors

## Hardware Requirements

- ESP32-CAM module
- Arduino Mega2560 or other Arduino modules
- 2 Servo motors
- Pan and Tilt camera platform
- 5 Vdc Power Supply (at least 2.0 A for ESP32-Cam)
- Breadboard (optional)

## Software Requirements

- Arduino IDE 
- PlatformIO on Visual Studio Code

## Installation
- Clone the github repository to your device
- `cd esp32-target-tracker`
- `pip install -r requirements.txt`

### Setting up Arduino Module

1. **Download and install Arduino IDE**
   - Download the latest version of the Arduino IDE from [here](https://www.arduino.cc/en/software).
   - Install the IDE following the instructions for your operating systems

2. **Open the StandardFirmata in Arduino IDE**
   - Go to `File` > `Examples` > `Firmata` and select `StandardFirmata`.

3. **Select the board and port**
   - Go to `Tools` > `Board` > `Arduino AVR Board` and select `Arduino Mega2560`.
   - Go to `Tools` > `Port` and select the port to which the Arduino Mega is connected.

4. **Upload the code**
   - Click the build button to compile and upload the code to the Arduino Mega2560

5. **Open `main.py` and set the GPIO pin used to control servo motors and port connected to the Arduino**

    ```python
    # Select the pin and port
    PIN1 = 9
    PIN2 = 10   
    PORT = 'COM5'
    
    # Select the board used to control servo motor
    
    # board = Arduino(port)   
    BOARD = ArduinoMega(PORT)

    servoPan = Servo("servoPan", "MG90S", PIN1, BOARD)
    servoTilt = Servo("servoTilt", "MG90S", PIN2, BOARD)

### Setting up ESP32-CAM module

1. **Open `http_stream.cpp` and set your WiFi credentials:**

    ```cpp
    const char* ssid = "YOUR_WIFI_ID";  // REPLACE_WITH_YOUR_SSID
    const char* password = "YOUR_WIFI_PASSWORD";  // REPLACE_WITH_YOUR_PASSWORD

2. **Upload the code**
   - Click the build button to compile and upload the code to the ESP32-CAM module

3. **Open the Serial Monitor**
   - Go to `Tools` > `Serial Monitor`.
   - Set the baud rate to `115200`.
   - Note the IP address url printed in the Serial Monitor.

4. **Open `main.py` and set the IP address url retrieve from previous step**
    ```python
     # Setup camera
    URL = "http://192.168.1.1/" # REPLACE_WITH_YOUR_IP
    WINDOW_NAME = "Esp32 live cam"

## Configuration

1. **Set the FOV of the image received from ESP32-CAM** 
    
    Note: the desired values might be lower than the actual FOV values due to the limitations of the servo motors 
    ```python
    image640_480_fov = ImageFOV(640, 480, 15, 13)
   

2. **Open `main.py` and set your color in BGR:**
    
    The tracked color should be relatively bright and saturated
    ```python
    # Select color
    orange = [7, 20, 120]  # orange in BGR colorspace
    colorDetect = ColorDetect(orange)

## Usage

- Run `main.py`.
- Use the keys **Esc**, **D**, **F**, and **C** on the keyboard to switch modes.

## Troubleshooting

- Ensure the wiring is correct.
- Verify the ESP32-CAM is in flash mode when uploading code.
- Check the Serial Monitor for any changes in IP address.
- Ensure the ESP32-CAM and servo motors has a stable power supply.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.