from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

class rule110(CellularAutomaton):

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=MooreNeighborhood(self.edge_rule))
        self.name = "rule110"
        self.stateC = 3
        self.statenames = {
            "0":"void",
            "1":"Quiescent",
            "2":"Non-quiescent",
        }

        self.colour_alias = {
            "1":[220,220,220,0],
            "2":[30,30,30,0]
        }


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state

        left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1))[0],
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1))[0])

        centre = last_cell_state[0]

        lcr = lambda l, c, r: l == left and c == centre and r == right


        if lcr(2,2,2):
            new_cell_state = [1,]
        elif lcr(2,2,1):
            new_cell_state = [1,]
        elif lcr(2,1,2):
            new_cell_state = [2,]
        elif lcr(2,1,1):
            new_cell_state = [2,]
        elif lcr(1,2,2):
            new_cell_state = [1,]
        elif lcr(1,2,1):
            new_cell_state = [2,]
        elif lcr(1,1,2):
            new_cell_state = [2,]
        elif lcr(1,1,1):
            new_cell_state = [1,]

        return new_cell_state
