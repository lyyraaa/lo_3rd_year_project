from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule
import random

X = [0]
BIT = [1]
BORDER = [2]
BORDER_ACT = [3]
CELL = [4]
CELL_ACT = [5]
MARK_1 = [6]
MARK_2 = [7]
MARK_4 = [8]
MARK_8 = [9]
MARK_16 = [10]
MARK_32 = [11]
DROPPER_1 = [12]
DROPPER_2 = [13]
DROPPER_4 = [14]
DROPPER_8 = [15]
DROPPER_16 = [16]
DROPPER_32 = [17]

class unaryconv(CellularAutomaton):
    """ A CA to convert binary representations to unary"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "unaryconv"
        self.stateC = 18
        self.statenames = {
            "1":"Bit",
            "2":"Border",
            "3":"Border Active",
            "4":"Cell",
            "5":"Cell Active",
            "6":"Mark 1",
            "7":"Mark 2",
            "8":"Mark 4",
            "9":"Mark 8",
            "10":"Mark 16",
            "11":"Mark 32",
            "12":"Dropper 1",
            "13":"Dropper 2",
            "14":"Dropper 4",
            "15":"Dropper 8",
            "16":"Dropper 16",
            "17":"Dropper 32"
        }

        self.colour_alias = {
            "1":[0,0,0,0],
            "2":[17,85,204,0],
            "3":[109,158,235,0],
            "4":[102,102,102,0],
            "5":[0,255,255,0],
            "6":[252,229,205,0],
            "7":[249,203,156,0],
            "8":[246,178,107,0],
            "9":[230,145,56,0],
            "10":[180,95,6,0],
            "11":[120,64,3,0],
            "12":[234,209,220,0],
            "13":[213,166,189,0],
            "14":[194,123,160,0],
            "15":[166,77,121,0],
            "16":[116,27,71,0],
            "17":[76,17,4,0]
        }

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state

        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))

        # Dropper generation
        if last_cell_state == BIT:
            if top == MARK_1:
                new_cell_state = DROPPER_1
            elif top == MARK_2:
                new_cell_state = DROPPER_2
            elif top == MARK_4:
                new_cell_state = DROPPER_4
            elif top == MARK_8:
                new_cell_state = DROPPER_8
            elif top == MARK_16:
                new_cell_state = DROPPER_16
            elif top == MARK_32:
                new_cell_state = DROPPER_32
            else:
                new_cell_state = X
            return new_cell_state

        # Dropper split rules
        if last_cell_state == DROPPER_2 and right == X:
            new_cell_state = DROPPER_1
        elif last_cell_state == X and left == DROPPER_2:
            new_cell_state = DROPPER_1

        elif last_cell_state == DROPPER_4 and right == X:
            new_cell_state = DROPPER_2
        elif last_cell_state == X and left == DROPPER_4:
            new_cell_state = DROPPER_2

        elif last_cell_state == DROPPER_8 and right == X:
            new_cell_state = DROPPER_4
        elif last_cell_state == X and left == DROPPER_8:
            new_cell_state = DROPPER_4

        elif last_cell_state == DROPPER_16 and right == X:
            new_cell_state = DROPPER_8
        elif last_cell_state == X and left == DROPPER_16:
            new_cell_state = DROPPER_8

        elif last_cell_state == DROPPER_32 and right == X:
            new_cell_state = DROPPER_16
        elif last_cell_state == X and left == DROPPER_32:
            new_cell_state = DROPPER_16

        # dropper move rules
        elif last_cell_state == DROPPER_1 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_1:
            new_cell_state = DROPPER_1

        elif last_cell_state == DROPPER_2 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_2:
            new_cell_state = DROPPER_2

        elif last_cell_state == DROPPER_4 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_4:
            new_cell_state = DROPPER_4

        elif last_cell_state == DROPPER_8 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_8:
            new_cell_state = DROPPER_8

        elif last_cell_state == DROPPER_16 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_16:
            new_cell_state = DROPPER_16

        elif last_cell_state == DROPPER_32 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_32:
            new_cell_state = DROPPER_32


        # Border rules
        elif last_cell_state == BORDER and left == DROPPER_1:
            new_cell_state = BORDER_ACT
        elif last_cell_state == BORDER and left == BORDER_ACT:
            new_cell_state = CELL
        elif last_cell_state == BORDER:
            new_cell_state = BORDER
        elif last_cell_state == BORDER_ACT:
            new_cell_state = BORDER

        # Cell rules
        elif last_cell_state == CELL and left == BORDER_ACT:
            new_cell_state = CELL_ACT
        elif last_cell_state == DROPPER_1 and right == BORDER:
            new_cell_state = X
        elif last_cell_state == X and left == BORDER_ACT:
            new_cell_state = CELL_ACT
        elif last_cell_state == CELL_ACT and right == CELL:
            new_cell_state = CELL
        elif last_cell_state == CELL and left == CELL_ACT:
            new_cell_state = CELL_ACT
        elif last_cell_state == CELL_ACT and right == X:
            new_cell_state = CELL
        elif last_cell_state == X and left == CELL_ACT:
            new_cell_state = CELL
        elif last_cell_state == CELL:
            new_cell_state = CELL


        return new_cell_state
