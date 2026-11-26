"""Les terrains du circuit et leurs paramètres physiques, lus par la voiture.
Terrain est la classe abstraite ; DrivableTerrain (Road, Grass, Dirt, Ice)
et HoleTerrain (Void) en héritent."""
from abc import ABC, abstractmethod


class Terrain(ABC):
    """Classe abstraite de tous les terrains : on ne peut pas créer un Terrain,
    seulement ses classes filles. La voiture lit ses paramètres pour accélérer,
    freiner et déraper selon le sol."""

    name = "terrain"
    # Paramètres par défaut, chaque terrain redéfinit les siens
    traction = 1.0          # part de l'accélération et du freinage transmise au sol
    grip = 0.3              # part de la glissade de côté supprimée à chaque frame
    drift_threshold = 1.5   # vitesse de côté (px/frame) à partir de laquelle on dérape
    drift_grip = 0.4        # multiplie grip pendant un dérapage
    drift_friction = 0.99   # ralentissement pendant un dérapage
    rolling_friction = 1.0  # ralentissement normal sur ce terrain (1 = aucun)

    @abstractmethod
    def is_drivable(self) -> bool:
        """Méthode abstraite que les classes filles doivent réécrire : renvoie
        True pour un DrivableTerrain et False pour un HoleTerrain."""


class DrivableTerrain(Terrain, ABC):
    """Classe fille de Terrain pour les terrains où l'on peut rouler :
    is_drivable renvoie True."""

    def is_drivable(self) -> bool:
        return True


class HoleTerrain(Terrain, ABC):
    """Classe fille de Terrain pour les trous où l'on ne peut pas rouler :
    is_drivable renvoie False."""

    # On ne roule pas dessus : aucune adhérence
    traction = 0.0
    grip = 0.0

    def is_drivable(self) -> bool:
        return False


class Road(DrivableTerrain):
    """Classe fille de DrivableTerrain : la route, meilleure traction, dérape rarement
    mais frotte fort en dérapage."""

    name = "road"
    traction = 1.0
    grip = 0.30
    drift_threshold = 1.15
    drift_grip = 0.45
    drift_friction = 0.985
    rolling_friction = 1.0


class Grass(DrivableTerrain):
    """Classe fille de DrivableTerrain : l'herbe, traction moyenne et ralentit la voiture."""

    name = "grass"
    traction = 0.8
    grip = 0.18
    drift_threshold = 0.7
    drift_grip = 0.5
    drift_friction = 0.99
    rolling_friction = 0.97


class Dirt(DrivableTerrain):
    """Classe fille de DrivableTerrain : la terre, traction moyenne, dérape facilement."""

    name = "dirt"
    traction = 0.7
    grip = 0.12
    drift_threshold = 0.6
    drift_grip = 0.5
    drift_friction = 0.993
    rolling_friction = 0.995


class Ice(DrivableTerrain):
    """Classe fille de DrivableTerrain : la glace, presque aucune adhérence, la voiture glisse."""

    name = "ice"
    traction = 0.35
    grip = 0.025
    drift_threshold = 0.3
    drift_grip = 0.6
    drift_friction = 0.999
    rolling_friction = 1.0


class Void(HoleTerrain):
    """Classe fille de HoleTerrain : le vide, hérite de tout et ne change que son nom."""

    name = "void"


# Un seul objet par type de terrain, partagé par toutes les cases des circuits
# (un terrain ne change jamais pendant la course)
TERRAINS: dict[str, Terrain] = {
    terrain.name: terrain for terrain in (Road(), Grass(), Dirt(), Ice(), Void())
}
