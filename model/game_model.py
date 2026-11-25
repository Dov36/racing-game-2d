from constants import GameState, GRID_ROWS, GRID_COLS, TILE_SIZE
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:
    """Modèle du jeu (M de MVC) : l'état courant du jeu, le circuit et la voiture.

    Le modèle ne lit pas le clavier et ne dessine rien.
    """

    def __init__(self):
        self.state: str = GameState.MENU      # état courant de l'automate du jeu
        self.circuit: Circuit | None = None   # créé au lancement de la course
        self.car: Car | None = None

    def load_circuit(self) -> None:
        """Construit un circuit de GRID_ROWS lignes et GRID_COLS colonnes de cases de route,
        puis place la voiture au départ."""
        grid = [[RoadTile(col=col_idx, row=row_idx)
                 for col_idx in range(GRID_COLS)]
                for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        """Crée la voiture au centre de sa case de départ (colonne 7, ligne 1).

        La voiture travaille en pixels : on convertit donc la case en coordonnées.
        """
        start_col, start_row = 7, 1
        x = start_col * TILE_SIZE + TILE_SIZE / 2
        y = start_row * TILE_SIZE + TILE_SIZE / 2
        self.car = Car(x, y)

    def update(self) -> None:
        """Fait avancer le jeu d'une frame : la voiture se déplace seulement pendant la course."""
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update()
