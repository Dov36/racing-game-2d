"""Case élémentaire de la grille d'un circuit."""


class RoadTile:
    """Une case du circuit.

    Elle ne contient que des données : sa position (col, row), le nom de son
    terrain, son bloc éventuel (C, L, B, 1, 2...) et l'objet Terrain d'Isaac
    (physics) que la voiture lit pour sa physique. C'est la vue qui la dessine.
    """

    def __init__(self, col: int, row: int, terrain: str, block, physics):
        self.col = col
        self.row = row
        self.terrain = terrain
        self.block = block
        self.physics = physics
