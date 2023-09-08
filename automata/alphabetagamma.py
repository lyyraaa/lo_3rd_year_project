from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

VOID = [0]
A = [1]
B = [2]
C = [3]
D = [4]
X = [5]

class alphabetagamma(CellularAutomaton):
    """ A simple CA to test the anything but purple problem"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "aby"
        self.stateC = 6
        self.statenames = {
            "0":"void",
            "1":"Alpha",
            "2":"Beta",
            "3":"Gamma"
        }

        self.colour_alias = {
            "1":[220,0,0,0],
            "3":[100,255,80,0],
            "2":[100,150,70,0],
            "4":[100,150,70,0]
        }

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = VOID


        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))



        if last_cell_state == [1] and (left == [2] or right == [4]):
            new_cell_state = [3]
        elif last_cell_state == [1]:
            new_cell_state = [1]
        elif last_cell_state == [3]:
            new_cell_state = [3]
        elif left == [2]:
            new_cell_state = [2]
        elif right == [4]:
            new_cell_state = [4]


        return new_cell_state










"""


from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

VOID = [0]
A = [1]
B = [2]
C = [3]
D = [4]
X = [5]

class alphabetagamma(CellularAutomaton):
    #A simple CA to test the anything but purple problem

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "aby"
        self.stateC = 6
        self.statenames = {
            "0":"void",
            "1":"Alpha",
            "2":"Beta",
            "3":"Gamma"
        }

        self.colour_alias = {
            "1":[220,0,0,0],
            "5":[100,255,0,0],
            "2":[100,255,0,0]
        }

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = VOID


        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))


        if last_cell_state == A and (left == X or right == X):
            new_cell_state = B
        if last_cell_state == B:
            new_cell_state = B


        return new_cell_state"""
