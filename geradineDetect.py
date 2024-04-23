import cv2
from djitellopy import Tello

# Initialiser le drone Tello
tello = Tello()
tello.connect()
tello.streamon()


# Fonction pour capturer le flux vidéo depuis la caméra du drone
def capture_video():
    return tello.get_frame_read().frame


# Fonction pour détecter et éviter les obstacles
def detect_and_avoid_obstacles(frame):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Appliquer un flou gaussien pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Appliquer un seuillage pour obtenir un masque binaire
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
    # Trouver les contours des objets en mouvement
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Parcourir les contours détectés
    for contour in contours:
        # Ignorer les petits contours
        if cv2.contourArea(contour) < 500:
            continue
        # Calculer les coordonnées du centre du contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # Si l'obstacle est à gauche, tourner à droite
            if cx < frame.shape[1] // 2:
                return "right"
            # Si l'obstacle est à droite, tourner à gauche
            else:
                return "left"

    # Si aucun obstacle n'est détecté, maintenir la position
    return "hover"


# Boucle principale pour le streaming vidéo continu
while True:
    # Capturer un cadre vidéo
    frame = capture_video()

    # Détecter et éviter les obstacles
    avoidance_command = detect_and_avoid_obstacles(frame)

    # Afficher le cadre vidéo avec la commande d'évitement
    cv2.putText(frame, avoidance_command, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Streaming vidéo avec détection et évitement d\'obstacles', frame)

    # Quitter la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fermer les fenêtres et déconnecter le drone
cv2.destroyAllWindows()
tello.streamoff()
tello.disconnect()