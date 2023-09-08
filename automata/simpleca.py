from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

VOID = [0]
SIGNAL_LEFT = [1]
SIGNAL_RIGHT = [2]
STOP = [3]

SIGNAL_LEFT_0 = [4]
SIGNAL_LEFT_1 = [5]
SIGNAL_LEFT_2 = [6]

BLINKER_0 = [7]
BLINKER_1 = [8]

CON_PERSIST = [9]

NEEDS_2 = [10]

NEEDS_3_plus = [11]

class simpleCA(CellularAutomaton):
    """ A simple CA to test information flow"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "simpleca"
        self.stateC = 12
        self.statenames = {
            "0":"void",
            "1":"VC left",
            "2":"VC top",
            "3":"V0 Signal",
            "4":"SignalLeft 0",
            "5":"SignalLeft 1",
            "6":"SignalLeft 2",
            "7":"Blinker 0",
            "8":"Blinker 1",
            "9":"Con Persist",
            "10":"Needs least 2",
            "11":"Needs least 3"
        }

        self.colour_alias = {
            "1":[255,30,255,0],
            "2":[0,255,255,0],
            "3":[100,100,100,0],
            "4":[250,100,0,0],
            "5":[200,100,0,0],
            "6":[150,100,0,0],
            "7":[255,90,160,0],
            "8":[160,90,255,0],
            "9":[90,30,140,0]
        }


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state


        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))

        #print(neighbors_last_states)
        #print(left,top,bot,right)
        # order in neumann  = left, top, bot, right
        if last_cell_state == NEEDS_2 and sum([cel == STOP for cel in [top,bot,left,right]]) >= 2:
            new_cell_state = NEEDS_2
        elif last_cell_state == NEEDS_3_plus and sum([cel == STOP for cel in [top,bot,left,right]]) >= 3:
            new_cell_state = NEEDS_3_plus

        elif last_cell_state == VOID and top == SIGNAL_RIGHT:
            new_cell_state = SIGNAL_RIGHT
        elif last_cell_state == VOID and left == SIGNAL_LEFT:
            new_cell_state = SIGNAL_LEFT
        elif last_cell_state == SIGNAL_LEFT_0:
            new_cell_state = SIGNAL_LEFT_1
        elif last_cell_state == SIGNAL_LEFT_1:
            new_cell_state = SIGNAL_LEFT_2
        elif last_cell_state == VOID and left == SIGNAL_LEFT_2:
            new_cell_state = SIGNAL_LEFT_0
        elif last_cell_state == STOP:
            new_cell_state = STOP
        elif last_cell_state == BLINKER_0:
            new_cell_state = BLINKER_1
        elif last_cell_state == BLINKER_1:
            new_cell_state = BLINKER_0
        elif last_cell_state == CON_PERSIST and (left == SIGNAL_LEFT or top == SIGNAL_RIGHT):
            new_cell_state = CON_PERSIST
        else:
            new_cell_state = VOID

        return new_cell_state
