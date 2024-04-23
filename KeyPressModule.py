import pygame

# Initialiser la bibliothèque pygame
def init():
    # Initialiser le module pygame
    pygame.init()
    # Définir la taille de la fenêtre à 400x400 pixels
    win = pygame.display.set_mode((400, 400))

# Récupérer l'état d'une touche spécifique
def getKey(keyName):
    # Récupérer tous les événements qui se sont produits depuis la dernière fois que cette fonction a été appelée
    for eve in pygame.event.get(): pass
    # Récupérer l'état de toutes les touches
    keyInput = pygame.key.get_pressed()
    # Récupérer le code de la touche spécifiée
    myKey = getattr(pygame,'K_{}'.format(keyName))
    # Vérifier si la touche est pressée
    if keyInput[myKey]:
        # Si la touche est pressée, retourner True
        return True
    # Si la touche n'est pas pressée, retourner False
    return False

# Fonction principale
def main():
    # Récupérer l'état de la touche 'a'
    print(getKey("a"))

# Exécuter la fonction principale
if __name__ == '__main__':
    # Initialiser la fenêtre pygame
    init()
    # Exécuter la fonction principale en boucle infinie
    while True:
        main()