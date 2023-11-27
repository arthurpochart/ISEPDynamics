from ev3dev2.motor import MediumMotor, OUTPUT_C, OUTPUT_A, OUTPUT_B
from time import sleep
from pynput import keyboard

print("System control: ")
print("Press 1 to start")

drive = MoveTank(OUTPUT_A, OUTPUT_B)
grabber = MediumMotor(OUTPUT_C)

grabberSpeed = 50
driveSpeed=50

def open_claw():
    grabber.on_for_degrees(speed=myspeed,degrees=30)

def close_claw():
    grabber.on_for_degrees(speed=-myspeed,degrees=30)

escape = False
while escape==False:
    direction = input("1.Right 2.Left 3.Open 4.Close")
    
    match direction:
        case '1':
            drive.turn_right(driveSpeed,90)
        case '2'
             drive.turn_left(driveSpeed,90)
        case '3':
             open_claw()
        case '4':
             close_claw()
        case _:
            print("Exiting")
            escape==True


