from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

X = [7]
L = [0]
G = [1]
A = [2]
B = [3]
C = [4]
F = [8]


class FSSP(CellularAutomaton):

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=MooreNeighborhood(self.edge_rule))
        self.name = "FSSP"
        self.stateC = 9
        self.statenames = {
            "0":"Rest State",
            "1":"General",
            "2":"State A",
            "3":"State B",
            "4":"State C",
            "7":"Borders",
            "8":"Fire Signal"
        }


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        border = (len(neighbors_last_states) != 2)

        if border:
            new_cell_state = X
        # A SQUARE
        elif self.LCR(A,A,A,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(C,A,A,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(L,A,A,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(X,A,A,last_cell_state,neighbors_last_states):
            new_cell_state = F

        elif self.LCR(A,A,B,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,A,B,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(L,A,B,last_cell_state,neighbors_last_states):
            new_cell_state = L

        elif self.LCR(A,A,C,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(B,A,C,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(G,A,C,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(L,A,C,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(X,A,C,last_cell_state,neighbors_last_states):
            new_cell_state = G

        elif self.LCR(A,A,G,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,A,G,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(G,A,G,last_cell_state,neighbors_last_states):
            new_cell_state = C

        elif self.LCR(A,A,L,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(B,A,L,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(C,A,L,last_cell_state,neighbors_last_states):
            new_cell_state = A

        elif self.LCR(A,A,X,last_cell_state,neighbors_last_states):
            new_cell_state = F
        elif self.LCR(B,A,X,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(G,A,X,last_cell_state,neighbors_last_states):
            new_cell_state = C

        # B SQUARE

        elif self.LCR(A,B,A,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,B,A,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(C,B,A,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(G,B,A,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(L,B,A,last_cell_state,neighbors_last_states):
            new_cell_state = G

        elif self.LCR(A,B,B,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,B,B,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(L,B,B,last_cell_state,neighbors_last_states):
            new_cell_state = B

        elif self.LCR(A,B,C,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(B,B,C,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(G,B,C,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(L,B,C,last_cell_state,neighbors_last_states):
            new_cell_state = L

        elif self.LCR(B,B,G,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(C,B,G,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(G,B,G,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(L,B,G,last_cell_state,neighbors_last_states):
            new_cell_state = B

        elif self.LCR(A,B,L,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(B,B,L,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(C,B,L,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(G,B,L,last_cell_state,neighbors_last_states):
            new_cell_state = C

        elif self.LCR(C,B,X,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(G,B,X,last_cell_state,neighbors_last_states):
            new_cell_state = G

        # C SQUARE

        elif self.LCR(C,C,A,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(L,C,A,last_cell_state,neighbors_last_states):
            new_cell_state = A

        elif self.LCR(A,C,B,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(C,C,B,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(G,C,B,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(L,C,B,last_cell_state,neighbors_last_states):
            new_cell_state = G

        elif self.LCR(B,C,C,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(C,C,C,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(L,C,C,last_cell_state,neighbors_last_states):
            new_cell_state = C

        elif self.LCR(A,C,G,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,C,G,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(C,C,G,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(G,C,G,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(L,C,G,last_cell_state,neighbors_last_states):
            new_cell_state = G

        elif self.LCR(A,C,L,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,C,L,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(C,C,L,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(G,C,L,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(L,C,L,last_cell_state,neighbors_last_states):
            new_cell_state = C

        elif self.LCR(A,C,X,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,C,X,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(G,C,X,last_cell_state,neighbors_last_states):
            new_cell_state = B

        # G square

        elif self.LCR(L,G,A,last_cell_state,neighbors_last_states):
            new_cell_state = G

        elif self.LCR(A,G,B,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(B,G,B,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(C,G,B,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(G,G,B,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(L,G,B,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(X,G,B,last_cell_state,neighbors_last_states):
            new_cell_state = G

        elif self.LCR(A,G,C,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(B,G,C,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(C,G,C,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(G,G,C,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(L,G,C,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(X,G,C,last_cell_state,neighbors_last_states):
            new_cell_state = G

        elif self.LCR(B,G,G,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(C,G,G,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(G,G,G,last_cell_state,neighbors_last_states):
            new_cell_state = F
        elif self.LCR(X,G,G,last_cell_state,neighbors_last_states):
            new_cell_state = F

        elif self.LCR(A,G,L,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(B,G,L,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(C,G,L,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(G,G,L,last_cell_state,neighbors_last_states):
            new_cell_state = B
        elif self.LCR(X,G,L,last_cell_state,neighbors_last_states):
            new_cell_state = A

        elif self.LCR(B,G,X,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(C,G,X,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(G,G,X,last_cell_state,neighbors_last_states):
            new_cell_state = F

        # L SQUARE

        elif self.LCR(A,L,A,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(B,L,A,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(C,L,A,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(G,L,A,last_cell_state,neighbors_last_states):
            new_cell_state = L

        elif self.LCR(A,L,B,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(B,L,B,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(C,L,B,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(G,L,B,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(L,L,B,last_cell_state,neighbors_last_states):
            new_cell_state = L

        elif self.LCR(A,L,C,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(B,L,C,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(C,L,C,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(G,L,C,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(L,L,C,last_cell_state,neighbors_last_states):
            new_cell_state = L

        elif self.LCR(A,L,G,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(B,L,G,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(C,L,G,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(G,L,G,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(L,L,G,last_cell_state,neighbors_last_states):
            new_cell_state = L

        elif self.LCR(A,L,L,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(B,L,L,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(C,L,L,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(G,L,L,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(L,L,L,last_cell_state,neighbors_last_states):
            new_cell_state = L

        elif self.LCR(A,L,X,last_cell_state,neighbors_last_states):
            new_cell_state = C
        elif self.LCR(B,L,X,last_cell_state,neighbors_last_states):
            new_cell_state = L
        elif self.LCR(C,L,X,last_cell_state,neighbors_last_states):
            new_cell_state = G
        elif self.LCR(G,L,X,last_cell_state,neighbors_last_states):
            new_cell_state = A
        elif self.LCR(L,L,X,last_cell_state,neighbors_last_states):
            new_cell_state = L

        else:
            new_cell_state = [8]

        return new_cell_state

    def LCR(self,left,current,right,last_cell_state,neighbors_last_states):
        return (left == neighbors_last_states[0] and right == neighbors_last_states[1] and current == last_cell_state)
