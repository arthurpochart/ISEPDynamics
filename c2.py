from ev3dev2.motor import MediumMotor, OUTPUT_C, OUTPUT_A, OUTPUT_B
from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, MoveDiffer
ential, SpeedRPM
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor, ColorSensor
from threading import Thread
import os
print("System control: ")
print("Press 1 to start")

drive = MoveTank(OUTPUT_A, OUTPUT_B)
grabber = MediumMotor(OUTPUT_C)
colorSensor = ColorSensor()
leds = Leds()
drive.gyro = GyroSensor()
drive.gyro.calibrate()
us = UltrasonicSensor()
grabberSpeed = 50
driveSpeed=15
wheelCirc = 5.6*3.14
x = 0
y = 0
onBorder = False
right = True
chill = False
def driveFor(meters):
    rots = meters/wheelCirc
    drive.on_for_rotations(driveSpeed,driveSpeed,rots,brake=False)
def open_claw():
    grabber.on_for_degrees(speed=grabberSpeed,degrees=360*3)

def close_claw():
    grabber.on_for_degrees(speed=-grabberSpeed,degrees=360*3)

def checkBorder():
    global onBorder
    global chill
    while True:
        color = colorSensor.color
        if chill == True:
            sleep(12)
        if color == 1:
            onBorder = True

def turn_around_r():
    global y
    global x
    drive.turn_right(driveSpeed,90)
    driveFor(10)
    y+=10
    drive.turn_right(driveSpeed,90)
    driveFor(5)

def turn_around_l():
    global y
    global x
    drive.turn_left(driveSpeed,90)
    driveFor(10)
    y+=10
    drive.turn_left(driveSpeed,90)
    driveFor(5)

def snek():
    global onBorder
    global right
    global x
    while True:
        drive.on(driveSpeed,driveSpeed)
        print('x:'+str(x)+' y:'+str(y))
        dist = us.distance_centimeters
        print('dist:'+str(dist))
        os.system('clear')
        if dist < 5:
            drive.off()
            close_claw()
            turn_around_r()
        if onBorder == True:
            drive.off()
            if right == True:
                x=150
                turn_around_r()
                chill = True
                right = False
            else:
                x=0
                turn_around_l()
                chill = True
                right = True
            onBorder = False
        else:
            continue

def snake():
    global x
    global onBorder
    while not onBorder:
        drive.on(driveSpeed,driveSpeed)
def menu():
    escape = False
    while escape==False:
        direction = input("1.Right 2.Left 3.Open 4.Close 5.Test\n")
        if direction=='1':
            deg = input('Degrees:\n')
            drive.turn_right(driveSpeed,float(deg))
        elif direction=='2':
            deg = input('Degrees\n')
            drive.turn_left(driveSpeed,float(deg))
        elif direction=='3':
            open_claw()
        elif direction=='4':
            close_claw()
        elif direction=='5':
            p1=Thread(target=checkBorder)
            p2=Thread(target=snake)
            p1.start()
            p2.start()
        elif direction == '6':
            try:
                dist = input("\n")
                driveFor(float(dist))
            except KeyboardInterrupt:
                menu()
        else:
            print("Exiting")
            escape==True

if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print('Exiting\n')


