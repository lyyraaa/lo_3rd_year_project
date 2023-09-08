from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule
import random

X = [0]
BIT = [1]
BORDER = [2]
BORDER_ACT = [3]
CELL = [4]
CELL_ACT = [5]
MARK_1 = [6]
MARK_2 = [7]
MARK_4 = [8]
MARK_8 = [9]
MARK_16 = [10]
MARK_32 = [11]
DROPPER_1 = [12]
DROPPER_2 = [13]
DROPPER_4 = [14]
DROPPER_8 = [15]
DROPPER_16 = [16]
DROPPER_32 = [17]

# Transition stuff

MID = [18]
CAP = [19]
INITMIDPOINT = [20]
SIGNAL_0 = [21]
SIGNAL_1 = [22]
SIGNAL_2 = [23]
SIGNAL_V1 = [24]
SIGNAL_VMINUS = [25]

# Prime setup
SETUP_3 = [26]
SETUP_2 = [27]
SETUP_1 = [28]
SETUP_0 = [29]

COUNTDOWN_0_3 = [30]
COUNTDOWN_0_2 = [31]
COUNTDOWN_0_1 = [32]

COUNTDOWN_1_2 = [33]
COUNTDOWN_1_1 = [34]

COUNTDOWN_2_1 = [35]

V1_DELAY = [51]
PRIME = [52]
NOT_PRIME = [53]

class primecheck(CellularAutomaton):
    """ A CA to check primality of binary numbers by conversion to unary"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "primecheck"
        self.stateC = 54
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
            "17":"Dropper 32",
            "18":"Midpoint",
            "19":"Capstone",
            "20":"Midpoint init.",
            "21":"Signal 1/3 0",
            "22":"Signal 1/3 1",
            "23":"Signal 1/3 2",
            "24":"Signal V",
            "25":"Signal V-1",
            "26":"Setup for 3",
            "27":"Setup for 2",
            "28":"Setup for 1",
            "29":"Setup for 0",
            "30":"Countdown0, 3",
            "31":"Countdown0, 2",
            "32":"Countdown0, 1",
            "33":"Countdown1, 2",
            "34":"Countdown1, 1",
            "35":"Countdown2, 1",
            "41":"Non-Prime Mark",
            "45":"Prime Marker",
            "51":"Final Compare",
            "52":"Is Prime",
            "53":"Not Prime"
        }

        self.colour_alias = {
            "1":[0,0,0,0],
            "2":[17,85,204,0],
            "3":[109,158,235,0],
            "4":[102,102,102,0],
            "5":[0,255,255,0],
            "6":[252,229,205,0],
            "7":[249,203,156,0],
            "8":[246,178,107,0],
            "9":[230,145,56,0],
            "10":[180,95,6,0],
            "11":[120,64,3,0],
            "12":[234,209,220,0],
            "13":[213,166,189,0],
            "14":[194,123,160,0],
            "15":[166,77,121,0],
            "16":[116,27,71,0],
            "17":[76,17,4,20],
            "18":[255,255,0,0],
            "19":[255,0,255,0],
            "20":[0,255,0,0],
            "21":[19,79,92,0],
            "22":[118,165,175,0],
            "23":[162,196,201,0],
            "24":[106,168,79,0],
            "25":[147,196,125,0],
            "26":[255,242,205,0],
            "27":[255,229,153,0],
            "28":[255,217,201,0],
            "29":[241,194,50,0],
            "30":[32,18,77,0],
            "31":[53,28,117,0],
            "32":[103,78,167,0],
            "33":[11,83,148,0],
            "34":[61,133,198,0],
            "35":[69,129,142,0],
            "41":[100,255,100,0],
            "45":[255,100,100,0],
            #"51":[140,140,120,255],
            "52":[0,255,0,0],
            "53":[255,0,0,0],

            "36":[255,160,180,0],
            "37":[160,255,160,0],
            "38":[160,160,255,0],
            "39":[160,255,255,0],
            "40":[255,160,255,0],
            "41":[255,255,160,0],
            "42":[105,105,105,0],
            "43":[255,255,255,0],
            "44":[60,200,200,0],
            "45":[45,150,150,0],
            "46":[254,216,176,0],
            "47":[248,213,104,0],
            "48":[255,174,66,0],
            "49":[255,159,0,0],
            "50":[255,103,0,0],
            "51":[190, 48, 255,0],
            #"52":[154, 39, 207,255]
        }

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = last_cell_state

        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))


        # [41] IS PRIME
        # [45]is no prime

        # Prime gen LCR rules
        #if last_cell_state == X or last_cell_state[0] > 35:


        if self.LCR(48,38,48,last_cell_state,neighbors_last_states):
            new_cell_state = [47]
        elif self.LCR(41,-1,39,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(45,-1,38,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(45,-1,46,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(48,42,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [43]
        elif self.LCR(48,43,42,last_cell_state,neighbors_last_states):
            new_cell_state = [48]
        elif self.LCR(50,43,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [36]
        elif self.LCR(43,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [42]
        elif self.LCR(50,36,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [37]
        elif self.LCR(-1,36,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [36]
        elif self.LCR(36,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [43]
        elif self.LCR(37,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]
        elif self.LCR(39,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]
        elif self.LCR(40,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]
        elif self.LCR(50,37,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [39]
        elif self.LCR(-1,39,43,last_cell_state,neighbors_last_states):
            new_cell_state = [39]
        elif self.LCR(-1,39,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [40]
        elif self.LCR(-1,40,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [38]
        elif self.LCR(50,38,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [47]
        elif self.LCR(-1,37,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [37]
        elif self.LCR(-1,38,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [38]
        elif self.LCR(-1,43,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [43]
        elif self.LCR(-1,46,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [45]
        elif self.LCR(-1,47,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [46]
        elif self.LCR(46,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]

        elif self.LCR(48,-1,36,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(48,-1,37,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(48,-1,38,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(48,-1,40,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(48,-1,41,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(48,-1,45,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(48,-1,46,last_cell_state,neighbors_last_states):
            new_cell_state = [50]

        elif self.LCR(48,0,43,last_cell_state,neighbors_last_states):
            new_cell_state = [50]

        elif self.LCR(49,-1,41,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(49,-1,45,last_cell_state,neighbors_last_states):
            new_cell_state = [50]

        elif self.LCR(45,0,41,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(45,0,45,last_cell_state,neighbors_last_states):
            new_cell_state = [50]

        elif self.LCR(45,44,41,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(45,44,45,last_cell_state,neighbors_last_states):
            new_cell_state = [50]

        elif self.LCR(45,48,41,last_cell_state,neighbors_last_states):
            new_cell_state = [50]
        elif self.LCR(45,48,45,last_cell_state,neighbors_last_states):
            new_cell_state = [50]

        elif self.LCR(41,-1,41,last_cell_state,neighbors_last_states):
            new_cell_state = [0]
        elif self.LCR(-1,-1,45,last_cell_state,neighbors_last_states):
            new_cell_state = [44]

        elif self.LCR(41,50,44,last_cell_state,neighbors_last_states):
            new_cell_state = [49]
        elif self.LCR(45,50,44,last_cell_state,neighbors_last_states):
            new_cell_state = [49]

        elif self.LCR(-1,41,44,last_cell_state,neighbors_last_states):
            new_cell_state = [45]
        elif self.LCR(-1,41,49,last_cell_state,neighbors_last_states):
            new_cell_state = [45]
        elif self.LCR(-1,41,50,last_cell_state,neighbors_last_states):
            new_cell_state = [45]

        elif self.LCR(-1,45,44,last_cell_state,neighbors_last_states):
            new_cell_state = [45]
        elif self.LCR(-1,45,49,last_cell_state,neighbors_last_states):
            new_cell_state = [45]
        elif self.LCR(-1,45,50,last_cell_state,neighbors_last_states):
            new_cell_state = [45]

        elif self.LCR(-1,41,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [41]
        elif self.LCR(-1,45,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [41]

        elif self.LCR(41,50,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]
        elif self.LCR(45,50,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]

        elif self.LCR(48,-1,44,last_cell_state,neighbors_last_states):
            new_cell_state = [49]
        elif self.LCR(48,-1,50,last_cell_state,neighbors_last_states):
            new_cell_state = [49]

        elif self.LCR(49,-1,44,last_cell_state,neighbors_last_states):
            new_cell_state = [49]
        elif self.LCR(49,-1,50,last_cell_state,neighbors_last_states):
            new_cell_state = [49]

        elif self.LCR(48,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]
        elif self.LCR(49,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [48]

        elif self.LCR(-1,-1,50,last_cell_state,neighbors_last_states):
            new_cell_state = [50]

        elif self.LCR(-1,-1,44,last_cell_state,neighbors_last_states):
            new_cell_state = [44]
        elif self.LCR(-1,-1,49,last_cell_state,neighbors_last_states):
            new_cell_state = [44]

        elif self.LCR(-1,-1,-1,last_cell_state,neighbors_last_states):
            new_cell_state = [0]


        #if last_cell_state == X or last_cell_state[0] <= 35:
            # Count down
        # Pass/fail signals
        if last_cell_state == BORDER and right == SIGNAL_VMINUS and top == [45]:
            new_cell_state = NOT_PRIME
        elif last_cell_state == BORDER and right == SIGNAL_VMINUS and top == [41]:
            new_cell_state = PRIME
        elif last_cell_state == PRIME or last_cell_state == NOT_PRIME:
            new_cell_state = last_cell_state
        elif last_cell_state == SIGNAL_VMINUS and top == SETUP_3:
            new_cell_state = BORDER

        # Countdown progress
        elif last_cell_state == COUNTDOWN_0_3:
            new_cell_state = COUNTDOWN_0_2
        elif last_cell_state == COUNTDOWN_0_2:
            new_cell_state = COUNTDOWN_0_1
        elif last_cell_state == COUNTDOWN_0_1: # RIGHTMOST
            new_cell_state = [43]
        elif last_cell_state == COUNTDOWN_1_2:
            new_cell_state = COUNTDOWN_1_1
        elif last_cell_state == COUNTDOWN_1_1: # RIGHT
            new_cell_state = [39]
        elif last_cell_state == COUNTDOWN_2_1: # LEFT
            new_cell_state = X
        elif last_cell_state == SETUP_3 and right == COUNTDOWN_2_1: #LEFTMOST
            new_cell_state = [45]

        # Countdown gen
        elif last_cell_state == SETUP_0 and (bot == SIGNAL_VMINUS or bot == MID):
            new_cell_state = COUNTDOWN_0_3
        elif last_cell_state == SETUP_1 and right == COUNTDOWN_0_3:
            new_cell_state = COUNTDOWN_1_2
        elif last_cell_state == SETUP_2 and right == COUNTDOWN_1_2:
            new_cell_state = COUNTDOWN_2_1

        # Prime setup rules
        elif last_cell_state == X and bot == INITMIDPOINT:
            new_cell_state = SETUP_3
        elif last_cell_state == X and left == SETUP_3:
            new_cell_state = SETUP_2
        elif last_cell_state == X and left == SETUP_2:
            new_cell_state = SETUP_1
        elif last_cell_state == X and left == SETUP_1:
            new_cell_state = SETUP_0
        elif last_cell_state == SETUP_3 or last_cell_state == SETUP_2 or last_cell_state == SETUP_1 or last_cell_state == SETUP_0:
            new_cell_state = last_cell_state

        # Cap rules
        elif last_cell_state == CAP and (right == X or right == BORDER):
            new_cell_state = X
        elif last_cell_state == CAP and right == CELL:
            new_cell_state = X
        elif last_cell_state == CAP:
            new_cell_state = CAP
        elif (last_cell_state == X or last_cell_state == BORDER) and left == CAP:
            new_cell_state = CAP

        # Midpoint init stuff
        elif last_cell_state == CELL and left == CAP:
            new_cell_state = INITMIDPOINT
        elif last_cell_state == INITMIDPOINT:
            new_cell_state = SIGNAL_1
        elif left == INITMIDPOINT:
            new_cell_state = SIGNAL_V1

        # Midpoint found
        elif last_cell_state == MID:
            new_cell_state = CELL
        elif right == MID:
            new_cell_state = SIGNAL_VMINUS
        elif left == MID and last_cell_state == SIGNAL_0:
            new_cell_state = SIGNAL_V1
        elif left == MID and last_cell_state == CELL:
            new_cell_state = V1_DELAY
        elif last_cell_state == V1_DELAY:
            new_cell_state = SIGNAL_V1

        # Midpoint finding
        elif (last_cell_state == SIGNAL_0 or last_cell_state == SIGNAL_1 or last_cell_state == SIGNAL_2) and right == SIGNAL_VMINUS:
            new_cell_state = MID
        elif last_cell_state == SIGNAL_0:
            new_cell_state = SIGNAL_1
        elif last_cell_state == SIGNAL_1:
            new_cell_state = SIGNAL_2
        elif last_cell_state == SIGNAL_2:
            new_cell_state = CELL
        elif left == SIGNAL_2:
            new_cell_state = SIGNAL_0
        elif last_cell_state == CELL and left == SIGNAL_V1:
            new_cell_state = SIGNAL_V1
        elif last_cell_state == SIGNAL_V1 and right == CELL:
            new_cell_state = CELL
        elif last_cell_state == SIGNAL_V1 and right == X:
            new_cell_state = SIGNAL_VMINUS
        elif last_cell_state == CELL and right == SIGNAL_VMINUS:
            new_cell_state = SIGNAL_VMINUS
        elif last_cell_state == SIGNAL_VMINUS:
            new_cell_state = CELL

        # Dropper generation
        elif last_cell_state == BIT:
            if top == MARK_1:
                new_cell_state = DROPPER_1
            elif top == MARK_2:
                new_cell_state = DROPPER_2
            elif top == MARK_4:
                new_cell_state = DROPPER_4
            elif top == MARK_8:
                new_cell_state = DROPPER_8
            elif top == MARK_16:
                new_cell_state = DROPPER_16
            elif top == MARK_32:
                new_cell_state = DROPPER_32
            else:
                new_cell_state = X
            return new_cell_state

        # Dropper split rules
        elif last_cell_state == DROPPER_2 and right == X:
            new_cell_state = DROPPER_1
        elif last_cell_state == X and left == DROPPER_2:
            new_cell_state = DROPPER_1

        elif last_cell_state == DROPPER_4 and right == X:
            new_cell_state = DROPPER_2
        elif last_cell_state == X and left == DROPPER_4:
            new_cell_state = DROPPER_2

        elif last_cell_state == DROPPER_8 and right == X:
            new_cell_state = DROPPER_4
        elif last_cell_state == X and left == DROPPER_8:
            new_cell_state = DROPPER_4

        elif last_cell_state == DROPPER_16 and right == X:
            new_cell_state = DROPPER_8
        elif last_cell_state == X and left == DROPPER_16:
            new_cell_state = DROPPER_8

        elif last_cell_state == DROPPER_32 and right == X:
            new_cell_state = DROPPER_16
        elif last_cell_state == X and left == DROPPER_32:
            new_cell_state = DROPPER_16

        # dropper move rules
        elif last_cell_state == DROPPER_1 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_1:
            new_cell_state = DROPPER_1

        elif last_cell_state == DROPPER_2 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_2:
            new_cell_state = DROPPER_2

        elif last_cell_state == DROPPER_4 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_4:
            new_cell_state = DROPPER_4

        elif last_cell_state == DROPPER_8 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_8:
            new_cell_state = DROPPER_8

        elif last_cell_state == DROPPER_16 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_16:
            new_cell_state = DROPPER_16

        elif last_cell_state == DROPPER_32 and right == X:
            new_cell_state = X
        elif last_cell_state == X and left == DROPPER_32:
            new_cell_state = DROPPER_32


        # Border rules
        elif last_cell_state == BORDER and left == DROPPER_1:
            new_cell_state = BORDER_ACT
        elif last_cell_state == BORDER and left == BORDER_ACT:
            new_cell_state = CELL
        elif last_cell_state == BORDER:
            new_cell_state = BORDER
        elif last_cell_state == BORDER_ACT:
            new_cell_state = BORDER

        # Cell rules
        elif last_cell_state == CELL and left == BORDER_ACT:
            new_cell_state = CELL_ACT
        elif last_cell_state == DROPPER_1 and right == BORDER:
            new_cell_state = X
        elif last_cell_state == X and left == BORDER_ACT:
            new_cell_state = CELL_ACT
        elif last_cell_state == CELL_ACT and right == CELL:
            new_cell_state = CELL
        elif last_cell_state == CELL and left == CELL_ACT:
            new_cell_state = CELL_ACT
        elif last_cell_state == CELL_ACT and right == X:
            new_cell_state = CELL
        elif last_cell_state == X and left == CELL_ACT:
            new_cell_state = CELL
        elif last_cell_state == CELL:
            new_cell_state = CELL



        elif last_cell_state == MARK_1 or last_cell_state == MARK_2 or last_cell_state == MARK_4 or last_cell_state == MARK_8 or last_cell_state == MARK_16 or last_cell_state == MARK_32:
            new_cell_state = X

        return new_cell_state

    def LCR(self,left,current,right,last_cell_state,neighbors_last_states):
        con_left = True if left == -1 and (last_cell_state == X or last_cell_state[0] > 35) \
            else (left == neighbors_last_states[0][0])
        con_right = True if right == -1 and (last_cell_state == X or last_cell_state[0] > 35) \
            else (right == neighbors_last_states[3][0])
        con_centre = True if current == -1 and (last_cell_state == X or last_cell_state[0] > 35) \
            else (current == last_cell_state[0])
        return (con_left and con_centre and con_right)
