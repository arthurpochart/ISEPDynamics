from ev3dev2.motor import MediumMotor, OUTPUT_C
from time import sleep

claw = MediumMotor(OUTPUT_C)

myspeed = 50

def open_claw():
    claw.motor.on_for_degrees(speed=myspeed,degrees=30)

def close_claw():
    claw.motor.on_for_degrees(speed=-myspeed,degrees=30)

close_claw()
sleep(1)
open_claw()