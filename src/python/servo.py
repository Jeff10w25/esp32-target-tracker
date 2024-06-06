import time
from pyfirmata import ArduinoMega, SERVO, util

# Trying OOP!

class Servo:
    
    def __init__(self, name: any, type: str, pin: int, board: any) -> None:
        self.name = name
        self.type = type
        self.pin = pin
        self.board = board
        Servo.setup(self)
    
    def setup(self) -> None:
        try:
            self.servo = self.board.digital[self.pin] # pin on ArduinoMega
            self.servo.mode = SERVO
            print(f"Communication with {self.name} successfully started!")
        except Exception as e:
            print(f"Communication Failed. {e}")
            
    def servoName(self) -> None:
        return '{} type: {}'.format(self.name, self.type)
        
    def validAngle(angle: int) -> int:
        if angle < 0:
            validAngle = 0
        elif angle > 180:
            validAngle = 180
        else:
            validAngle = angle
        return validAngle
        
    def sweepServo(self, delay: int) -> None:
        """ This will start sweeping servo from 0 degrees to 180 degrees angle"""
        for i in range(0, 181, 1):
            self.servo.write(i)
            time.sleep(delay)
        for i in range(180, -1, -1):
            self.servo.write(i)
            time.sleep(delay)
        
    def writeServoAngle(self, angle: int) -> None:
        outAngle = Servo.validAngle(angle)
        self.servo.write(outAngle)

# Test run
if __name__ == '__main__':    
    pin1 = 9
    pin2 = 10   
    port = 'COM5'
    board = ArduinoMega(port)

    servoPan = Servo("servoPan", "MG90S", pin1, board)
    servoTilt = Servo("servoTilt", "MG90S", pin2, board)

    # servoPan.setup()
    print(servoPan.servoName())
    while True:
        servoPan.writeServoAngle(90)
