from ev3dev2.motor import MediumMotor, OUTPUT_C, OUTPUT_A, OUTPUT_B
from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, MoveDifferent
ial, SpeedRPM
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor, ColorSensor
from threading import Thread, Event
from ev3dev2.wheel import EV3Tire,Wheel,EV3EducationSetTire
import os


print("System control: ")

#Define multithreading events for communication
stop_event = Event()
detected_event = Event()


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
onBorder = False
right = True
chill = False
detected = False
calibrationrot = 100
mdiff = MoveDifferential(OUTPUT_A,OUTPUT_B,EV3EducationSetTire,calibrationrot)
mdiff.gyro = GyroSensor()
mdiff.gyro.calibrate()

def driveFor(meters):
    rots = meters/wheelCirc
    drive.on_for_rotations(driveSpeed,driveSpeed,rots,brake=False)
def open_claw():
    grabber.on_for_degrees(speed=grabberSpeed,degrees=360*2.7)

def close_claw():
    grabber.on_for_degrees(speed=-grabberSpeed,degrees=360*2.7)

def checkBorder():
    global onBorder
    global chill
    global detected
    while not stop_event.is_set():
        color = colorSensor.color
        dist = us.distance_centimeters
        x = mdiff.x_pos_mm
        y = mdiff.y_pos_mm
        if int(dist) < 4:
            detected = True
            print("DETECTED at position X:"+str(round(x))+" Y:"+str(round(y)))
            detected_event.set()
            stop_event.wait()
        if chill == True:
            sleep(13)
        if color == 1:
            onBorder = True

def killThread(thread):
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')

def log():
    while not stop_event.is_set():
        x = mdiff.x_pos_mm
        y = mdiff.y_pos_mm
        print("X:"+str(round(x))+" Y:"+str(round(y)))
        sleep(1)
def controlThread():
    global detected
    while not stop_event.is_set():
        detected_event.wait()
        print("Killing Thread")
        mdiff.off()
        close_claw()
        stop_event.set()
        mdiff.on_to_coordinates(driveSpeed,0,0)
        print("Going Home")
        sleep(20)
        open_claw()


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

def snake():
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

def square():
    global onBorder
    global right
    global x
    mdiff.gyro.calibrate()
    mdiff.odometry_start(90,0,0,0.005)
    xList = [0, 1500, 1500, 0, 0, 1200, 1200, 300, 300, 900, 900, 600, 600, 750, 750, 600]
    yList = [0, 0, 1500, 1500, 300, 300, 1200, 1200, 600, 600, 900, 900, 600, 600, 750, 750]
    for i in range(len(xList)):
        mdiff.on_to_coordinates(driveSpeed,xList[i],yList[i])
        sleep(1)

def sector():
    global onBorder
    global right
    global x
    mdiff.gyro.calibrate()
    mdiff.odometry_start(90, 0, 0, 0.005)
    xList = [0, 1200, 750, 600, 0, 1500, 1200, 600, 0, 750, 900, 1500, 900, 300]
    yList = [0, 1200, 1500, 0, 600, 750, 0, 1500, 900, 750, 1500, 900, 0, 750]
    for i in range(len(xList)):
        mdiff.on_to_coordinates(driveSpeed,xList[i], yList[i])
        sleep(1)

def menu():
    global detected
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
            p2=Thread(target=square)
            p3=Thread(target=controlThread)
            p4=Thread(target=log)
            p4.start()
            p1.start()
            p2.start()
            p3.start()
            sleep(1)
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
