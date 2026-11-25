import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, CAR_WIDTH, CAR_HEIGHT,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


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

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        self._draw_car(model.car)
        self._draw_hud(model.car)

    def _draw_car(self, car) -> None:
        """Dessine la voiture : un rectangle rouge tourné selon son angle.

        Le rectangle est d'abord dessiné tourné vers la droite (angle 0),
        et la bande blanche (le pare-brise) indique l'avant de la voiture.
        """
        body = pygame.Surface((CAR_HEIGHT, CAR_WIDTH), pygame.SRCALPHA)
        pygame.draw.rect(body, (230, 60, 60), body.get_rect(), border_radius=6)
        pygame.draw.rect(body, (255, 255, 255), (CAR_HEIGHT - 16, 4, 8, CAR_WIDTH - 8), border_radius=2)
        rotated = pygame.transform.rotate(body, car.angle)   # rotate tourne dans le sens trigonométrique
        self.screen.blit(rotated, rotated.get_rect(center=(int(car.x), int(car.y))))

    def _draw_hud(self, car) -> None:
        """Affiche en bas de l'écran la vitesse et l'angle de la voiture, et un rappel des commandes.

        Le bandeau est semi-transparent pour laisser voir le circuit en dessous.
        """
        lines = [
            (f"Vitesse : {car.speed:5.2f} px/frame     Angle : {car.angle % 360:5.1f}°", COLOR_ACCENT),
            ("Z / ↑ : avancer   S / ↓ : freiner, reculer   Q D / ← → : tourner   Échap : menu", COLOR_TEXT),
        ]
        panel_height = 16 + len(lines) * 26
        panel = pygame.Surface((WINDOW_WIDTH, panel_height), pygame.SRCALPHA)
        panel.fill((*COLOR_PANEL, 200))   # 200 sur 255 : légèrement transparent
        top = WINDOW_HEIGHT - panel_height
        self.screen.blit(panel, (0, top))
        for i, (line, color) in enumerate(lines):
            text = self.small_font.render(line, True, color)
            self.screen.blit(text, (14, top + 8 + i * 26))
