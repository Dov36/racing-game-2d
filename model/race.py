"""Règles de la course : points de passage, tours, chronomètre, vainqueur."""
from constants import FPS


class RaceManager:
    """Suit l'avancement des joueurs : portes, tours, chrono et vainqueur.

    Un tour compte seulement si le joueur est passé par toutes les portes
    avant de retraverser la ligne d'arrivée. Une porte est un groupe de cases
    C voisines : la piste fait deux cases de large, donc deux C côte à côte
    forment une seule porte. Le premier qui finit ses tours gagne.
    """

    def __init__(self, circuit, total_laps: int, player_count: int = 2):
        self.circuit = circuit
        self.total_laps = total_laps
        self.player_count = player_count
        self.gates = self._find_gates(circuit)  # liste d'ensembles de (col, row)
        self.gate_of = {cell: index
                        for index, gate in enumerate(self.gates)
                        for cell in gate}
        self.passed = [set() for _ in range(player_count)]  # portes déjà franchies
        self.laps = [0] * player_count  # tours terminés
        self.on_finish_line = [False] * player_count
        self.winner: int | None = None  # indice du gagnant, None tant que ça dure
        self.frames = 0  # frames écoulées depuis le départ

    @staticmethod
    def _find_gates(circuit) -> list[set]:
        """Regroupe les cases 'C' voisines en portes.

        Parcours de graphe avec une pile : on part d'une case C non visitée
        et on empile ses voisines C (haut, bas, gauche, droite) jusqu'à
        épuisement ; l'ensemble visité forme une porte. Méthode statique :
        elle n'a besoin d'aucun état du gestionnaire, seulement du circuit.
        """
        cells = {(t.col, t.row) for t in circuit.find_block("C")}
        gates, seen = [], set()
        for start in sorted(cells, key=lambda cell: (cell[1], cell[0])):
            if start in seen:
                continue
            gate, stack = set(), [start]
            while stack:
                cell = stack.pop()
                if cell in seen:
                    continue
                seen.add(cell)
                gate.add(cell)
                col, row = cell
                for neighbour in ((col + 1, row), (col - 1, row),
                                  (col, row + 1), (col, row - 1)):
                    if neighbour in cells and neighbour not in seen:
                        stack.append(neighbour)
            gates.append(gate)
        return gates

    def tick(self) -> None:
        """Avance le chronomètre d'une frame (arrêté une fois la course finie)."""
        if not self.is_finished():
            self.frames += 1

    def time_seconds(self) -> float:
        """Temps de course écoulé, en secondes."""
        return self.frames / FPS

    def gates_passed(self, index: int) -> int:
        """Nombre de portes franchies par le joueur pendant son tour actuel."""
        return len(self.passed[index])

    def update_player(self, index: int, tile) -> None:
        """Met à jour l'avancement d'un joueur d'après la case sous sa voiture.

        Appelée à chaque frame par le modèle du jeu. tile vaut None si la
        voiture est hors de la carte : il n'y a alors rien à faire.
        """
        if tile is None or self.is_finished():
            return
        if tile.block == "C":
            self.passed[index].add(self.gate_of[(tile.col, tile.row)])
        if tile.block == "L":
            # On ne compte qu'à l'entrée sur la ligne, sinon on aurait un
            # tour à chaque frame passée dessus.
            if not self.on_finish_line[index]:
                self.on_finish_line[index] = True
                self._try_finish_lap(index)
        else:
            self.on_finish_line[index] = False

    def _try_finish_lap(self, index: int) -> None:
        """Valide un tour si toutes les portes ont été franchies."""
        if not self.gates or len(self.passed[index]) < len(self.gates):
            return
        self.laps[index] += 1
        self.passed[index].clear()
        if self.laps[index] >= self.total_laps:
            self.winner = index

    def is_finished(self) -> bool:
        """Vrai dès qu'un joueur a terminé tous ses tours."""
        return self.winner is not None
