import cv2
from djitellopy import tello
import time
import KeyPressModule as kp

kp.init()
me = tello.Tello()
me.connect()

print(me.get_battery())

global img

me.streamon()

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


    if kp.getKey("p"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)
        time.sleep(0.3)
    return[lr, fb, ud, yv]

while True:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1],values[2],values[3])
    time.sleep(0.05)
# image bouclée
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360,240))

    # Appliquer un filtre de correction de couleur pour corriger la couleur bleu
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #Ouverture d'un fenetre d'affichage
    cv2.imshow("Image", img)
    cv2.waitKey(1)