import pygame


# Touches des 2 joueurs sur un même clavier
PLAYER_1_MAPPING = {
    pygame.K_z:      "accelerate",
    pygame.K_w:      "accelerate",
    pygame.K_s:      "brake",
    pygame.K_q:      "turn_left",
    pygame.K_a:      "turn_left",
    pygame.K_d:      "turn_right",
}

PLAYER_2_MAPPING = {
    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:   "brake",
    pygame.K_LEFT:   "turn_left",
    pygame.K_RIGHT:  "turn_right",
}

# Liste des joueurs, indice 0 : joueur 1, indice 1 : joueur 2
MAPPINGS = [PLAYER_1_MAPPING, PLAYER_2_MAPPING]


class InputHandler:
    """InputHandler : partie contrôleur du MVC qui lit le clavier des 2 joueurs en continu"""

    def __init__(self):
        self.mappings = MAPPINGS

    def get_inputs(self, player_index: int) -> dict:
        """La méthode prend l'index 0 ou 1 correspondant à un des 2 joueurs
        et renvoie un dictionnaire des actions activées par ce joueur"""
        mapping = self.mappings[player_index]
        # Tableau de booléens des touches avec True pour une qui est enfoncée
        keys = pygame.key.get_pressed()
        # Toutes les actions sont initialisées à False
        p = {action: False for action in mapping.values()}

        for key, action in mapping.items():
            if keys[key]:
                p[action] = True

        return p
