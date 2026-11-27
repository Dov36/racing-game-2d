""" voiture avec une vitesse en vecteur (vx, vy) pour pouvoir déraper selon le terrain """
import math

from constants import (
    AIR_FRICTION, BOOST_ACCELERATION, CAR_ACCELERATION, CAR_BRAKE,
    CAR_MAX_REVERSE, CAR_TURN_SPEED, TILE_SIZE,
)
from model.terrain import Terrain, TERRAINS


class Car:
    """La voiture (modèle) : position, vitesse et angle, sans dessin.
    La vitesse (vx, vy) est séparée de l'angle : le nez tourne tout de suite,
    mais la vitesse ne suit que grâce à l'adhérence du terrain, sinon on dérape."""

    def __init__(self, start_col: int, start_row: int, start_angle: float = 0.0):
        # On reçoit une case, on place la voiture au centre de cette case
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.vx: float = 0.0  # en pixels par frame, y vers le bas comme l'écran
        self.vy: float = 0.0
        self.angle: float = start_angle  # en degrés, 0 = droite, 90 = haut
        self.terrain: Terrain = TERRAINS["road"]  # changé à chaque frame par GameModel
        self.drifting: bool = False
        # Si on tombe avant le premier point de passage, on revient au départ
        self.respawn_x = self.x
        self.respawn_y = self.y
        self.respawn_angle = start_angle

    def forward(self) -> tuple[float, float]:
        """Vecteur unitaire dans la direction du nez de la voiture."""
        rad = math.radians(self.angle)
        return math.cos(rad), -math.sin(rad)  # - car l'axe y de l'écran descend

    @property
    def speed(self) -> float:
        """Vitesse vers l'avant (négative en marche arrière)."""
        fx, fy = self.forward()
        return self.vx * fx + self.vy * fy  # produit scalaire avec le nez

    @speed.setter
    def speed(self, value: float) -> None:
        """Change la vitesse vers l'avant sans toucher à la glissade de côté."""
        fx, fy = self.forward()
        delta = value - self.speed
        self.vx += delta * fx
        self.vy += delta * fy

    def accelerate(self) -> None:
        """Le moteur pousse vers l'avant, selon la traction du terrain."""
        self.speed += CAR_ACCELERATION * self.terrain.traction

    def brake(self) -> None:
        """Freine, puis recule si on continue à freiner à l'arrêt."""
        # Au moins 30 % du freinage, même si le terrain n'accroche presque pas
        self.speed -= CAR_BRAKE * max(self.terrain.traction, 0.3)
        if self.speed < -CAR_MAX_REVERSE:
            self.speed = -CAR_MAX_REVERSE

    def boost(self) -> None:
        """Poussée d'un bloc de boost."""
        self.speed += BOOST_ACCELERATION

    def turn_left(self) -> None:
        self.angle += self._turn_rate()

    def turn_right(self) -> None:
        self.angle -= self._turn_rate()

    def _turn_rate(self) -> float:
        """Degrés par frame, un peu plus en dérapage."""
        # Tourner plus vite en dérapage aide à contre-braquer
        return CAR_TURN_SPEED * 1.15 if self.drifting else CAR_TURN_SPEED

    def update_physics(self) -> None:
        """Adhérence, dérapage et frottements selon le terrain, puis déplacement."""
        terrain = self.terrain
        fx, fy = self.forward()
        # forward : vitesse dans l'axe du nez, lateral : vitesse de côté (la glissade)
        forward = self.vx * fx + self.vy * fy
        lateral = -self.vx * fy + self.vy * fx

        # Les pneus enlèvent une part grip de la glissade à chaque frame.
        # Au-dessus du seuil du terrain, ils décrochent : on dérape.
        grip = terrain.grip
        self.drifting = abs(lateral) > terrain.drift_threshold
        if self.drifting:
            grip *= terrain.drift_grip
            forward *= terrain.drift_friction
        lateral *= 1 - min(grip, 1.0)

        # Frottement de l'air × traction : même vitesse max sur tous les terrains
        drag = (1 - AIR_FRICTION) * terrain.traction
        forward *= (1 - drag) * terrain.rolling_friction
        lateral *= (1 - drag) * terrain.rolling_friction

        # On remet les deux parties ensemble dans le repère de l'écran, puis on avance
        self.vx = forward * fx - lateral * fy
        self.vy = forward * fy + lateral * fx
        self.x += self.vx
        self.y += self.vy

    def set_respawn_point(self, x: float, y: float) -> None:
        """Mémorise l'endroit où réapparaître (sur un point de passage)."""
        self.respawn_x = x
        self.respawn_y = y
        self.respawn_angle = self.angle

    def respawn(self) -> None:
        """Replace la voiture au dernier point de passage, avec une vitesse nulle."""
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.angle = self.respawn_angle
        self.vx = self.vy = 0.0
        self.drifting = False
