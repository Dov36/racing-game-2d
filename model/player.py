""" joueur de la course """
from model.car import Car


class Player:
    """Un joueur : son nom et sa voiture pendant la course."""

    def __init__(self, default_name: str):
        self.default_name = default_name  # "Joueur 1" ou "Joueur 2"
        self.car: Car | None = None       # créée par GameModel au début de la course

    def display_name(self) -> str:
        """Renvoie le nom à afficher."""
        return self.default_name
