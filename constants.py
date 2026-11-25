WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

# --- Voiture ---
CAR_ACCELERATION = 0.05   # ajouté à la vitesse à chaque frame où l'on accélère
CAR_BRAKE = 0.1           # retiré à la vitesse à chaque frame où l'on freine
CAR_TURN_SPEED = 3.0      # degrés de rotation par frame
CAR_MAX_REVERSE = 2.0     # vitesse maximale en marche arrière

# La vitesse est multipliée par ce coefficient à chaque frame : c'est le frottement de l'air.
# Il limite la vitesse maximale (environ 5 pixels/frame) et fait ralentir la voiture
# quand on lâche l'accélérateur.

AIR_FRICTION = 0.99

CAR_WIDTH = 30
CAR_HEIGHT = 50


class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_GRID = (50, 54, 66)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
