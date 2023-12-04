from ev3dev2.motor import MediumMotor, OUTPUT_C, OUTPUT_A, OUTPUT_B
from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.led import Leds

print("System control: ")
print("Press 1 to start")

drive = MoveTank(OUTPUT_A, OUTPUT_B)
grabber = MediumMotor(OUTPUT_C)
colorSensor = ColorSensor()

grabberSpeed = 50
driveSpeed=50

def open_claw():
    grabber.on_for_degrees(speed=grabberSpeed,degrees=360*3)

def close_claw():
    grabber.on_for_degrees(speed=-grabberSpeed,degrees=360*3)


def snakeTest():
    onBorder = False
    while not onBorder:
        color = colorSensor.color
        print(color)
        sleep(0.5)
        drive.on_for_seconds('0.5')
        if color != 0:
            onBorder = True
            leds.set_color("LEFT", "RED")
            leds.set_color("RIGHT", "RED")


escape = False
while escape==False:
    direction = input("1.Right 2.Left 3.Open 4.Close 5.Test")
    
    if direction=='1':
        drive.turn_right(driveSpeed,90)
    elif direction=='2':
        drive.turn_left(driveSpeed,90)
    elif direction=='3':
        open_claw()
    elif direction=='4':
        close_claw()
    elif direction=='5':
        snakeTest()
    else:
        print("Exiting")
        escape==True



