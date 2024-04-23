from djitellopy import tello
import cv2

me=tello.Tello()
me.connect()
print(me.get_battery())

# Définir la qualité de l'image
#me.set_video_bitrate(0)

#Demarrer le stream de la camera
me.streamon()

#boucle de la capture d'image
while True :
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360,240))

    # Appliquer un filtre de correction de couleur pour corriger la couleur bleu
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #Ouverture d'un fenetre d'affichage
    cv2.imshow("Image", img)
    cv2.waitKey(1)