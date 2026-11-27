import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:
    """Contrôleur du jeu.

    Il fait tourner la boucle principale, lit les événements du clavier,
    les traduit en actions sur le modèle, puis demande à la vue de dessiner.
    Le comportement des touches dépend de l'état du jeu (menu ou course).
    """

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))        # Ouvre l'ecran du jeu aux dimensions Largeur*Longueur (Dimension venant du fichier constant.py)
        self.clock = pygame.time.Clock()         
        self.model = GameModel()                                                    # Creation du modele.
        self.view = GameView(self.screen)                                           # Creation de la vue.
        self.input_handler = InputHandler()                                         # Creation de l'objet qui lit le clavier
        self.running = True                                                         # Tant que running est True, le jeu continue.

    def run(self) -> None:
        """Boucle principale : une itération correspond à une frame (FPS fois par seconde).

        À chaque frame : on traite les événements, on met à jour le modèle,
        on dessine, puis on attend pour garder une vitesse constante.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """Traite les événements ponctuels : fermeture de la fenêtre et appuis sur une touche."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Envoie la touche appuyée au traitement correspondant à l'état courant du jeu."""
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.RACING:
            self.handle_racing_key(key)
        elif state == GameState.RESULTS:
            self.handle_results_key(key)

    def handle_menu_key(self, key: int) -> None:
        """Dans le menu : Entrée lance la course, Échap quitte le jeu."""
        if key == pygame.K_RETURN:
            self.model.start_race()
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_racing_key(self, key: int) -> None:
        """Pendant la course : Échap ramène au menu principal."""
        if key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def handle_results_key(self, key: int) -> None:
        """Sur l'écran des résultats : Entrée relance une course, Échap ramène au menu."""
        if key == pygame.K_RETURN:
            self.model.start_race()   # nouvelle course, tours et chrono remis à zéro
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self) -> None:
        """Pendant la course, lit les touches maintenues et met à jour le modèle.

        Chaque joueur conduit sa propre voiture : le joueur 1 avec Z Q S D,
        le joueur 2 avec les flèches.
        """
        if self.model.state != GameState.RACING:
            return

        for index, player in enumerate(self.model.players):
            player_input = self.input_handler.get_inputs(index)
            self.apply_input(player.car, player_input)
        self.model.update()

    def apply_input(self, car, player_input: dict) -> None:
        """Transmet à la voiture les commandes demandées pendant cette frame.

        player_input est un dictionnaire {action: bool}. On utilise get(..., False) :
        une action absente du dictionnaire (touche pas encore définie) est ignorée.
        """
        if player_input.get('accelerate', False):
            car.accelerate()
        if player_input.get('brake', False):
            car.brake()
        if player_input.get('turn_left', False):
            car.turn_left()
        if player_input.get('turn_right', False):
            car.turn_right()

    def render(self) -> None:
        """Demande à la vue de dessiner l'état actuel du modèle."""
        self.view.draw(self.model)

    def quit(self) -> None:
        """Ferme pygame et arrête le programme."""
        self.running = False
        pygame.quit()
        sys.exit()
