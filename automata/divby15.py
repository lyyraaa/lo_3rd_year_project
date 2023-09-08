from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

X = [0]
STOP = [1]
PASS = [2]
EVEN = [3]
DIV3_0 = [4]
DIV3_1 = [9]
DIV3_2 = [10]
DIV3PASS = [5] # div 2
ODD = [6]
BIT = [7]
DIV5PASS = [8]
DIV5_0 = [11]
DIV5_1 = [12]
DIV5_2 = [13]
DIV5_3 = [14]
DIV5_4 = [15]

class divby15(CellularAutomaton):
    """ A CA to calculate divisibility by 15 on a binary string"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "divby15"
        self.stateC = 16
        self.statenames = {
            "0":"void",
            "1":"Fail marker",
            "2":"Pass marker",
            "3":"Even marker",
            "4":"Div3+0",
            "5":"Div3 pass",
            "6":"Odd markers",
            "7":"Active Bits",
            "8":"Div5 pass",
            "9":"Div3+1",
            "10":"Div3+2",
            "11":"Div5+0",
            "12":"Div5+1",
            "13":"Div5+2",
            "14":"Div5+3",
            "15":"Div5+4"

        }


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state

        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))


        if last_cell_state == PASS:
            new_cell_state = PASS
        elif last_cell_state == STOP and left == DIV3_0:
            new_cell_state = DIV3PASS
        elif last_cell_state == STOP and left == DIV5_0:
            new_cell_state = DIV5PASS

        elif last_cell_state == DIV3PASS and bot == DIV5PASS:
            new_cell_state = X
        elif last_cell_state == DIV5PASS and top == DIV3PASS:
            new_cell_state = PASS
        elif last_cell_state == DIV5PASS or last_cell_state == DIV3PASS:
            new_cell_state = STOP


        elif last_cell_state == STOP:
            new_cell_state = STOP

        # DIV3 Eater
        elif last_cell_state == X and left == DIV3_0:
            new_cell_state = DIV3_0
        elif last_cell_state == X and left == DIV3_1:
            new_cell_state = DIV3_1
        elif last_cell_state == X and left == DIV3_2:
            new_cell_state = DIV3_2

        elif last_cell_state == ODD and left == DIV3_0:
            new_cell_state = DIV3_1
        elif last_cell_state == ODD and left == DIV3_1:
            new_cell_state = DIV3_2
        elif last_cell_state == ODD and left == DIV3_2:
            new_cell_state = DIV3_0

        elif last_cell_state == EVEN and left == DIV3_0:
            new_cell_state = DIV3_2
        elif last_cell_state == EVEN and left == DIV3_1:
            new_cell_state = DIV3_0
        elif last_cell_state == EVEN and left == DIV3_2:
            new_cell_state = DIV3_1

        # DIV5 Eater
        elif last_cell_state == X and left == DIV5_0:
            new_cell_state = DIV5_0
        elif last_cell_state == X and left == DIV5_1:
            new_cell_state = DIV5_2
        elif last_cell_state == X and left == DIV5_2:
            new_cell_state = DIV5_4
        elif last_cell_state == X and left == DIV5_3:
            new_cell_state = DIV5_1
        elif last_cell_state == X and left == DIV5_4:
            new_cell_state = DIV5_3

        elif last_cell_state == BIT and left == DIV5_0:
            new_cell_state = DIV5_1
        elif last_cell_state == BIT and left == DIV5_1:
            new_cell_state = DIV5_3
        elif last_cell_state == BIT and left == DIV5_2:
            new_cell_state = DIV5_0
        elif last_cell_state == BIT and left == DIV5_3:
            new_cell_state = DIV5_2
        elif last_cell_state == BIT and left == DIV5_4:
            new_cell_state = DIV5_4

        elif last_cell_state == BIT:
            new_cell_state = BIT
        elif last_cell_state == ODD and bot == BIT:
            new_cell_state = ODD
        elif last_cell_state == EVEN and bot == BIT:
            new_cell_state = EVEN

        else:
            new_cell_state = X

        return new_cell_state
