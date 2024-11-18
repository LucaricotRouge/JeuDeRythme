import pygame
import sys
import random 
import datetime
import time 
import openpyxl
from openpyxl import Workbook
import os 
import serial

# Spécifier le port série (vérifie le port COM dans l'IDE Arduino)
# ser = serial.Serial('COM3', 9600, timeout=1)  # Remplace 'COM3' par ton port
# time.sleep(2)  # Attendre que la connexion soit établie

print("Connexion série établie...")

pygame.init()

# Créer la fenêtre
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
date = 0

image_menu = pygame.transform.scale(pygame.image.load('fondMenu.jpg'), (800, 600))  # Redimensionne l'image à 800x600

image_jeu = pygame.transform.scale(pygame.image.load('fondJeu.jpg'), (800, 600))  # Redimensionne l'image à 800x600

# Joueur masculin avec l'animation de base 
JM1 = pygame.transform.scale(pygame.image.load('JM1.png'), (32*4, 32*4))
JM2 = pygame.transform.scale(pygame.image.load('JM2.png'), (32*4, 32*4))
JMAttack = pygame.transform.scale(pygame.image.load('JM1Attack.png'), (32*4, 32*4))

# Joueur féminin avec l'animation de base 
JF1 = pygame.transform.scale(pygame.image.load('JF1.png'), (32*4, 32*4))
JF2 = pygame.transform.scale(pygame.image.load('JF2.png'), (32*4, 32*4))
JFAttack = pygame.transform.scale(pygame.image.load('JF1Attack.png'), (32*4, 32*4))

# Joueur masculin avec l'animation de base 
JM1C = pygame.transform.scale(pygame.image.load('JM1C.png'), (32*4, 32*4))
JM2C = pygame.transform.scale(pygame.image.load('JM2C.png'), (32*4, 32*4))
JMAttackC = pygame.transform.scale(pygame.image.load('JM1CAttack.png'), (32*4, 32*4))

# Joueur féminin avec l'animation de base 
JF1C = pygame.transform.scale(pygame.image.load('JF1C.png'), (32*4, 32*4))
JF2C = pygame.transform.scale(pygame.image.load('JF2C.png'), (32*4, 32*4))
JFAttackC = pygame.transform.scale(pygame.image.load('JF1CAttack.png'), (32*4, 32*4))

# Joueur masculin avec l'animation de base 
JM1CC = pygame.transform.scale(pygame.image.load('JM1CC.png'), (32*4, 32*4))
JM2CC = pygame.transform.scale(pygame.image.load('JM2CC.png'), (32*4, 32*4))
JMAttackCC = pygame.transform.scale(pygame.image.load('JM1CCAttack.png'), (32*4, 32*4))

# Joueur féminin avec l'animation de base 
JF1CC = pygame.transform.scale(pygame.image.load('JF1CC.png'), (32*4, 32*4))
JF2CC = pygame.transform.scale(pygame.image.load('JF2CC.png'), (32*4, 32*4))
JFAttackCC = pygame.transform.scale(pygame.image.load('JF1CCAttack.png'), (32*4, 32*4))

# Cochon qui sert de cible et qui va se déplacer :
Cochon = pygame.transform.scale(pygame.image.load('Cochon.png'), (32*4, 32*4))
cochon_rect = Cochon.get_rect()
# Position initiale du Cochon
cochon_rect.x = 800
cochon_rect.y = 400
# Dimensions de la hitbox (carré de 4x4 pixels)
hitbox_size = 4
speed = 5 # vitesse de déplacement du cochon 
speed20 = False
speed50 = False
speed100 = False

# Initialiser le module de musique
pygame.mixer.init()
# Charger une musique
cochon_channel = pygame.mixer.Channel(1)
spell_channel = pygame.mixer.Channel(2)

# Définir le titre de la fenêtre
pygame.display.set_caption("Magie&Cochon")

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Police pour le texte
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
big_font = pygame.font.SysFont(None, 72)       

# Classe Player
class Player:
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex

    def __str__(self):
        return f"{self.name} ({self.sex})"

# Liste des joueurs (limite à 10)
players = []
# p1 = Player("Lu", "M")
# players.append(p1)
selected_player_index = None

# Spécifier le chemin complet du fichier Excel en utilisant le répertoire courant
current_dir = os.getcwd()  # Obtenir le répertoire courant
EXCEL_FILE = os.path.join(current_dir, "resultatJeu.xlsx")

# Création d'un nouveau classeur Excel
workbook = Workbook()
sheet = workbook.active
sheet.title = "resultatDuJeu"

# Ajouter les en-têtes de colonnes
headers = ["Date", "Joueur", "Sex", "Score", "GoodHit", "PerfectHit", "Précision"]
sheet.append(headers)
print("Fichier Excel créé avec succès !")


# Fonction pour afficher du texte centré
def draw_text(text, font, color, surface, x, y):
    
    label = font.render(text, True, color)
    surface.blit(label, (x - label.get_width() // 2, y - label.get_height() // 2))


# Fonction pour afficher du texte centré pendant 3 sec 
def draw_textDuration(text, font, color, surface, x, y, duration):
    
    """
    Affiche un texte sur l'écran pendant un temps donné.
    
    Paramètres:
    - surface: l'écran sur lequel dessiner <=> écran ici
    - font: la police d'écriture
    - text: le texte à afficher
    - color: couleur du texte (tuple RGB)
    - x, y: position du texte
    - duration: temps que l'on veut pour l'affichage 
    """
    start_time = pygame.time.get_ticks()  # Obtenir le temps actuel
    while pygame.time.get_ticks() - start_time < duration:
        label = font.render(text, True, color)
        surface.blit(label, (x - label.get_width() // 2, y - label.get_height() // 2))
        pygame.display.flip()  # Mettre à jour l'affichage



# Classe des boutons
class Button:
    def __init__(self, text, x, y, width, height, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

        #action sera en général une fonction qui va se lancer lorsque l'on va appuyer sur le bouton
        self.action = action

    def draw(self, surface):
        draw_text(self.text, font, WHITE, surface, self.rect.centerx, self.rect.centery)

    def click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

# Variables pour gérer l'état du menu
current_screen = "menu"
input_text = ""
selected_sex = None
message = ""

# Fonction pour créer un joueur
def create_player_screen():
    global current_screen, input_text, selected_sex, message
    input_text = ""
    selected_sex = None
    current_screen = "create_player"
    message = "Entrez le nom du joueur :"

def confirm_create_player():
    global input_text, selected_sex, message, current_screen
    if len(input_text) == 0 or selected_sex is None:
        message = "Nom ou sexe invalide !"
        return

    if len(players) >= 5:
        message = "La liste des joueurs est pleine."
        return

    new_player = Player(input_text, selected_sex)
    players.append(new_player)
    message = f"Joueur {new_player} créé."
    current_screen = "menu"

def cancel_create_player():
    global current_screen
    current_screen = "menu"

def select_player_screen():
    global current_screen
    current_screen = "select_player"

def quit_game():
    pygame.quit()
    sys.exit()


# fonction qui se lance quand on appuie sur M ou L dans la création de joueur
def set_sex(sex):
    global selected_sex

    selected_sex = sex
    if(sex == "M"): 
        draw_textDuration("Vous avez séléctionné M", font, WHITE, screen, 400, 400, 1000)
    elif(sex == "F"): 
        draw_textDuration("Vous avez séléctionné F", font, WHITE, screen, 400, 400, 1000)
    else: 
        draw_textDuration("...", font, WHITE, screen, 400, 400, 1000)

# fonction pour gérer l'insertion de ce que l'on a tapé au clavier notamment lors de la création d'un personnage et que l'on entre son nom  
def handle_input(event):
    global input_text
    if event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]
    else:
        input_text += event.unicode

def delete_selected_player():
    global selected_player_index
    if selected_player_index is not None:
        players.pop(selected_player_index)
        score[selected_player_index] = 0
        precisionGood[selected_player_index] = 0
        precisionPerfect[selected_player_index] = 0
        nombreDeClick[selected_player_index] = 0
        selected_player_index = None


def go_back_to_menu():
    global current_screen, selected_player_index, game_paused, game_started,active_cochons, current_pattern, pattern_index, pattern_start_time, last_switch_time, is_attacking, attack_start_time 
    selected_player_index = None
    current_screen = "menu"
    game_paused = False
    game_started = False 
    active_cochons = []
    current_pattern = []
    pattern_index = 0 
    pattern_start_time = 0
    last_switch_time = 0  
    is_attacking = False
    attack_start_time = 0   
    pygame.mixer.music.stop()

# Fonction pour dessiner la liste des joueurs
def draw_player_list():
    global selected_player_index
    draw_text("Liste des joueurs :", font, WHITE, screen, 400, 100)
    y_offset = 150
    for i, player in enumerate(players):
        color = GREEN if i == selected_player_index else WHITE
        draw_text(f"{i + 1}. {player}", small_font, color, screen, 400, y_offset)
        y_offset += 60
    if selected_player_index is not None:
        y_offset = 150 + selected_player_index * 60
        start_button = Button("Start", 150, y_offset + 20, 150, 30, BLUE, start_game_with_player)
        delete_button = Button("Supprimer", 500, y_offset + 20, 150, 30, RED, delete_selected_player)
        score_button = Button("Score", 320, y_offset + 20, 150, 30, WHITE, show_score)

        start_button.draw(screen)
        delete_button.draw(screen)
        score_button.draw(screen)

        for button in [start_button, delete_button, score_button]:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if button == start_button:
                    draw_text(button.text, font, (255, 255, 0), screen, button.rect.centerx, button.rect.centery)
                elif button == delete_button:
                     draw_text(button.text, font, (255, 0, 0), screen, button.rect.centerx, button.rect.centery)
                elif button == score_button:
                    draw_text(button.text, font, BLUE, screen, button.rect.centerx, button.rect.centery)
            else:
                draw_text(button.text, font, WHITE, screen, button.rect.centerx, button.rect.centery)

    leaderboard_button = Button("LeaderBoard", 320, 450, 150, 30, WHITE, show_leaderboard)
    leaderboard_button.draw(screen)
    if leaderboard_button.rect.collidepoint(pygame.mouse.get_pos()):
        draw_text(leaderboard_button.text, font, BLUE, screen, leaderboard_button.rect.centerx, leaderboard_button.rect.centery)



    draw_text("Appuyez sur Échap pour revenir", font, WHITE, screen, 400, 500)



def sort_scores_by_player():
    # Associer les scores aux joueurs (score, joueur)
    player_scores = [(score[i], players[i]) for i in range(len(players))]

    # Trier par score, du plus grand au plus petit
    player_scores.sort(reverse=True, key=lambda x: x[0])

    # Extraire les joueurs et les scores trié
    sorted_scores = [score for score, _ in player_scores]
    sorted_players = [player for _, player in player_scores]

    return sorted_players, sorted_scores

def show_leaderboard():
    global current_screen 
    current_screen = "leaderboard"

# Fonction pour afficher le leaderboard
def leaderboard():
    
    screen.fill(WHITE)  
    # Trier les joueurs par score
    sorted_players, sorted_scores = sort_scores_by_player()

    # Affichage du leaderboard
    y_offset = 100
    draw_text("Leaderboard:", font, BLACK, screen, 400, y_offset)
    y_offset += 50

    for i, player in enumerate(sorted_players):
        player_text = f"{player} : {sorted_scores[i]}"
        draw_text(player_text, small_font, GREEN, screen, 400, y_offset)
        y_offset += 40  # Espacement entre les joueurs

    draw_text("Appuyez sur Échap pour revenir", font, BLACK, screen, 400, 500)

    pygame.display.flip()

# Création des boutons pour le menu principal
buttons = [
    Button("Créer un joueur", 250, 150, 300, 50, BLUE, create_player_screen),
    Button("Joueur", 250, 250, 300, 50, BLUE, select_player_screen),
    Button("Quitter", 250, 350, 300, 50, RED, quit_game)
]

# Boutons pour le sexe
sex_buttons = [
    Button("M", 250, 300, 100, 50, BLACK, lambda: set_sex("M")),
    Button("F", 450, 300, 100, 50, BLACK, lambda: set_sex("F"))
]

# Ajouter une variable pour suivre l'état du jeu
game_started = False
game_paused = False

# Fonctions d'action pour les boutons
def resume_game():
    global game_paused
    game_paused = False

continue_button = Button("Continuer", 300, 200, 200, 50, WHITE, resume_game)
quitter_button = Button("Quitter", 300, 300, 200, 50, RED, go_back_to_menu)

def draw_pause_screen():
    """Affiche le menu de pause avec les boutons."""
    screen.fill(BLACK)
    
    # Dessiner les boutons Continuer et Quitter
    continue_button.draw(screen)
    quitter_button.draw(screen)
    pygame.display.flip()

def start_game_with_player():
    
    global selected_player_index, game_started, misscounter, date
    if selected_player_index is not None and not game_started:
        game_started = True  # Indiquer que le jeu a démarré
        print(f"Lancement du jeu avec {players[selected_player_index]} {selected_player_index}")
        global current_screen
        current_screen = "game"  # Changer l'écran en mode jeu

    score[selected_player_index] = 0
    precisionGood[selected_player_index] = 0
    precisionPerfect[selected_player_index] = 0
    nombreDeClick[selected_player_index] = 0
    misscounter = 0

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")




current_imageJM = JM1  # Initialisation de l'image actuelle
hitboxGoodJM = current_imageJM.get_rect(topleft=(50, 400)) # Créer un rectangle (hitbox) pour un score GOOD ! 
                                                            
hitboxPerfectJM = current_imageJM.get_rect(topleft=(130, 400)) # Créer un rectangle (hitbox) pour un score PERFECT !
# je redimensionne ma hitbox 
hitboxGoodJM.width = 80   
hitboxGoodJM.height = 128  

hitboxPerfectJM.width = 40

current_imageJF = JF1  # Initialisation de l'image actuelle
hitboxGoodJF = current_imageJF.get_rect(topleft=(50, 400)) # Créer un rectangle (hitbox) pour un score GOOD ! 
                                                            
hitboxPerfectJF = current_imageJF.get_rect(topleft=(130, 400)) # Créer un rectangle (hitbox) pour un score PERFECT !
# je redimensionne ma hitbox 
hitboxGoodJF.width = 80   
hitboxGoodJF.height = 128  

hitboxPerfectJF.width = 40

last_switch_time = 0  # Dernière fois où les images ont changé


# Variables pour l'attaque 
is_attacking = False
attack_start_time = 0

# Il est important d'initialiser des variables persistantes à l'extérieure de draw_game_screen car elle est appelée constamment dans la boucle 
# while En déplaçant la déclaration de last_switch_time en dehors de la fonction, nous nous assurons qu'une fois qu'une image a changé, 
# le temps écoulé entre les changements d'image est calculé sur la base du temps total de l'application, et non juste depuis le dernier appel de 
# la fonction. Cela permet à last_switch_time de retenir la valeur de la dernière fois où une image a changé.
#  Si la variable last_switch_time est définie à l'intérieur de la fonction draw_game_screen(), chaque fois que la fonction est appelée 
# (par exemple, à chaque boucle de jeu), last_switch_time est réinitialisé à 0, ce qui signifie que la condition 
# if current_time - last_switch_time >= switch_interval: est toujours vraie dès le premier appel.



# Gestion des paternes et défilement des cochons : 
# Patterns définis avec des intervalles

patterns = [
    [0.5, 0.5, 0.5],          
    [0.0, 0.8, 0.5, 0.8],     
    [0.5, 0.5, 0.5, 0.8],     
    [0.8, 0.8],               
    [0.0]                     
]

# Variables pour gérer les cochons en cours
active_cochons = []
current_pattern = []
pattern_index = 0 # index qui parcourt les cochons du patern pour savoir au combien t ième cochon du patern on se situe 
pattern_start_time = 0

def spawn_cochon():
    """Créer un nouveau cochon à droite de l'écran avec sa hitbox"""
    cochon_rect = Cochon.get_rect()
    cochon_rect.x = 800  # Position initiale à droite de l'écran
    cochon_rect.y = 400  # Position verticale fixe

    # Définir la hitbox centrée par rapport au cochon
    hitbox_size = 4
    hitbox_rect = pygame.Rect(
        cochon_rect.centerx - hitbox_size // 2,
        cochon_rect.centery - hitbox_size // 2,
        hitbox_size,
        hitbox_size
    )

    cochon_channel.play(pygame.mixer.Sound("bruitCochon.mp3"))  
    # Retourner un dictionnaire avec le rect du cochon et sa hitbox
    return {"rect": cochon_rect, "hitbox": hitbox_rect, "processed": False}

def draw_cochons():
    """Afficher et déplacer les cochons à l'écran avec leurs hitboxes"""
    for cochon in active_cochons:
        # Déplacer le cochon vers la gauche
        cochon["rect"].x -= speed

        # Mettre à jour la position de la hitbox pour qu'elle suive le cochon
        cochon["hitbox"].x = cochon["rect"].centerx - cochon["hitbox"].width // 2
        cochon["hitbox"].y = cochon["rect"].centery - cochon["hitbox"].height // 2

        # Afficher le cochon à l'écran
        screen.blit(Cochon, cochon["rect"])

        # Dessiner la hitbox (pour le débogage)
        # pygame.draw.rect(screen, (255, 0, 0), cochon["hitbox"], 1)

def update_cochons():
    """Mettre à jour la liste des cochons, en supprimant ceux qui sont sortis de l'écran"""
    global active_cochons
    active_cochons = [c for c in active_cochons if c["rect"].right > 0]

def start_new_pattern():
    """Démarrer un nouveau pattern"""
    global current_pattern, pattern_index, pattern_start_time
    current_pattern = random.choice(patterns)
    pattern_index = 0
    pattern_start_time = pygame.time.get_ticks()

def handle_pattern():
    global pattern_index, pattern_start_time

    # Si tous les cochons du pattern ont été générés
    if pattern_index >= len(current_pattern):
        if not active_cochons:
            start_new_pattern()
        return

    current_time = pygame.time.get_ticks()

    # Vérifier si le délai pour le prochain cochon est écoulé
    if (current_time - pattern_start_time) / 1000 >= current_pattern[pattern_index]:
        new_cochon = spawn_cochon()
        active_cochons.append(new_cochon)
        print(f"Spawned cochon at pattern index {pattern_index}")  # Debug
        pattern_index += 1
        pattern_start_time = current_time



# Données statistiques que l'on va utiliser 

score = [0]*5; 
precisionPerfect = [0]*5; 
precisionGood = [0]*5; 
nombreDeClick = [0]*5; 


def show_score():
    global current_screen
    current_screen = "score_screen"

def draw_score_screen():
    screen.fill(BLACK)  # Fond noir

    # Utiliser l'index du joueur sélectionné pour récupérer les scores et précisions
    if selected_player_index is not None:
        # Récupérer les informations du joueur courant
        player_score = score[selected_player_index]
        player_precision_good = precisionGood[selected_player_index]
        player_precision_perfect = precisionPerfect[selected_player_index]
        player_clicks = nombreDeClick[selected_player_index]

        # Calculer la précision totale (si nombre de clics n'est pas nul)
        total_precision = 0
        if player_clicks > 0:
            total_precision = (player_precision_good + player_precision_perfect) / player_clicks * 100

        # Afficher les informations sur l'écran
        draw_text(f"Score: {player_score}", font, WHITE, screen, 400, 100)
        draw_text(f"Good Hits: {player_precision_good}", font, WHITE, screen, 400, 200)
        draw_text(f"Perfect Hits: {player_precision_perfect}", font, WHITE, screen, 400, 300)
        draw_text(f"Nombre de Clicks: {player_clicks}", font, WHITE, screen, 400, 400)
        draw_text(f"Précision Totale: {total_precision:.2f}%", font, WHITE, screen, 400, 500)

    # Bouton pour revenir au menu de création de joueur
    retour_button = Button("Retour", 0, 400, 150, 50, RED, action=go_back_to_select_player)
    retour_button.draw(screen)

def go_back_to_select_player():
    global current_screen
    current_screen = "select_player"

# Variables affichages "miss", "good", "perfect"
hit_result_text = ""
hit_result_color = (255, 255, 255)  # Couleur par défaut
result_display_time = 1000  # Durée d'affichage du message en millisecondes
last_result_time = 0
misscounter = 0 # compter le nombre de miss pour afficher un game over

def check_full_hitM(cochon):

    global score, precisionPerfect, precisionGood, nombreDeClick, misscounter, is_attacking
    """Vérifie si la hitbox du cochon est complètement à l'intérieur des hitboxes du personnage"""
    # Récupérer la hitbox du cochon
    cochon_hitbox = cochon["hitbox"]

    # Vérifier que tous les coins du cochon sont dans la hitboxPerfect ou hitboxGood
    if hitboxPerfectJM.collidepoint(cochon_hitbox.topleft) and \
       hitboxPerfectJM.collidepoint(cochon_hitbox.topright) and \
       hitboxPerfectJM.collidepoint(cochon_hitbox.bottomleft) and \
       hitboxPerfectJM.collidepoint(cochon_hitbox.bottomright):
        score[selected_player_index] += 2
        precisionPerfect[selected_player_index] +=1
        nombreDeClick[selected_player_index] += 1
        is_attacking = False
        return "Perfect", GREEN
    
    elif hitboxGoodJM.collidepoint(cochon_hitbox.topleft) and \
         hitboxGoodJM.collidepoint(cochon_hitbox.topright) and \
         hitboxGoodJM.collidepoint(cochon_hitbox.bottomleft) and \
         hitboxGoodJM.collidepoint(cochon_hitbox.bottomright):
        score[selected_player_index] += 1
        precisionGood[selected_player_index] +=1
        nombreDeClick[selected_player_index] += 1
        is_attacking = False 
        return "Good", BLUE
    
    is_attacking = False
    misscounter += 1
    nombreDeClick[selected_player_index] +=1
    return "Miss", RED    

def check_full_hitF(cochon):

    global score, precisionPerfect, precisionGood, nombreDeClick, misscounter, is_attacking #, ser
    """Vérifie si la hitbox du cochon est complètement à l'intérieur des hitboxes du personnage"""
    # Récupérer la hitbox du cochon
    cochon_hitbox = cochon["hitbox"]

    # Vérifier que tous les coins du cochon sont dans la hitboxPerfect ou hitboxGood
    if hitboxPerfectJF.collidepoint(cochon_hitbox.topleft) and \
       hitboxPerfectJF.collidepoint(cochon_hitbox.topright) and \
       hitboxPerfectJF.collidepoint(cochon_hitbox.bottomleft) and \
       hitboxPerfectJF.collidepoint(cochon_hitbox.bottomright):
        score[selected_player_index] += 2
        precisionPerfect[selected_player_index] +=1
        nombreDeClick[selected_player_index] += 1
        is_attacking = False
        # if ser.is_open:
        #     ser.write(("Perfect" + '\n').encode())  # Envoyer le résultat à l'Arduino
        #     time.sleep(1)

        return "Perfect", GREEN
    
    elif hitboxGoodJF.collidepoint(cochon_hitbox.topleft) and \
         hitboxGoodJF.collidepoint(cochon_hitbox.topright) and \
         hitboxGoodJF.collidepoint(cochon_hitbox.bottomleft) and \
         hitboxGoodJF.collidepoint(cochon_hitbox.bottomright):
        score[selected_player_index] += 1
        precisionGood[selected_player_index] +=1
        nombreDeClick[selected_player_index] += 1
        is_attacking = False 
        # if ser.is_open:
        #     ser.write(("Good" + '\n').encode())  # Envoyer le résultat à l'Arduino
        #     time.sleep(1)
            
        return "Good", BLUE
    
    is_attacking = False
    misscounter += 1
    nombreDeClick[selected_player_index] +=1
    # if ser.is_open:
    #     ser.write(("Miss" + '\n').encode())  # Envoyer le résultat à l'Arduino
    #     time.sleep(1)
            
    return "Miss", RED 

result_displayed = False

def draw_game_screen():

    global current_imageJM, current_imageJF, last_switch_time, attack_start_time, is_attacking, hit_result_text, active_cochons, hit_result_color, last_result_time, result_displayed, current_screen, misscounter, speed, speed20, speed50, speed100

    # Variable pour gérer le temps dans les animations de bases 

    switch_interval = 200  # Intervalle (en millisecondes) à laquelle l'animation de base va changer 

    screen.blit(image_jeu, (0, 0))  # Afficher l'image à partir du coin supérieur gauche
    current_time = pygame.time.get_ticks() # temps actuel 


    # pygame.draw.rect(screen, RED, hitboxGoodJM, 2)
    # pygame.draw.rect(screen, BLUE, hitboxPerfectJM, 2)

    # Animation des joeurs 
    if(players[selected_player_index].sex == "M"):
        
        # Vérifier si l'intervalle de 0.5 seconde est passé
        if current_time - last_switch_time >= switch_interval and misscounter == 0:
            # Alterner entre JM1 et JM2
            if current_imageJM == JM1: # si on détecte JM1 dans la zone où a été chargé l'image JM1
                current_imageJM = JM2
            else:
                current_imageJM = JM1
            
            # Mettre à jour le temps de changement d'image
            last_switch_time = current_time
        
        if is_attacking and misscounter == 0:
            if current_time - attack_start_time < switch_interval:
                # Afficher l'image d'attaque pendant 0.5 seconde
                current_imageJM = JMAttack
            else:
                # Fin de l'animation d'attaque, retour à l'animation normale
                is_attacking = False
                attack_start_time = 0

        # Vérifier si l'intervalle de 0.5 seconde est passé
        if current_time - last_switch_time >= switch_interval and misscounter ==1:
            # Alterner entre JM1 et JM2
            if current_imageJM == JM1C: # si on détecte JM1 dans la zone où a été chargé l'image JM1
                current_imageJM = JM2C
            else:
                current_imageJM = JM1C
            
            # Mettre à jour le temps de changement d'image
            last_switch_time = current_time

        if is_attacking and misscounter == 1:
            if current_time - attack_start_time < switch_interval:
                # Afficher l'image d'attaque pendant 0.5 seconde
                current_imageJM = JMAttackC
            else:
                # Fin de l'animation d'attaque, retour à l'animation normale
                is_attacking = False
                attack_start_time = 0
        
                # Vérifier si l'intervalle de 0.5 seconde est passé et que misscounter >= 5 
        if current_time - last_switch_time >= switch_interval and misscounter == 2:
            # Alterner entre JM1 et JM2
            if current_imageJM == JM1CC: # si on détecte JM1 dans la zone où a été chargé l'image JM1
                current_imageJM = JM2CC
            else:
                current_imageJM = JM1CC
            
            # Mettre à jour le temps de changement d'image
            last_switch_time = current_time
        
        if is_attacking and misscounter == 2:
            if current_time - attack_start_time < switch_interval:
                # Afficher l'image d'attaque pendant 0.5 seconde
                current_imageJM = JMAttackCC
            else:
                # Fin de l'animation d'attaque, retour à l'animation normale
                is_attacking = False
                attack_start_time = 0

        handle_pattern()

        # Mettre à jour et afficher les cochons
        update_cochons()
        draw_cochons()

        screen.blit(current_imageJM, (20, 400))  # Afficher l'image à partir du coin supérieur gauche

               # Vérifier si la touche espace est appuyée
                # Vérifier si la touche espace est appuyée

        if (is_attacking == True):
                
            for cochon in active_cochons:
                if not cochon['processed']:  # Si le cochon n'a pas été traité
                    # Vérifier si la hitbox du cochon est dans la zone
                    if cochon["hitbox"].colliderect(hitboxGoodJM) or cochon["hitbox"].colliderect(hitboxPerfectJM):
                        result, color = check_full_hitM(cochon)
                        hit_result_text = result
                        hit_result_color = color
                        last_result_time = pygame.time.get_ticks()  # Temps du dernier hit
                        cochon['processed'] = True  # Marquer ce cochon comme traité
                        result_displayed = True  # On a affiché un résultat, donc ne pas afficher "Miss"
                        break  # Sortir de la boucle

                    # Si le cochon est complètement sorti à gauche
                    elif cochon["hitbox"].right < hitboxGoodJM.left:
                        cochon['processed'] = True  # Marquer ce cochon comme traité
                        result_displayed = True  # Résultat déjà affiché, ne pas mettre "Miss"
                        misscounter += 1
                        break  # Passer au cochon suivant

            # Si aucun résultat n'a été affiché (tous les cochons sont en dehors de la zone), c'est un "Miss"
            if not result_displayed:
                hit_result_text = "Miss"
                hit_result_color = RED
                last_result_time = pygame.time.get_ticks()

        # Afficher le résultat (Perfect, Good, Miss) pendant 1 seconde
        if hit_result_text and pygame.time.get_ticks() - last_result_time < 500:
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render(hit_result_text, True, hit_result_color)
            screen.blit(text_surface, (650, 20))  # Position en haut à droite
        print(hit_result_text)

        pattern_reset_delay = 500  # 0.5 seconde de délai

        # Vérifier si tous les cochons ont été traités et réinitialiser
        if all(cochon.get('processed', False) for cochon in active_cochons):
            if pygame.time.get_ticks() - pattern_start_time > pattern_reset_delay:
                active_cochons = []
                start_new_pattern()

        # augmenter la vitesse des cochons lorsque le score dépasse 20, 50 et 100

        if score[selected_player_index] >=20 and score[selected_player_index] <50 and speed20 == False:
            speed += 2
            speed20 = True

        if score[selected_player_index] >=50 and score[selected_player_index] <100 and speed50 == False:
            speed += 3
            speed50 = True 

        if score[selected_player_index] >= 100 and speed100 == False:
            speed += 5
            speed100 = True

        print(f"Pattern choisi : {current_pattern}")
        print(f"Active cochons: {len(active_cochons)}, Pattern Index: {pattern_index}")
        screen.blit(pygame.font.SysFont(None, 36).render(f"Score : {score[selected_player_index]}", True, WHITE), (20, 20))  # Affichage du score 
        # Vérifier si le joueur a perdu
        if misscounter == 3:
            # On rentre les données de la game en fin de partie 
            sheet.append([
            date,
            players[selected_player_index].name,
            players[selected_player_index].sex,
            score[selected_player_index],
            precisionGood[selected_player_index],
            precisionPerfect[selected_player_index],
            (precisionGood[selected_player_index]+precisionPerfect[selected_player_index])/nombreDeClick[selected_player_index]*100
            ])
    
            workbook.save(EXCEL_FILE)
            current_screen = "game_over"
            game_over()

        pygame.display.flip()


    else: # Cas où m'on choisit le personnage féminin
        
        # Vérifier si l'intervalle de 0.5 seconde est passé
        if current_time - last_switch_time >= switch_interval and misscounter ==0:
            # Alterner entre JM1 et JM2
            if current_imageJF == JF1: # si on détecte JM1 dans la zone où a été chargé l'image JM1
                current_imageJF = JF2
            else:
                current_imageJF = JF1
            
            # Mettre à jour le temps de changement d'image
            last_switch_time = current_time
        
        if is_attacking and misscounter == 0:
            if current_time - attack_start_time < switch_interval:
                # Afficher l'image d'attaque pendant 0.5 seconde
                current_imageJF = JFAttack
            else:
                # Fin de l'animation d'attaque, retour à l'animation normale
                is_attacking = False
                attack_start_time = 0

        # Vérifier si l'intervalle de 0.5 seconde est passé
        if current_time - last_switch_time >= switch_interval and misscounter == 1:
            # Alterner entre JM1 et JM2
            if current_imageJF == JF1C: # si on détecte JM1 dans la zone où a été chargé l'image JM1
                current_imageJF = JF2C
            else:
                current_imageJF = JF1C
            
            # Mettre à jour le temps de changement d'image
            last_switch_time = current_time

        if is_attacking and misscounter == 1:
            if current_time - attack_start_time < switch_interval:
                # Afficher l'image d'attaque pendant 0.5 seconde
                current_imageJF = JFAttackC
            else:
                # Fin de l'animation d'attaque, retour à l'animation normale
                is_attacking = False
                attack_start_time = 0
        
        if current_time - last_switch_time >= switch_interval and misscounter == 2:
            # Alterner entre JM1 et JM2
            if current_imageJF == JF1CC: # si on détecte JM1 dans la zone où a été chargé l'image JM1
                current_imageJF = JF2CC
            else:
                current_imageJF = JF1CC
            
            # Mettre à jour le temps de changement d'image
            last_switch_time = current_time
        
        if is_attacking and misscounter == 2:
            if current_time - attack_start_time < switch_interval:
                # Afficher l'image d'attaque pendant 0.5 seconde
                current_imageJF = JFAttackCC
            else:
                # Fin de l'animation d'attaque, retour à l'animation normale
                is_attacking = False
                attack_start_time = 0

        handle_pattern()

        # Mettre à jour et afficher les cochons
        update_cochons()
        draw_cochons()

        screen.blit(current_imageJF, (20, 400))  # Afficher l'image à partir du coin supérieur gauche

               # Vérifier si la touche espace est appuyée
                # Vérifier si la touche espace est appuyée

        if (is_attacking == True):
                
            for cochon in active_cochons:
                if not cochon['processed']:  # Si le cochon n'a pas été traité
                    # Vérifier si la hitbox du cochon est dans la zone
                    if cochon["hitbox"].colliderect(hitboxGoodJF) or cochon["hitbox"].colliderect(hitboxPerfectJF):
                        result, color = check_full_hitF(cochon)
                        hit_result_text = result
                        hit_result_color = color
                        last_result_time = pygame.time.get_ticks()  # Temps du dernier hit
                        cochon['processed'] = True  # Marquer ce cochon comme traité
                        result_displayed = True  # On a affiché un résultat, donc ne pas afficher "Miss"
                        break  # Sortir de la boucle

                    # Si le cochon est complètement sorti à gauche
                    elif cochon["hitbox"].right < hitboxGoodJF.left:
                        cochon['processed'] = True  # Marquer ce cochon comme traité
                        result_displayed = True  # Résultat déjà affiché, ne pas mettre "Miss"
                        misscounter += 1
                        break  # Passer au cochon suivant

            # Si aucun résultat n'a été affiché (tous les cochons sont en dehors de la zone), c'est un "Miss"
            if not result_displayed:
                hit_result_text = "Miss"
                hit_result_color = RED
                last_result_time = pygame.time.get_ticks()

        # Afficher le résultat (Perfect, Good, Miss) pendant 1 seconde
        if hit_result_text and pygame.time.get_ticks() - last_result_time < 500:
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render(hit_result_text, True, hit_result_color)
            screen.blit(text_surface, (650, 20))  # Position en haut à droite
        print(hit_result_text)

        pattern_reset_delay = 500  # 0.5 seconde de délai

        # Vérifier si tous les cochons ont été traités et réinitialiser
        if all(cochon.get('processed', False) for cochon in active_cochons):
            if pygame.time.get_ticks() - pattern_start_time > pattern_reset_delay:
                active_cochons = []
                start_new_pattern()

        if score[selected_player_index] >=20 and score[selected_player_index] <50 and speed20 == False:
            speed += 2
            speed20 = True

        if score[selected_player_index] >=50 and score[selected_player_index] <100 and speed50 == False:
            speed += 3
            speed50 = True 

        if score[selected_player_index] >= 100 and speed100 == False:
            speed += 5
            speed100 = True

        print(f"Pattern choisi : {current_pattern}")
        print(f"Active cochons: {len(active_cochons)}, Pattern Index: {pattern_index}")
        screen.blit(pygame.font.SysFont(None, 36).render(f"Score : {score[selected_player_index]}", True, WHITE), (20, 20))  # Affichage du score 
        # Vérifier si le joueur a perdu
        if misscounter == 3:
             # On rentre les données de la game en fin de partie 
            sheet.append([
            date,
            players[selected_player_index].name,
            players[selected_player_index].sex,
            score[selected_player_index],
            precisionGood[selected_player_index],
            precisionPerfect[selected_player_index],
            (precisionGood[selected_player_index]+precisionPerfect[selected_player_index])/nombreDeClick[selected_player_index]*100
            ])
    
            workbook.save(EXCEL_FILE)
            
            current_screen = "game_over"
            game_over()

        pygame.display.flip()
        
def game_over():
    global current_screen, misscounter, speed, speed20, speed50, speed100
    
    screen.fill(BLACK)  

    draw_text("GAME OVER", big_font, RED, screen, screen.get_width() // 2, screen.get_height() // 3)
    gameover_button = Button("retourner au menu", screen.get_width() // 2 - 100, screen.get_height() // 2, 200, 50, WHITE, go_back_to_menu)
    gameover_button.draw(screen)
    misscounter =  0

    speed = 5
    speed20 = False
    speed50 = False
    speed100 = False
    # Rafraîchir l'écran pour afficher les éléments
    pygame.display.update()

running = True
# Dans la boucle principale, on gère l'affichage des différents écrans
while running:

    # affichage du fond
    screen.fill(BLACK)    

    if current_screen == "menu":
        screen.blit(image_menu, (0, 0))  # (0, 0) pour afficher l'image à partir du coin supérieur gauche  
        for button in buttons:
            #Si la souris est dans la zone du bouton 
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if button.text == "Créer un joueur" or button.text == "Joueur":
                    draw_text(button.text, font, (255, 255, 0), screen, button.rect.centerx, button.rect.centery)
                elif button.text == "Quitter":
                    draw_text(button.text, font, RED, screen, button.rect.centerx, button.rect.centery)
            else:
                button.draw(screen)


    elif current_screen == "create_player":
        screen.blit(image_menu, (0, 0))  

        draw_text("Créer un joueur", font, WHITE, screen, 400, 50)
        draw_text(message, font, WHITE, screen, 400, 100)
        draw_text(f"Nom : {input_text}", font, WHITE, screen, 400, 200)

        for button in sex_buttons:
            button.draw(screen)
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                draw_text(button.text, font, GREEN, screen, button.rect.centerx, button.rect.centery)  
            else:
                button.draw(screen)

        confirm_button = Button("Confirmer", 200, 500, 150, 50, BLUE, confirm_create_player)
        return_button = Button("Retour", 450, 500, 150, 50, RED, cancel_create_player)
        confirm_button.draw(screen)
        return_button.draw(screen)

        for button in [confirm_button, return_button]:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                # Si la souris est sur le bouton Confirmer, couleur jaune
                if button == confirm_button:
                    draw_text(button.text, font, (255, 255, 0), screen, button.rect.centerx, button.rect.centery)
                # Si la souris est sur le bouton Retour, couleur rouge
                elif button == return_button:
                    draw_text(button.text, font, (255, 0, 0), screen, button.rect.centerx, button.rect.centery)
            else:
                draw_text(button.text, font, WHITE, screen, button.rect.centerx, button.rect.centery)


    elif current_screen == "select_player":
        screen.blit(image_menu, (0, 0))  

        draw_player_list()

    elif current_screen == "game" and game_started:
        if game_paused:
            # Afficher l'écran de pause si le jeu est en pause
            draw_pause_screen()
        else:
            draw_game_screen()  # Afficher l'écran de jeu

    elif current_screen == "score_screen": 
            draw_score_screen()
            retour_button = Button("Retour", 0, 400, 150, 50, RED, action=go_back_to_select_player)
            retour_button.draw(screen)
            if retour_button.rect.collidepoint(pygame.mouse.get_pos()):
                    draw_text(retour_button.text, font, RED, screen, retour_button.rect.centerx, retour_button.rect.centery)

    elif current_screen == "game_over":
        game_over()
        gameover_button = Button("retourner au menu", screen.get_width() // 2 - 100, screen.get_height() // 2, 200, 50, WHITE, go_back_to_menu)
        gameover_button.draw(screen)

    elif current_screen == "leaderboard": 
        leaderboard()

    # try:
    #     while True:
    #         if ser.in_waiting > 0:
    #             data = ser.readline().decode().strip()  # Lire la ligne envoyée par l'Arduino
    #             if data == "BUTTON_PRESSED":
    #                 print("Bouton appuyé détecté ! 💅")
    # except KeyboardInterrupt:
    #     print("Arrêt du programme.")
    # finally:
    #     ser.close()
        # Gestion des événements
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if current_screen == "create_player":
                handle_input(event)
            elif current_screen == "select_player" and event.key == pygame.K_ESCAPE:
                go_back_to_menu()
            elif current_screen == "leaderboard" and event.key == pygame.K_ESCAPE:
                current_screen = "select_player"
            if current_screen == "game" and event.key == pygame.K_SPACE and not is_attacking: #if current_screen == "game" and (event.key == pygame.K_SPACE or data == "BUTTON_PRESSED") and not is_attacking:
                # Début de l'attaque
                is_attacking = True
                spell_channel.play(pygame.mixer.Sound("MagicSpell.mp3"))
                attack_start_time = pygame.time.get_ticks()
            if event.key == pygame.K_p:
                game_paused = True
                

        elif event.type == pygame.MOUSEBUTTONDOWN: # pos prend la position càd coordonnées (x, y) du click de souris
            pos = pygame.mouse.get_pos()

            if current_screen == "menu":
                for button in buttons:
                    button.click(pos)
            
            elif current_screen == "create_player":
                for button in sex_buttons:
                    button.click(pos)
                confirm_button.click(pos)
                return_button.click(pos)
            

            # Dans la boucle principale, vérifier les clics de souris pour ces boutons
            elif current_screen == "select_player":
                for i, player in enumerate(players):
                    if 150 + i * 60 <= pos[1] <= 180 + i * 60: # on vérifie si on a cliqué sur une zone où est affiché le joueur 
                        selected_player_index = i
                    # Dans la boucle principale, dessiner les boutons "Start" et "Delete" pour chaque joueur sélectionné
                    if selected_player_index is not None:
                        y_offset = 150 + selected_player_index * 60
                        start_button = Button("Start", 150, y_offset + 20, 150, 30, BLUE, start_game_with_player)
                        delete_button = Button("Supprimer", 500, y_offset + 20, 150, 30, RED, delete_selected_player)
                        score_button = Button("Score", 320, y_offset + 20, 150, 30, WHITE, show_score)

                        start_button.draw(screen)
                        delete_button.draw(screen)
                        score_button.draw(screen)

                        for button in [start_button, delete_button, score_button]:
                            if button.rect.collidepoint(pygame.mouse.get_pos()):
                                if button == start_button:
                                    draw_text(button.text, font, (255, 255, 0), screen, button.rect.centerx, button.rect.centery)
                            elif button == delete_button:
                                draw_text(button.text, font, (255, 0, 0), screen, button.rect.centerx, button.rect.centery)
                            elif button == score_button:
                                draw_text(button.text, font, BLUE, screen, button.rect.centerx, button.rect.centery)
                        else:
                            draw_text(button.text, font, WHITE, screen, button.rect.centerx, button.rect.centery)
                        
                        start_button.click(pos)
                        delete_button.click(pos)
                        score_button.click(pos)
                
                leaderboard_button = Button("LeaderBoard", 320, 450, 150, 30, WHITE, show_leaderboard)
                leaderboard_button.draw(screen)
                leaderboard_button.click(pos)
                if leaderboard_button.rect.collidepoint(pygame.mouse.get_pos()):
                    draw_text(leaderboard_button.text, font, BLUE, screen, button.rect.centerx, button.rect.centery)


            elif current_screen == "game": 
                continue_button.click(event.pos)
                quitter_button.click(event.pos)

            elif current_screen == "score_screen":
                score_button.click(pos)
                retour_button = Button("Retour", 0, 400, 150, 50, RED, action=go_back_to_select_player)
                retour_button.click(pos)

            elif current_screen == "game_over":
                gameover_button = Button("retourner au menu", screen.get_width() // 2 - 100, screen.get_height() // 2, 200, 50, WHITE, go_back_to_menu)
                gameover_button.click(pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()









# #Start the game loop 
# running = True; 
# while running : 
#     for event in pygame.event.get(): 
#         if event.type == pygame.QUIT: 
#             running = False 
#     # Fill the screen with a color 
#     screen.fill((0, 0, 0))
#     # Updates the WHOLE screen 
#     pygame.display.flip()
#     # or update only a part of the screen - w/o an argument it updates the whole screen 
#     # pygame.display.update(objects_to_update)
#     clock.tick(60)
# pygame.quit()


