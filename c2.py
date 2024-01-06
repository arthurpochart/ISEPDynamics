from ev3dev2.motor import MediumMotor, OUTPUT_C, OUTPUT_A, OUTPUT_B
from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor, ColorSensor
from threading import Thread
from ev3dev2.wheel import EV3Tire,Wheel
import os

class OurTire(Wheel):

    def __init__(self):
        Wheel.__init__(self,56.0,28)


print("System control: ")

drive = MoveTank(OUTPUT_A, OUTPUT_B)
grabber = MediumMotor(OUTPUT_C)
colorSensor = ColorSensor()
leds = Leds()
#drive.gyro = GyroSensor()
#drive.gyro.calibrate()
us = UltrasonicSensor()
grabberSpeed = 50
driveSpeed=15
wheelCirc = 5.6*3.14
x = 0
y = 0
tire = OurTire()
wheel = Wheel(56.0,28)
onBorder = False
right = True
chill = False
Delta = 0
nb_Turns = 9

calibrationrot = 83
mdiff = MoveDifferential(OUTPUT_A,OUTPUT_B,wheel,calibrationrot)
mdiff.gyro = GyroSensor()
mdiff.gyro.calibrate()

def driveFor(meters):
    rots = meters/wheelCirc
    drive.on_for_rotations(driveSpeed,driveSpeed,rots,brake=False)
def open_claw():
    grabber.on_for_degrees(speed=grabberSpeed,degrees=360*2.5)

def close_claw():
    grabber.on_for_degrees(speed=-grabberSpeed,degrees=360*2.5)

def checkBorder():
    global onBorder
    global chill
    while True:
        color = colorSensor.color
        if chill == True:
            sleep(13)
        if color == 1:
            onBorder = True

def turn_around_r():
    global y
    global x
    drive.turn_right(driveSpeed,90-4)
    driveFor(10)
    y+=10
    drive.turn_right(driveSpeed,90-4)
    driveFor(5)

def turn_around_l():
    global y
    global x
    drive.turn_left(driveSpeed,90-5)
    driveFor(10)
    y+=10
    drive.turn_left(driveSpeed,90-5)
    driveFor(5)

def turn_around_r_diff():
    global y
    global x
    global Delta
    mdiff.on_to_coordinates(driveSpeed,1000-Delta,0)
    x = 1000-Delta
    mdiff.turn_to_angle(driveSpeed,calibrationrot,use_gyro=True)
    mdiff.on_to_coordinates(driveSpeed,1000-Delta,0)
    y = 1000-Delta
    mdiff.turn_to_angle(driveSpeed,calibrationrot,use_gyro=True)
    mdiff.on_to_coordinates(driveSpeed,1000-Delta,0)
    x = 0 + Delta
    Delta+=80
    mdiff.turn_to_angle(driveSpeed,calibrationrot,use_gyro=True)
    mdiff.on_to_coordinates(driveSpeed,1000-Delta,0)
    y = 0 + Delta
    mdiff.turn_to_angle(driveSpeed,calibrationrot,use_gyro=True)

def expanding_square():
    global onBorder
    global right
    global x
    global y
    while True:
        mdiff.gyro.calibrate()
        mdiff.odometry_start(theta_degrees_start=0)
        print('x:'+str(x)+' y:' +str(y))
        dist = us.distance_centimeters
        print('dist:'+str(dist))
        os.system('clear')
        mdiff.on_to_coordinates(driveSpeed,1000,0)
        if dist < 10:
            mdiff.odometry_stop()
            mdiff.on_to_coordinates(driveSpeed,5,0)
            close_claw()
        
        if onBorder == True:
            mdiff.odometry_stop()
            i = 0 
            for i in range(nb_Turns):
                turn_around_r_diff()
                right = False
        else
            continue
                







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
        if dist < 10:
            drive.off()
            driveFor(5)
            close_claw()
        if onBorder == True:
            drive.off()
            if right == True:
                x=150
                turn_around_r()
                chill = True
                right = False
            else:
                x=0
                chill = True
                right = True
            onBorder = False
        else:
            continue

def rando():
    global onBorder
    global right
    global x
    mdiff.gyro.calibrate()
    mdiff.odometry_start(theta_degrees_start=0)

    mdiff.on_to_coordinates(driveSpeed,1000,0)

    mdiff.turn_to_angle(driveSpeed,0,use_gyro=True)
    mdiff.turn_to_angle(driveSpeed,90,use_gyro=True)
    mdiff.turn_to_angle(driveSpeed,180,use_gyro=True)
    mdiff.turn_to_angle(driveSpeed,270,use_gyro=True)
    mdiff.turn_to_angle(driveSpeed,360,use_gyro=True)

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
            p2=Thread(target=rando)
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
