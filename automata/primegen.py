from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule
import random

X = [0]

# Unary conv stuff


class primegen(CellularAutomaton):
    """ A CA to generate a list of primes"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "primegen"
        self.stateC = 17
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
        #    "1":[0,0,0,255],
        #    "2":[17,85,204,255],
        #    "3":[109,158,235,255],
        #    "4":[102,102,102,255],
        #    "5":[0,255,255,255],
        #    "6":[252,229,205,255],
        #    "7":[249,203,156,255],
        #    "8":[246,178,107,255],
        #    "9":[230,145,56,255],
        #    "10":[180,95,6,255],
        #    "11":[120,64,3,255],
        #    "12":[234,209,220,255],
        #    "13":[213,166,189,255],
        #    "14":[194,123,160,255],
        #    "15":[166,77,121,255],
        #    "16":[116,27,71,255],
        #    "17":[76,17,4,2558]
        }

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state


        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))

        if self.LCR(13,3,13,last_cell_state,neighbors_last_states):
            new_cell_state = [12]
        elif self.LCR(6,-1,4,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(10,-1,3,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(10,-1,11,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(13,7,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [8]
        elif self.LCR(13,8,7,last_cell_state,neighbors_last_states):
            new_cell_state = [13]
        elif self.LCR(15,8,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [1]
        elif self.LCR(8,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [7]
        elif self.LCR(15,1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [2]
        elif self.LCR(-1,1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [1]
        elif self.LCR(1,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [8]
        elif self.LCR(2,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]
        elif self.LCR(4,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]
        elif self.LCR(5,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]
        elif self.LCR(15,2,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [4]
        elif self.LCR(-1,4,8,last_cell_state,neighbors_last_states):
            new_cell_state = [4]
        elif self.LCR(-1,4,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [5]
        elif self.LCR(-1,5,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [3]
        elif self.LCR(15,3,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [12]
        elif self.LCR(-1,2,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [2]
        elif self.LCR(-1,3,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [3]
        elif self.LCR(-1,8,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [8]
        elif self.LCR(-1,11,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [10]
        elif self.LCR(-1,12,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [11]
        elif self.LCR(11,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]

        elif self.LCR(13,-1,1,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(13,-1,2,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(13,-1,3,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(13,-1,5,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(13,-1,6,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(13,-1,10,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(13,-1,11,last_cell_state,neighbors_last_states):
            new_cell_state = [15]

        elif self.LCR(13,0,8,last_cell_state,neighbors_last_states):
            new_cell_state = [15]

        elif self.LCR(14,-1,6,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(14,-1,10,last_cell_state,neighbors_last_states):
            new_cell_state = [15]

        elif self.LCR(10,0,6,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(10,0,10,last_cell_state,neighbors_last_states):
            new_cell_state = [15]

        elif self.LCR(10,9,6,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(10,9,10,last_cell_state,neighbors_last_states):
            new_cell_state = [15]

        elif self.LCR(10,13,6,last_cell_state,neighbors_last_states):
            new_cell_state = [15]
        elif self.LCR(10,13,10,last_cell_state,neighbors_last_states):
            new_cell_state = [15]

        elif self.LCR(6,-1,6,last_cell_state,neighbors_last_states):
            new_cell_state = [0]
        elif self.LCR(-1,-1,10,last_cell_state,neighbors_last_states):
            new_cell_state = [9]

        elif self.LCR(6,15,9,last_cell_state,neighbors_last_states):
            new_cell_state = [14]
        elif self.LCR(10,15,9,last_cell_state,neighbors_last_states):
            new_cell_state = [14]

        elif self.LCR(-1,6,9,last_cell_state,neighbors_last_states):
            new_cell_state = [10]
        elif self.LCR(-1,6,14,last_cell_state,neighbors_last_states):
            new_cell_state = [10]
        elif self.LCR(-1,6,15,last_cell_state,neighbors_last_states):
            new_cell_state = [10]

        elif self.LCR(-1,10,9,last_cell_state,neighbors_last_states):
            new_cell_state = [10]
        elif self.LCR(-1,10,14,last_cell_state,neighbors_last_states):
            new_cell_state = [10]
        elif self.LCR(-1,10,15,last_cell_state,neighbors_last_states):
            new_cell_state = [10]

        elif self.LCR(-1,6,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [6]
        elif self.LCR(-1,10,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [6]

        elif self.LCR(6,15,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]
        elif self.LCR(10,15,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]

        elif self.LCR(13,-1,9,last_cell_state,neighbors_last_states):
            new_cell_state = [14]
        elif self.LCR(13,-1,15,last_cell_state,neighbors_last_states):
            new_cell_state = [14]

        elif self.LCR(14,-1,9,last_cell_state,neighbors_last_states):
            new_cell_state = [14]
        elif self.LCR(14,-1,15,last_cell_state,neighbors_last_states):
            new_cell_state = [14]

        elif self.LCR(13,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]
        elif self.LCR(14,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [13]

        elif self.LCR(-1,-1,15,last_cell_state,neighbors_last_states):
            new_cell_state = [15]

        elif self.LCR(-1,-1,9,last_cell_state,neighbors_last_states):
            new_cell_state = [9]
        elif self.LCR(-1,-1,14,last_cell_state,neighbors_last_states):
            new_cell_state = [9]

        elif self.LCR(-1,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [0]


        return new_cell_state

    def LCR(self,left,current,right,last_cell_state,neighbors_last_states):
        con_left = True if left == -1 else (left == neighbors_last_states[0][0])
        con_right = True if right == -1 else (right == neighbors_last_states[3][0])
        con_centre = True if current == -1 else (current == last_cell_state[0])
        return (con_left and con_centre and con_right)
