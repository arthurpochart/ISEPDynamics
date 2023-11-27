from ev3dev2.motor import MediumMotor, OUTPUT_C
from time import sleep

claw = MediumMotor(OUTPUT_C)

myspeed = 50

def open_claw():
    claw.on_for_degrees(speed=myspeed,degrees=360*3)

def close_claw():
    claw.on_for_degrees(speed=-myspeed,degrees=360*3)

close_claw()
print("Closing")
sleep(1)
print("Opening")
open_claw()
sleep(10)
