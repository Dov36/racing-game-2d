from constants import GameState
from model.car import Car
from model.circuit import Circuit
from model.tracks import TRACK_TEXT, TRACK_START_ANGLE


class GameModel:
    """Modèle du jeu (M de MVC) : l'état courant du jeu, le circuit et la voiture.

    Le modèle ne lit pas le clavier et ne dessine rien.
    """

    def __init__(self):
        self.state: str = GameState.MENU      # état courant de l'automate du jeu
        self.circuit: Circuit | None = None   # construit au lancement de la course
        self.car: Car | None = None

    def load_circuit(self) -> None:
        """Construit le circuit (TRACK_TEXT), puis place la voiture sur la case de départ."""
        self.circuit = Circuit.from_text(TRACK_TEXT)
        self.spawn_car()

    def spawn_car(self) -> None:
        """Crée la voiture sur la case de départ du joueur 1 (bloc "1").

        find_block renvoie la liste des cases qui portent ce bloc :
        on prend la première.
        """
        start = self.circuit.find_block("1")[0]
        self.car = Car(start.col, start.row, TRACK_START_ANGLE)

    def update(self) -> None:
        """Fait avancer le jeu d'une frame : la voiture lit le terrain
        de sa case, puis se déplace."""
        if self.state != GameState.RACING or self.circuit is None:
            return
        tile = self.circuit.get_tile_at_pixel(self.car.x, self.car.y)
        if tile is not None:
            self.car.terrain = tile.physics
        self.car.update_physics()