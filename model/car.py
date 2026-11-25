""" voiture représentée par sa position, angle, vitesse, sur un sol vide """
import math

from constants import (
    AIR_FRICTION, CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_REVERSE, CAR_TURN_SPEED,
    WINDOW_HEIGHT, WINDOW_WIDTH,
)


class Car:
    """Modèle MVC : Car est le modèle, elle ne fait que calculer le mouvement, le contrôleur lit le clavier, et la vue dessine"""

    def __init__(self, x: float, y: float, angle: float = 0.0):
        self.x = x  # position en pixels
        self.y = y
        self.angle = angle  # en degrés sens trigonométrique, 0 = droite
        self.speed = 0.0  # En pixels par frame ; négatif = marche arrière

    def forward(self) -> tuple[float, float]:
        rad = math.radians(self.angle)
        return math.cos(rad), -math.sin(rad)  # - car l'axe y de l'écran descend

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION

    def brake(self) -> None:
        self.speed -= CAR_BRAKE
        if self.speed < -CAR_MAX_REVERSE:  # Limite la marche arrière
            self.speed = -CAR_MAX_REVERSE

    def turn_left(self) -> None:
        self.angle += CAR_TURN_SPEED  # Sens trigo : l'angle qui augmente fait tourner vers la gauche

    def turn_right(self) -> None:
        self.angle -= CAR_TURN_SPEED

    def update(self) -> None:
        # Mise à jour de la vitesse de la voiture en fonction de la friction de l'air, puis de sa position 
        self.speed *= AIR_FRICTION
        fx, fy = self.forward()
        # Quand la voiture avance vers un côté, le % fait ressortir la voiture sur le coté opposé de l'écran
        self.x = (self.x + self.speed * fx) % WINDOW_WIDTH
        self.y = (self.y + self.speed * fy) % WINDOW_HEIGHT