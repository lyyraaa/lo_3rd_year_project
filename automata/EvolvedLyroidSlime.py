from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule
import random


DEAD = [0]
SLIME_A = [1]
SLIME_B = [2]

class EvolvedLyroidSlime(CellularAutomaton):
    """ A very basic slime/bacteria type CA that grows into its surroundings and randomly competes with a second organism """
    """ But this time on a VonNeumannNeighborhood """

    def __init__(self,initcells):
        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()
        self.name = "EvolvedLyroidSlime"
        self.stateC = 3
        self.statenames = {
            "0":"void",
            "1":"Slime A",
            "2":"Slime B"
        }
        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
            neighborhood=VonNeumannNeighborhood(self.edge_rule))

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        dom_neighbour = self.__get_dominant_neighbour(last_cell_state,neighbors_last_states)
        if dom_neighbour == 1:
            new_cell_state = SLIME_A
        if dom_neighbour == 2:
            new_cell_state = SLIME_B
        return new_cell_state

    @staticmethod
    def __get_dominant_neighbour(last_cell_state,neighbours):
        A_neighbors = []
        B_neighbors = []
        for n in neighbours:
            if n == SLIME_A:
                A_neighbors.append(1)
            if n == SLIME_B:
                B_neighbors.append(1)
        if len(A_neighbors) == 0 and len(B_neighbors) == 0:
            return 0
        elif len(A_neighbors) > len(B_neighbors):
            return 1
        elif len(B_neighbors) > len(A_neighbors):
            return 2
        elif last_cell_state == SLIME_A:
            return 1
        elif last_cell_state == SLIME_B:
            return 2
