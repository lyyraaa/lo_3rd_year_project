from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

X = [0]
STOP = [1]
PASS = [2]
EVEN = [3]
EATER_0 = [4]
EATER_1 = [9]
EATER_2 = [10]
YELLOW = [5] # div 2
ODD = [6]
BIT = [7]

class divby6(CellularAutomaton):
    """ A CA to calculate divisibility by 6 on a binary string"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "divby6"
        self.stateC = 11
        self.statenames = {
            "0":"void",
            "1":"Fail marker",
            "2":"Pass marker",
            "3":"Even marker",
            "4":"Eater+0",
            "5":"Div2 checker",
            "6":"Odd markers",
            "7":"Active Bits",
            "8":"None",
            "9":"Eater+1",
            "10":"Eater+2",

        }


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state

        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))


        if last_cell_state == EATER_0 and bot == PASS:
            new_cell_state = PASS
        elif last_cell_state == STOP and left == PASS:
            new_cell_state = PASS

        elif last_cell_state == X and left == EATER_0:
            new_cell_state = EATER_0
        elif last_cell_state == X and left == EATER_1:
            new_cell_state = EATER_1
        elif last_cell_state == X and left == EATER_2:
            new_cell_state = EATER_2

        elif last_cell_state == ODD and left == EATER_0:
            new_cell_state = EATER_1
        elif last_cell_state == ODD and left == EATER_1:
            new_cell_state = EATER_2
        elif last_cell_state == ODD and left == EATER_2:
            new_cell_state = EATER_0

        elif last_cell_state == EVEN and left == EATER_0:
            new_cell_state = EATER_2
        elif last_cell_state == EVEN and left == EATER_1:
            new_cell_state = EATER_0
        elif last_cell_state == EVEN and left == EATER_2:
            new_cell_state = EATER_1

        elif last_cell_state == YELLOW and top == X:
            new_cell_state = PASS
        elif last_cell_state == STOP:
            new_cell_state = STOP
        elif last_cell_state == PASS:
            new_cell_state = PASS
        elif last_cell_state == ODD:
            new_cell_state = ODD
        elif last_cell_state == EVEN:
            new_cell_state = EVEN
        elif last_cell_state == BIT and top == ODD:
            new_cell_state = ODD
        elif last_cell_state == BIT and top == EVEN:
            new_cell_state = EVEN
        else:
            new_cell_state = X

        return new_cell_state
