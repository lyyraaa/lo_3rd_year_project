from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

X = [0]
RED = [1]
WHITE = [8]
BLUE = [3]
R_BORDER = [6]
RW_BORDER = [5]
WB_BORDER = [4]
B_BORDER = [15]
B_BORDER_0 = [9]
B_BORDER_C = [18]
RW_BORDER_0 = [12]
RW_BORDER_C = [13]
RWWB_BORDER_CLASH = [14]
RW_ACCEPT_A = [7]
RW_ACCEPT_B = [11]
WB_BORDER_C = [10]
WB_BORDER_0 = [16]
WB_ACCEPT = [17]
RWB_ACCEPT = [2]
ACCEPT = [19]
FAIL = [20]

class frenchflag(CellularAutomaton):
    """ A CA to accept strings matching a^n b^n c^n"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "frenchflag"
        self.stateC = 21
        self.statenames = {
            "0":"Void",
            "1":"Red",
            "2":"R-W-B Accept",
            "3":"Blue",
            "4":"W-B Border",
            "5":"R-W Border",
            "6":"Red Border",
            "7":"R-W Accept A",
            "8":"White",
            "9":"B Border v=0",
            "10":"W-B Border v=c",
            "11":"R-W Accept B",
            "12":"R-W Border v=0",
            "13":"R-W Border v=c",
            "14":"RW-WB Clash",
            "15":"Blue Border",
            "16":"W-B Border v=0",
            "17":"W-B Accept",
            "18":"B Border v=c",
            "19":"Final Accept",
            "20":"Fail"
        }

        self.colour_alias = {
            "1":[160,160,255,0],
            "3":[255,160,180,0]
        }


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state

        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))

        # Fail propagation
        if last_cell_state == FAIL:
            new_cell_state = FAIL
        elif last_cell_state == RED and (left == BLUE or right == BLUE):
            new_cell_state = FAIL
        elif last_cell_state == BLUE and (left == RED or right == RED):
            new_cell_state = FAIL
        elif left == FAIL:
            new_cell_state = FAIL
        elif last_cell_state == B_BORDER_0 and right == WB_BORDER_C:
            new_cell_state = FAIL
        elif last_cell_state == B_BORDER_0 and left == RW_ACCEPT_B:
            new_cell_state = FAIL
        elif last_cell_state == B_BORDER_0 and left == RW_BORDER_C:
            new_cell_state = FAIL
        elif last_cell_state == B_BORDER_0 and right == B_BORDER_C:
            new_cell_state = FAIL
        elif last_cell_state == B_BORDER_0 and left == RW_ACCEPT_A:
            new_cell_state = FAIL
        elif last_cell_state == B_BORDER_0 and left == R_BORDER:
            new_cell_state = FAIL
        elif last_cell_state == B_BORDER_0 and right == WB_BORDER_C:
            new_cell_state = FAIL
        elif last_cell_state == WHITE and (left == X or right == X):
            new_cell_state = FAIL
        elif last_cell_state == RED and right == X:
            new_cell_state = FAIL
        elif last_cell_state == BLUE and left == X:
            new_cell_state = FAIL


        # Success propagation
        elif last_cell_state == B_BORDER_0 and left == RWB_ACCEPT:
            new_cell_state = ACCEPT
        elif last_cell_state == ACCEPT:
            new_cell_state = ACCEPT
        elif left == RWB_ACCEPT:
            new_cell_state = RWB_ACCEPT


        # Secondary border production
        elif last_cell_state == RW_BORDER:
            new_cell_state = RW_BORDER_0
        elif left == RW_BORDER:
            new_cell_state = RW_BORDER_C
        elif last_cell_state == WB_BORDER:
            new_cell_state = WB_BORDER_0
        elif right == WB_BORDER:
            new_cell_state = WB_BORDER_C
        elif right == B_BORDER:
            new_cell_state = B_BORDER_C
        elif last_cell_state == B_BORDER:
            new_cell_state = B_BORDER_0

        elif last_cell_state == B_BORDER_0:
            new_cell_state = B_BORDER_0

        # RWB accept
        elif last_cell_state == WB_ACCEPT and left == RW_ACCEPT_B:
            new_cell_state = RWB_ACCEPT


        # RW accept
        elif last_cell_state == RW_BORDER_0 and left == R_BORDER:
            new_cell_state = RW_ACCEPT_A
        elif last_cell_state == WB_BORDER_C and left == RW_ACCEPT_A:
            new_cell_state = RW_ACCEPT_B
        elif left == RW_ACCEPT_B:
            new_cell_state = RW_ACCEPT_B
        elif last_cell_state == RW_ACCEPT_A or last_cell_state == RW_ACCEPT_B:
            new_cell_state = X

        # WB accept
        elif last_cell_state == WB_BORDER_0 and left == RW_BORDER_C and right == B_BORDER_C:
            new_cell_state = WB_ACCEPT
        elif last_cell_state == WB_ACCEPT:
            new_cell_state = WB_ACCEPT

        # Clash signal
        elif left == RW_BORDER_C and right == WB_BORDER_C:
            new_cell_state = RWWB_BORDER_CLASH
        elif left == RWWB_BORDER_CLASH:
            new_cell_state = RW_BORDER_C
        elif right == RWWB_BORDER_CLASH:
            new_cell_state = WB_BORDER_C

        # elemental border production
        elif last_cell_state == RED and left == X:
            new_cell_state = R_BORDER
        elif last_cell_state == RED and right == WHITE:
            new_cell_state = RW_BORDER
        elif last_cell_state == WHITE and right == BLUE:
            new_cell_state = WB_BORDER
        elif last_cell_state == BLUE and right == X:
            new_cell_state = B_BORDER

        # Border signal movement
        elif left == R_BORDER:
            new_cell_state = R_BORDER
        elif left == RW_BORDER_C:
            new_cell_state = RW_BORDER_C
        elif right == WB_BORDER_C:
            new_cell_state = WB_BORDER_C
        elif right == B_BORDER_C:
            new_cell_state = B_BORDER_C
        elif last_cell_state == RW_BORDER_0:
            new_cell_state = RW_BORDER_0
        elif last_cell_state == WB_BORDER_0:
            new_cell_state = WB_BORDER_0

        else:
            new_cell_state = X

        #print(new_cell_state)
        return new_cell_state
