from constants import GameState, TILE_SIZE
from model.car import Car
from model.circuit import Circuit
from model.player import Player
from model.race import RaceManager
from model.tracks import TRACK_TEXT, TRACK_START_ANGLE, TRACK_LAPS


class GameModel:
    """Modèle du jeu (M de MVC) : l'état courant du jeu, le circuit et les deux joueurs.

    Le modèle ne lit pas le clavier et ne dessine rien.
    """

    def __init__(self):
        self.state: str = GameState.MENU      # état courant de l'automate du jeu
        self.circuit: Circuit | None = None   # construit au lancement de la course
        # Indice 0 : joueur 1, indice 1 : joueur 2 (comme dans InputHandler)
        self.players: list[Player] = [Player("Joueur 1"), Player("Joueur 2")]
        # Le RaceManager de Timothée : c'est lui qui compte les tours et le temps.
        # On en recrée un neuf à chaque course, sinon on garderait les tours d'avant.
        self.race: RaceManager | None = None

    def start_race(self) -> None:
        """Lance une nouvelle course depuis le début.

        Sert à la fois quand on appuie sur Entrée dans le menu et quand on
        rejoue depuis l'écran des résultats : tout repart de zéro.
        """
        self.load_circuit()
        self.state = GameState.RACING

    def load_circuit(self) -> None:
        """Construit le circuit (TRACK_TEXT), puis place les deux voitures au départ."""
        self.circuit = Circuit.from_text(TRACK_TEXT)
        self.spawn_cars()
        self.race = RaceManager(self.circuit, TRACK_LAPS, len(self.players))

    def spawn_cars(self) -> None:
        """Crée une voiture par joueur, sur sa case de départ : bloc "1" pour le
        joueur 1, bloc "2" pour le joueur 2."""
        for index, player in enumerate(self.players):
            start = self.circuit.find_block(str(index + 1))[0]
            player.car = Car(start.col, start.row, TRACK_START_ANGLE)

    def update(self) -> None:
        """Fait avancer le jeu d'une frame.

        Chaque voiture bouge, puis on dit au RaceManager sur quelle case elle
        est arrivée (c'est comme ça qu'il voit les portes et la ligne d'arrivée).
        Dès qu'un joueur a fini tous ses tours, on passe à l'écran des résultats.
        """
        if self.state != GameState.RACING or self.circuit is None:
            return

        for index, player in enumerate(self.players):
            self._update_car(player.car)
            tile = self.circuit.get_tile_at_pixel(player.car.x, player.car.y)
            self.race.update_player(index, tile)

        self.race.tick()   # le chrono avance d'une frame

        if self.race.is_finished():
            self.state = GameState.RESULTS

    def _update_car(self, car: Car) -> None:
        """Applique à une voiture les effets de la case où elle se trouve.

        - hors de la carte ou sur le vide : elle réapparaît au dernier point de passage ;
        - sur un point de passage (C) : il devient son point de réapparition ;
        - sur un boost (B) : elle est poussée vers l'avant ;
        puis elle lit le terrain de la case et se déplace.
        """
        tile = self.circuit.get_tile_at_pixel(car.x, car.y)

        if tile is None or not tile.physics.is_drivable():
            car.respawn()
            return

        if tile.block == "C":
            # On réapparaîtra au centre de cette case
            car.set_respawn_point(tile.col * TILE_SIZE + TILE_SIZE // 2,
                                  tile.row * TILE_SIZE + TILE_SIZE // 2)
        elif tile.block == "B":
            car.boost()

        car.terrain = tile.physics
        car.update_physics()
