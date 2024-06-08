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
        
    def validAngle(angle: int) -> int:
        """ Output angle value between 0-180 degrees only """    
        if angle < Servo.MIN_ANGLE:
            validAngle = Servo.MIN_ANGLE
        elif angle > Servo.MAX_ANGLE:
            validAngle = Servo.MAX_ANGLE
        else:
            validAngle = angle
        return validAngle
        
    def sweepServo(self, delay: int) -> None:
        """ Start sweeping servo from 0-180 degrees angle """
        for i in range(0, 181, 1):
            self.servo.write(i)
            time.sleep(delay)
        for i in range(180, -1, -1):
            self.servo.write(i)
            time.sleep(delay)
        
    def writeAngle(self, angle: int) -> None:
        outAngle = Servo.validAngle(angle)
        self.servo.write(outAngle)
        
    def moveAngle(self, angle: int) -> None:
        pass
        

# Test run only
if __name__ == '__main__':    
    # Select the pin and port
    PIN1 = 9
    PIN2 = 10   
    PORT = 'COM5'
    
    # Select the board used to control servo motor
    
    # board = Arduino(port)   
    BOARD = ArduinoMega(PORT)

    servoPan = Servo("servoPan", "MG90S", PIN1, BOARD)
    servoTilt = Servo("servoTilt", "MG90S", PIN2, BOARD)

    print(servoPan.servoName())
    while True:
        servoPan.writeAngle(90)
        servoTilt.writeAngle(90)
        # servoPan.sweepServo(0.05)
        # servoTilt.sweepServo(0.05)
        
        
