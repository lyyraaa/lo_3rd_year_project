from cellular_automaton import CellularAutomaton as CA, MooreNeighborhood,VonNeumannNeighborhood, CAWindow, EdgeRule

################################################################################
### Storage file for different cellular automata ###############################
################################################################################

# Each automata has to have a:

    # name, displayed on the UI
    # a count of the number of states it uses (this is actually the highest numbered state it uses)
    # an evolve rule, which says how to evolve between states
    # state name dictionary
        # this is optional to use, but allows naming of the states in the UI
        # for some reason it will crash if the names are too long. RW-WB Border Clash was too long

# This class is used by all my CA to load an inintial configuration from a file
# Cell files simply have their dimensions at the top, and then a matrix of cells
# Filepath can be None, for use in editor to not bother reading files when only details are needed.
class CellLoader():
    def __init__(self,filepath=None):
        self.cellarr = []

        # Reading lines and dimensions
        if isinstance(filepath,str):
            f = open(filepath, "r")
            lines = f.readlines()
            self.rowC,self.colC = int(lines[0].split()[0]),int(lines[0].split()[1])

            # Reading cell data to cell array
            for row in range(self.rowC):
                rowline = lines[row+1].split()
                rowarr = []
                for col in range(self.colC):
                    rowarr.append([int(rowline[col])])
                self.cellarr.append(rowarr)
        elif isinstance(filepath, list):
            self.rowC = len(filepath)
            self.colC = len(filepath[0])
            self.cellarr = filepath
        else:
            self.rowC = self.colC = 0

    def get_rowC(self):
        return self.rowC

    def get_colC(self):
        return self.colC

    def get_cells(self):
        return self.cellarr

class CellularAutomaton(CA):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.colour_alias = dict()
        self.quiesent_state = 0

    def init_cell_state(self, coord):  # pylint: disable=no-self-use
        return self.initcells[coord[0]][coord[1]]

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state
        return new_cell_state

    def getStatename(self,stateid):
        if self.statenames:
            name = self.statenames.get(str(stateid))
            if name: return name
            else: return "None"

    def getDimensions(self):
        return (self.rowC,self.colC)

    def get_colour_alias(self):
        if self.colour_alias:
            return self.colour_alias
