import cv2
import numpy as np
from djitellopy import tello
import time

# Créer une instance du drone Tello
me = tello.Tello()
# Se connecter au drone
me.connect()
# Afficher le niveau de batterie du drone
print(me.get_battery())

# Définir la qualité de l'image (facultatif)
#me.set_video_bitrate(0)

# Démarrer le flux vidéo de la caméra du drone
me.streamon()

# Prendre décollage du drone
#me.takeoff()
# Envoyer le drone en haut à une hauteur de 175 cm
me.send_rc_control(0, 0, 0, 50)
time.sleep(1.5)
me.send_rc_control(0, 0, 0, 0)

# Définir la plage de tailles de visage à suivre
fbRange = [6200, 6800]
# Définir les coefficients PID pour la poursuite du visage
pid = [0.4, 0.4, 0]
# Initialiser l'erreur précédente
pError = 0
# Définir la largeur et la hauteur de l'image
w, h = 360, 240

# Définir une fonction pour trouver le visage dans l'image
def findFace(img):
    # Charger le classificateur Haar cascade pour la détection de visage
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # Convertir l'image en niveau de gris
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.uint8)
    # Detecter les visages dans l'image
    faces = faceCascade.detectMultiScale(imgGray, scaleFactor=1.1, minNeighbors=5)

    # Initialiser les listes pour stocker les coordonnées et les superficies des visages
    myFaceListC = []
    myFaceListArea = []

    # Boucler sur les visages détectés
    for (x, y, w, h) in faces:
        # Dessiner un rectangle autour du visage
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # Calculer la position centrale du visage
        cx = x + w // 2
        cy = y + h // 2
        # Calculer la superficie du visage
        area = w * h
        # Dessiner un cercle à la position centrale du visage
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        # Ajouter les coordonnées et la superficie du visage aux listes
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    # Si des visages sont détectés
    if len(myFaceListArea) != 0:
        # Trouver l'index du visage avec la superficie la plus grande
        i = myFaceListArea.index(max(myFaceListArea))
        # Retourner l'image et les coordonnées et la superficie du visage
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        # Si aucun visage n'est détecté, retourner l'image et les coordonnées et la superficie par défaut
        return img, [[0, 0], 0]

# Définir une fonction pour suivre le visage
def trackFace(me, info, w, pid, pError):
    # Récupérer les coordonnées et la superficie du visage
    area = info[1]
    x, y = info[0]
    # Initialiser la vitesse de déplacement
    fb = 0

    # Calculer l'erreur en direction x
    error = x - w // 2
    # Calculer la vitesse en fonction de l'erreur et des coefficients PID
    speed = pid[0] * error + pid[1] * (error - pError)
    # Limiter la vitesse à l'intervalle -100 à 100
    speed = int(np.clip(speed, -100, 100))

    # Si la superficie du visage est dans la plage, définir la vitesse de déplacement à 0
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    # Si la superficie du visage est trop grande, définir la vitesse de déplacement à -20
    elif area > fbRange[1]:
        fb = -20
    # Si la superficie du visage est trop petite, définir la vitesse de déplacement à 20
    elif area < fbRange[0] and area != 0:
        fb = 20

    # Si la coordonnée x est 0, définir la vitesse à 0
    if x == 0:
        speed = 0
        error = 0

    # Envoyer les commandes de contrôle au drone
    me.send_rc_control(0, fb, 0, speed)

    # Retourner l'erreur
    return error

# Définir le classificateur Haar cascade pour la détection de visage
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Boucle principale
while True:
    # Récupérer la frame actuelle de la caméra du drone
    img = me.get_frame()
    # Convertir l'image en niveau de gris
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.uint8)
    # Detecter les visages dans l'image
    faces = faceCascade.detectMultiScale(imgGray, scaleFactor=1.1, minNeighbors=5)
    # Trouver le visage dans l'image
    img, info = findFace(img)
    # Suivre le visage
    pError = trackFace(me, info, w, pid, pError)
    # Afficher la sortie
    cv2.imshow("Sortie", img)
    if cv2.waitKey(1) & 0xff == ord('k'):
        me.land()
        break