from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

RED = [1]
BLUE = [3]
GREEN = [2]
CYAN = [4]
YELLOW = [5]
MAGENTA = [6]
BLACK = [7]
WHITE = [8]


class RedBlue(CellularAutomaton):
    """ A CA accepting languages in the form red^n blue^n """

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=MooreNeighborhood(self.edge_rule))
        self.name = "RedBlue"
        self.statenames = dict()
        self.stateC = 9


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        border = (len(neighbors_last_states) != 2)

        if border and last_cell_state == RED:
            new_cell_state = YELLOW
        elif neighbors_last_states[0] == BLACK:
            new_cell_state = BLACK
        elif neighbors_last_states[0] == WHITE:
            new_cell_state = WHITE
        elif border and last_cell_state == BLUE:
            new_cell_state = CYAN
        elif not border and neighbors_last_states[1] == BLUE and last_cell_state == RED:
            new_cell_state = MAGENTA
        elif neighbors_last_states[0] == GREEN and last_cell_state == CYAN:
            new_cell_state = WHITE
        elif neighbors_last_states[0] == GREEN and last_cell_state != CYAN:
            new_cell_state = BLACK
        elif not border and neighbors_last_states[1] == CYAN and last_cell_state == MAGENTA:
            new_cell_state = BLACK
        elif neighbors_last_states[0] == YELLOW and last_cell_state == MAGENTA:
            new_cell_state = GREEN
        elif not border and neighbors_last_states[0] == YELLOW:
            new_cell_state = YELLOW
        elif not border and neighbors_last_states[1] == CYAN:
            new_cell_state = CYAN
        elif last_cell_state == MAGENTA:
            new_cell_state = MAGENTA
        else:
            new_cell_state = [0]
        return new_cell_state
