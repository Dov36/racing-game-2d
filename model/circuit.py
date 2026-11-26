"""Le circuit : une grille de cases construite à partir d'un texte."""
from constants import TILE_SIZE
from model.road_tile import RoadTile
from model.terrain import TERRAINS
from model.tracks import TILE_CODES


class Circuit:
    """Grille de cases (RoadTile), rangée ligne par ligne.

    Le circuit ne dessine rien et ne connaît pas les voitures. On le fabrique
    avec Circuit.from_text.
    """

    def __init__(self, grid: list[list[RoadTile]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    @classmethod
    def from_text(cls, lines: list[str]) -> "Circuit":
        """Construit un circuit à partir d'une liste de chaînes.

        Chaque caractère devient une case d'après TILE_CODES. Toutes les
        lignes doivent avoir la même longueur, sinon on lève une ValueError
        (comme pour un caractère inconnu).
        """
        if not lines:
            raise ValueError("Un circuit doit avoir au moins une ligne")
        width = len(lines[0])
        grid = []
        for row, line in enumerate(lines):
            if len(line) != width:
                raise ValueError(
                    f"Ligne {row} : {len(line)} caractères au lieu de {width}")
            tiles = []
            for col, char in enumerate(line):
                if char not in TILE_CODES:
                    raise ValueError(
                        f"Caractère inconnu {char!r} (ligne {row}, colonne {col})")
                terrain, block = TILE_CODES[char]
                tiles.append(RoadTile(col, row, terrain, block,
                                      TERRAINS[terrain]))
            grid.append(tiles)
        return cls(grid)

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        """Renvoie la case (col, row), ou None hors de la grille."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        """Renvoie la case qui contient le pixel (px, py).

        La division entière par TILE_SIZE donne la colonne et la ligne. En
        dehors de la grille on renvoie None : l'extérieur de la carte est
        traité comme du vide par le modèle du jeu.
        """
        return self.get_tile(int(px // TILE_SIZE), int(py // TILE_SIZE))

    def find_block(self, block: str) -> list[RoadTile]:
        """Liste les cases qui portent ce bloc, ligne par ligne."""
        return [tile for tile in self.tiles() if tile.block == block]

    def tiles(self):
        """Parcourt toutes les cases, ligne par ligne."""
        for row in self.grid:
            yield from row

    def pixel_width(self) -> int:
        """Largeur du circuit en pixels."""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Hauteur du circuit en pixels."""
        return self.rows * TILE_SIZE
