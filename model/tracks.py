"""Description des circuits sous forme de texte.

Un circuit est une liste de 12 chaînes de 16 caractères : un caractère par
case. Le dictionnaire TILE_CODES traduit chaque caractère en (terrain, bloc).

Terrains : R route, H herbe, T terre, G glace, W eau, . vide.
Blocs    : C point de passage, L ligne d'arrivée, 1 et 2 départs des joueurs,
B boost.
"""

TILE_CODES = {
    ".": ("void", None),
    "R": ("road", None),
    "H": ("grass", None),
    "T": ("dirt", None),
    "G": ("ice", None),
    "C": ("road", "C"),
    "L": ("road", "L"),
    "1": ("road", "1"),
    "2": ("road", "2"),
    "B": ("road", "B"),
}

# Premier circuit : un anneau de 2 cases de large, 3 tours.
TRACK_TEXT = [
    "................",
    "...RR1RLRRBHH...",
    "..RRR2RLRRBRRR..",
    ".RR..........RR.",
    ".RR..........RR.",
    ".CC..........CC.",
    ".TT..........RR.",
    ".TT..........BB.",
    ".RR..........RR.",
    "..RRGGGRCRRBRR..",
    "...RGGGRCRRBR...",
    "................",
]
TRACK_LAPS = 3
TRACK_START_ANGLE = 0  # les voitures partent vers la droite
