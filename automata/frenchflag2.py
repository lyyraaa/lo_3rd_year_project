from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

X = [0]
RED = [1]
WHITE = [2]
BLUE = [3]
REDWHITE = [4]
BORDER = [5]
TRACKER_OUT = [6]
TRACKER_IN = [7]
SUCCESS = [8]
FAIL = [9]
FAIL_V = [10]

class frenchflag2(CellularAutomaton):
    """ A CA to accept strings matching a^n b^n c^n"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "frenchflag2"
        self.stateC = 11
        self.statenames = {
            "0":"Void",
            "1":"Red",
            "2":"White",
            "3":"Blue",
            "4":"Red/White",
            "5":"Border",
            "6":"Tracker in",
            "7":"Tracker out",
            "8":"Pass",
            "9":"Fail",
            "10":"Fail moving"
        }

        self.colour_alias = {
            "2":[255,255,255,0],
            "5":[60,60,60,0],
            "4":[247,127,190,0],
            "5":[60,60,60,0],
            "6":[255,174,66,0],
            "7":[255,103,0,0],
            "8":[0,255,0,0],
            "9":[255,0,0,0],
            "10":[90,90,90,0],
        }


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = X

        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))

        # success/fail signals
        if last_cell_state == BORDER and top == TRACKER_IN and right == X:
            new_cell_state = SUCCESS
        elif last_cell_state == BORDER and top == TRACKER_IN and right != X:
            new_cell_state = FAIL
        elif last_cell_state == SUCCESS:
            new_cell_state = SUCCESS
        elif last_cell_state == FAIL:
            new_cell_state = FAIL
        elif last_cell_state == BLUE and (right == RED or right == WHITE or right == REDWHITE):
            new_cell_state = FAIL_V
        elif right == FAIL_V and last_cell_state != BORDER:
            new_cell_state = FAIL_V
        elif last_cell_state == FAIL_V and left == BORDER:
            new_cell_state = FAIL_V

        # tracker movement
        elif left == TRACKER_OUT and bot != X:
            new_cell_state = TRACKER_OUT
        elif left == TRACKER_OUT and bot == X:
            new_cell_state = TRACKER_IN
        elif right == TRACKER_IN and bot != SUCCESS and bot != FAIL:
            new_cell_state = TRACKER_IN

        # blue-redwhite annihilation
        elif last_cell_state == REDWHITE and right == BLUE:
            new_cell_state = X
        elif last_cell_state == BLUE and left == REDWHITE:
            new_cell_state = X

        # Redwhite creation and movement
        elif last_cell_state == RED and right == WHITE and (left == RED or left == BORDER or left == REDWHITE):
            new_cell_state = REDWHITE
        elif last_cell_state == RED and right == REDWHITE:
            new_cell_state = REDWHITE
        elif last_cell_state == REDWHITE and left == RED:
            new_cell_state = RED
        elif last_cell_state == WHITE and left == RED:
            new_cell_state = X

        # free movement rules
        elif last_cell_state == X and right == BLUE:
            new_cell_state = BLUE
        elif last_cell_state == X and right == WHITE:
            new_cell_state = WHITE

        # persistence rules
        elif last_cell_state == RED and (left == BORDER or left == RED or left == REDWHITE or left == BLUE):
            new_cell_state = RED
        elif last_cell_state == WHITE and (left == WHITE or left == REDWHITE or left == BORDER or left == BLUE):
            new_cell_state = WHITE
        elif last_cell_state == BLUE and (left == BLUE or left == WHITE or left == BORDER or left == RED):
            new_cell_state = BLUE
        elif last_cell_state == REDWHITE and (left == BORDER or left == REDWHITE or left == BLUE or left == WHITE):
            new_cell_state = REDWHITE
        elif last_cell_state == BORDER:
            new_cell_state = BORDER
        else:
            new_cell_state = X

        return new_cell_state
