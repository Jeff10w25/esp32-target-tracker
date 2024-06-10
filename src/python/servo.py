import time
from pyfirmata import Arduino, ArduinoMega, SERVO

# Trying OOP!
class Servo:
    STARTING_ANGLE: int = 90
    MIN_ANGLE: int = 0
    MAX_ANGLE: int = 180
    
    def __init__(self, name: str, type: str, pin: int, board: any) -> None:
        self.name = name
        self.type = type
        self.pin = pin
        self.board = board
        self.setup()
    
    def setup(self) -> None:
        try:
            self.servo = self.board.digital[self.pin]   # pin on Arduino board
            self.servo.mode = SERVO
            print(f"Communication with {self.name} successfully started!")
        except Exception as e:
            print(f"Communication failed. {e}")
            
    def servoName(self) -> str:
        return "{} type: {}".format(self.name, self.type)
        
    def validAngle(self, angle: int) -> int:
        """ Takes in any angle value and returns angle value between 0-180 degrees """    
        if angle < self.MIN_ANGLE:
            return self.MIN_ANGLE
        elif angle > self.MAX_ANGLE:
            return self.MAX_ANGLE
        else:
            return angle
        
    def sweepServo(self, delay: int) -> None:
        """ Start sweeping servo from 0-180-0 degrees angle """
        for i in range(0, self.MAX_ANGLE + 1, 1):
            self.servo.write(i)
            time.sleep(delay)
        for i in range(self.MAX_ANGLE, self.MIN_ANGLE, -1):
            self.servo.write(i)
            time.sleep(delay)
        
    def writeAngle(self, angle: int) -> None:
        outAngle = self.validAngle(angle)
        self.servo.write(outAngle)
        
    def moveAngle(self, currentAngle: int, movAngle: int) -> int:
        """ Move servo by certain angle (negative or positive) from its current position """
        newAngle = currentAngle + movAngle
        self.servo.write(self.validAngle(newAngle))
        return newAngle
        

# Test run only
if __name__ == '__main__':    
    # Select the pin and port
    PIN1 = 9
    PIN2 = 10   
    PORT = 'COM5'
    
    # Select the board used to control servo motor
    # BOARD = Arduino(PORT)   
    BOARD = ArduinoMega(PORT)

    servoPan = Servo("servoPan", "MG90S", PIN1, BOARD)
    servoTilt = Servo("servoTilt", "MG90S", PIN2, BOARD)

    startPan = 90
    startTilt = 90
    
    print(servoPan.servoName())
    while True:
        servoPan.writeAngle(120)
        servoTilt.writeAngle(90)
        # servoPan.sweepServo(0.05)
        # servoTilt.sweepServo(0.05)
        
        # startPan = servoPan.moveAngle(startPan, -2)
        # startTilt = servoTilt.moveAngle(startTilt, +2)
        # time.sleep(0.25)
        
