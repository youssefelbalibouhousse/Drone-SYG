from djitellopy import tello
from time import sleep
import KeyPressModule as kp

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0,0,0,0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("z"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("q"): yv = -speed
    elif kp.getKey("d"): yv = speed

    if kp.getKey("w"): me.land()
    if kp.getKey("x"): me.takeoff()

    return[lr, fb, ud, yv]

while True:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1],values[2],values[3])
    sleep(0.05)