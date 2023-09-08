from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

# Cells can be named like so just before a CA class, to aid rule writing
ALIVE = [1]
DEAD = [0]

class ConwaysCA(CellularAutomaton):
    """ Cellular automaton with the evolution rules of conways game of life """

    def __init__(self,initcells):

        # Load initial config and set dimensions
        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        # Inherit CellularAutomaton methods, and define neighborhood
        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=MooreNeighborhood(self.edge_rule))

        self.name = "ConwaysCA"
        self.stateC = 2

        self.statenames = dict()

    # Defines how cells evolve over time
    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        alive_neighbours = self.__count_alive_neighbours(neighbors_last_states)
        if last_cell_state == DEAD and alive_neighbours == 3:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours < 2:
            new_cell_state = DEAD
        if last_cell_state == ALIVE and 1 < alive_neighbours < 4:
            new_cell_state = ALIVE
        if last_cell_state == ALIVE and alive_neighbours > 3:
            new_cell_state = DEAD
        return new_cell_state

    @staticmethod
    def __count_alive_neighbours(neighbours):
        alive_neighbors = []
        for n in neighbours:
            if n == ALIVE:
                alive_neighbors.append(1)
        return len(alive_neighbors)
