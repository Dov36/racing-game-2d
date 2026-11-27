import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, CAR_WIDTH, CAR_HEIGHT,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel



# Couleur de la voiture de chaque joueur (indice 0 : joueur 1, indice 1 : joueur 2)
PLAYER_COLORS = [
    (230, 60, 60),    # joueur 1 : rouge
    (60, 120, 230),   # joueur 2 : bleu
]

# Couleur de fond de chaque terrain (le nom vient de tile.terrain)
TERRAIN_COLORS = {
    "road": (90, 90, 100),     # route : gris
    "grass": (70, 150, 70),    # herbe : vert
    "dirt": (150, 105, 60),    # terre : marron
    "ice": (170, 220, 245),    # glace : bleu clair
    "void": (10, 10, 18),      # vide : presque noir
}


class GameView:
    """Vue du jeu (V de MVC) : dessine l'état du modèle avec pygame.

    La vue lit le modèle mais ne le modifie jamais.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

    def draw(self, model: GameModel) -> None:
        """Efface l'écran, dessine l'écran correspondant à l'état du jeu, puis l'affiche."""
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        """Dessine le menu principal : le titre et les deux boutons."""
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        """Dessine la course : les cases du circuit, la voiture, puis les informations."""
        if model.circuit is None:
            return

        for tile in model.circuit.tiles():
            self._draw_tile(tile)

        for index, player in enumerate(model.players):
            self._draw_car(player.car, PLAYER_COLORS[index])
        self._draw_hud(model.players)

    def _draw_tile(self, tile) -> None:
        """Dessine une case : la couleur de son terrain, puis son bloc éventuel."""
        rect = pygame.Rect(tile.col * TILE_SIZE, tile.row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, TERRAIN_COLORS.get(tile.terrain, COLOR_BG), rect)

        if tile.block == "L":                      # ligne d'arrivée : damier
            self._draw_checkered(rect)
        elif tile.block == "C":                    # point de passage : cadre jaune
            pygame.draw.rect(self.screen, COLOR_ACCENT, rect, 4)
        elif tile.block == "B":                    # boost : carré orange
            pygame.draw.rect(self.screen, (255, 140, 0), rect.inflate(-16, -16), border_radius=6)
        elif tile.block in ("1", "2"):             # départs : le numéro du joueur
            text = self.font.render(tile.block, True, COLOR_TEXT)
            self.screen.blit(text, text.get_rect(center=rect.center))

        if tile.terrain != "void":
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)   # quadrillage

    def _draw_checkered(self, rect: pygame.Rect) -> None:
        """Dessine un damier noir et blanc dans la case (ligne d'arrivée)."""
        square = TILE_SIZE // 4
        for i in range(4):
            for j in range(4):
                color = (240, 240, 240) if (i + j) % 2 == 0 else (20, 20, 20)
                pygame.draw.rect(self.screen, color,
                                 (rect.x + i * square, rect.y + j * square, square, square))



    def _draw_car(self, car, color: tuple[int, int, int]) -> None:
        """Dessine une voiture : un rectangle de la couleur du joueur, tourné selon son angle.

        Le rectangle est d'abord dessiné tourné vers la droite (angle 0),
        et la bande blanche (le pare-brise) indique l'avant de la voiture.
        """
        body = pygame.Surface((CAR_HEIGHT, CAR_WIDTH), pygame.SRCALPHA)
        pygame.draw.rect(body, color, body.get_rect(), border_radius=6)
        pygame.draw.rect(body, (255, 255, 255), (CAR_HEIGHT - 16, 4, 8, CAR_WIDTH - 8), border_radius=2)
        rotated = pygame.transform.rotate(body, car.angle)   # rotate tourne dans le sens trigonométrique
        self.screen.blit(rotated, rotated.get_rect(center=(int(car.x), int(car.y))))

    def _draw_hud(self, players) -> None:
        """Affiche en bas de l'écran la vitesse de chaque joueur et un rappel des commandes.

        Le bandeau est semi-transparent pour laisser voir le circuit en dessous.
        """
        lines = [
            (f"{player.display_name()} : {player.car.speed:5.2f} px/frame", PLAYER_COLORS[index])
            for index, player in enumerate(players)
        ]
        lines.append(("J1 : Z Q S D     J2 : flèches     Échap : menu", COLOR_TEXT))
        panel_height = 16 + len(lines) * 26
        panel = pygame.Surface((WINDOW_WIDTH, panel_height), pygame.SRCALPHA)
        panel.fill((*COLOR_PANEL, 200))   # 200 sur 255 : légèrement transparent
        top = WINDOW_HEIGHT - panel_height
        self.screen.blit(panel, (0, top))
        for i, (line, color) in enumerate(lines):
            text = self.small_font.render(line, True, color)
            self.screen.blit(text, (14, top + 8 + i * 26))
