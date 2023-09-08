from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule
import random

SPACE = [0]
BORDER = [1]
BORDER_1_0 = [164]
BORDER_2_0 = [165]

BORDER_1_1 = [166]
BORDER_2_1 = [167]

BORDER_1_2 = [168]
BORDER_2_2 = [169]



spaceship = [170]
spaceship_2 = [171]
spaceship_3 = [172]
spaceship_4 = [173]


"""
####################################
"""

a0w0k0m0_0 = [2]
a0w0k0m1_0 = [3]
a0w0k1m0_0 = [4]
a0w0k1m1_0 = [5]
a0w0k2m0_0 = [6]
a0w0k2m1_0 = [7]

a0w1k0m0_0 = [8]
a0w1k0m1_0 = [9]
a0w1k1m0_0 = [10]
a0w1k1m1_0 = [11]
a0w1k2m0_0 = [12]
a0w1k2m1_0 = [13]

a0w2k0m0_0 = [14]
a0w2k0m1_0 = [15]
a0w2k1m0_0 = [16]
a0w2k1m1_0 = [17]
a0w2k2m0_0 = [18]
a0w2k2m1_0 = [19]

""""""

a1w0k0m0_0 = [20]
a1w0k0m1_0 = [21]
a1w0k1m0_0 = [22]
a1w0k1m1_0 = [23]
a1w0k2m0_0 = [24]
a1w0k2m1_0 = [25]

a1w1k0m0_0 = [26]
a1w1k0m1_0 = [27]
a1w1k1m0_0 = [28]
a1w1k1m1_0 = [29]
a1w1k2m0_0 = [30]
a1w1k2m1_0 = [31]

a1w2k0m0_0 = [32]
a1w2k0m1_0 = [33]
a1w2k1m0_0 = [34]
a1w2k1m1_0 = [35]
a1w2k2m0_0 = [36]
a1w2k2m1_0 = [37]

""""""

a2w0k0m0_0 = [38]
a2w0k0m1_0 = [39]
a2w0k1m0_0 = [40]
a2w0k1m1_0 = [41]
a2w0k2m0_0 = [42]
a2w0k2m1_0 = [43]

a2w1k0m0_0 = [44]
a2w1k0m1_0 = [45]
a2w1k1m0_0 = [46]
a2w1k1m1_0 = [47]
a2w1k2m0_0 = [48]
a2w1k2m1_0 = [49]

a2w2k0m0_0 = [50]
a2w2k0m1_0 = [51]
a2w2k1m0_0 = [52]
a2w2k1m1_0 = [53]
a2w2k2m0_0 = [54]
a2w2k2m1_0 = [55]

"""
####################################
"""

a0w0k0m0_1 = [56]
a0w0k0m1_1 = [57]
a0w0k1m0_1 = [58]
a0w0k1m1_1 = [59]
a0w0k2m0_1 = [60]
a0w0k2m1_1 = [61]

a0w1k0m0_1 = [62]
a0w1k0m1_1 = [63]
a0w1k1m0_1 = [64]
a0w1k1m1_1 = [65]
a0w1k2m0_1 = [66]
a0w1k2m1_1 = [67]

a0w2k0m0_1 = [68]
a0w2k0m1_1 = [69]
a0w2k1m0_1 = [70]
a0w2k1m1_1 = [71]
a0w2k2m0_1 = [72]
a0w2k2m1_1 = [73]

""""""

a1w0k0m0_1 = [74]
a1w0k0m1_1 = [75]
a1w0k1m0_1 = [76]
a1w0k1m1_1 = [77]
a1w0k2m0_1 = [78]
a1w0k2m1_1 = [79]

a1w1k0m0_1 = [80]
a1w1k0m1_1 = [81]
a1w1k1m0_1 = [82]
a1w1k1m1_1 = [83]
a1w1k2m0_1 = [84]
a1w1k2m1_1 = [85]

a1w2k0m0_1 = [86]
a1w2k0m1_1 = [87]
a1w2k1m0_1 = [88]
a1w2k1m1_1 = [89]
a1w2k2m0_1 = [90]
a1w2k2m1_1 = [91]

""""""

a2w0k0m0_1 = [92]
a2w0k0m1_1 = [93]
a2w0k1m0_1 = [94]
a2w0k1m1_1 = [95]
a2w0k2m0_1 = [96]
a2w0k2m1_1 = [97]

a2w1k0m0_1 = [98]
a2w1k0m1_1 = [99]
a2w1k1m0_1 = [100]
a2w1k1m1_1 = [101]
a2w1k2m0_1 = [102]
a2w1k2m1_1 = [103]

a2w2k0m0_1 = [104]
a2w2k0m1_1 = [105]
a2w2k1m0_1 = [106]
a2w2k1m1_1 = [107]
a2w2k2m0_1 = [108]
a2w2k2m1_1 = [109]

"""
#####################################
"""

a0w0k0m0_2 = [110]
a0w0k0m1_2 = [111]
a0w0k1m0_2 = [112]
a0w0k1m1_2 = [113]
a0w0k2m0_2 = [114]
a0w0k2m1_2 = [115]

a0w1k0m0_2 = [116]
a0w1k0m1_2 = [117]
a0w1k1m0_2 = [118]
a0w1k1m1_2 = [119]
a0w1k2m0_2 = [120]
a0w1k2m1_2 = [121]

a0w2k0m0_2 = [122]
a0w2k0m1_2 = [123]
a0w2k1m0_2 = [124]
a0w2k1m1_2 = [125]
a0w2k2m0_2 = [126]
a0w2k2m1_2 = [127]

""""""

a1w0k0m0_2 = [128]
a1w0k0m1_2 = [129]
a1w0k1m0_2 = [130]
a1w0k1m1_2 = [131]
a1w0k2m0_2 = [132]
a1w0k2m1_2 = [133]

a1w1k0m0_2 = [134]
a1w1k0m1_2 = [135]
a1w1k1m0_2 = [136]
a1w1k1m1_2 = [137]
a1w1k2m0_2 = [138]
a1w1k2m1_2 = [139]

a1w2k0m0_2 = [140]
a1w2k0m1_2 = [141]
a1w2k1m0_2 = [142]
a1w2k1m1_2 = [143]
a1w2k2m0_2 = [144]
a1w2k2m1_2 = [145]

""""""

a2w0k0m0_2 = [146]
a2w0k0m1_2 = [147]
a2w0k1m0_2 = [148]
a2w0k1m1_2 = [149]
a2w0k2m0_2 = [150]
a2w0k2m1_2 = [151]

a2w1k0m0_2 = [152]
a2w1k0m1_2 = [153]
a2w1k1m0_2 = [154]
a2w1k1m1_2 = [155]
a2w1k2m0_2 = [156]
a2w1k2m1_2 = [157]

a2w2k0m0_2 = [158]
a2w2k0m1_2 = [159]
a2w2k1m0_2 = [160]
a2w2k1m1_2 = [161]
a2w2k2m0_2 = [162]
a2w2k2m1_2 = [163]

"""
#######################################
"""

"""
    Take away 54 to get to base state

    k states:
        2 -> 55
    w states:
        56 -> 109
    a states:
        110 -> 163

        BORDER_1_0 = [164]
        BORDER_2_0 = [165]

        BORDER_1_1 = [166]
        BORDER_2_1 = [167]

        BORDER_1_2 = [168]
        BORDER_2_2 = [169]

"""

BORDERS = [BORDER,BORDER_1_0,BORDER_2_0,BORDER_1_1,BORDER_2_1,BORDER_1_2,BORDER_2_2]

class stringsort2(CellularAutomaton):
    """ A CA to sort strings in the language abc"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "stringsort2"
        self.stateC = 174
        self.statenames = {
            "0":"SPACE",
            "1":"BORDER",
            "164":"BORDER_1_0",
            "165":"BORDER_2_0",
            "166":"BORDER_1_1",
            "167":"BORDER_2_1",
            "168":"BORDER_1_2",
            "169":"BORDER_2_2",
            "170":"spaceship",
            "171":"spaceship_2",
            "172":"spaceship_3",
            "173":"spaceship_4",
            "2":"a0w0k0m0_0",
            "3":"a0w0k0m1_0",
            "4":"a0w0k1m0_0",
            "5":"a0w0k1m1_0",
            "6":"a0w0k2m0_0",
            "7":"a0w0k2m1_0",
            "8":"a0w1k0m0_0",
            "9":"a0w1k0m1_0",
            "10":"a0w1k1m0_0",
            "11":"a0w1k1m1_0",
            "12":"a0w1k2m0_0",
            "13":"a0w1k2m1_0",
            "14":"a0w2k0m0_0",
            "15":"a0w2k0m1_0",
            "16":"a0w2k1m0_0",
            "17":"a0w2k1m1_0",
            "18":"a0w2k2m0_0",
            "19":"a0w2k2m1_0",
            "20":"a1w0k0m0_0",
            "21":"a1w0k0m1_0",
            "22":"a1w0k1m0_0",
            "23":"a1w0k1m1_0",
            "24":"a1w0k2m0_0",
            "25":"a1w0k2m1_0",
            "26":"a1w1k0m0_0",
            "27":"a1w1k0m1_0",
            "28":"a1w1k1m0_0",
            "29":"a1w1k1m1_0",
            "30":"a1w1k2m0_0",
            "31":"a1w1k2m1_0",
            "32":"a1w2k0m0_0",
            "33":"a1w2k0m1_0",
            "34":"a1w2k1m0_0",
            "35":"a1w2k1m1_0",
            "36":"a1w2k2m0_0",
            "37":"a1w2k2m1_0",
            "38":"a2w0k0m0_0",
            "39":"a2w0k0m1_0",
            "40":"a2w0k1m0_0",
            "41":"a2w0k1m1_0",
            "42":"a2w0k2m0_0",
            "43":"a2w0k2m1_0",
            "44":"a2w1k0m0_0",
            "45":"a2w1k0m1_0",
            "46":"a2w1k1m0_0",
            "47":"a2w1k1m1_0",
            "48":"a2w1k2m0_0",
            "49":"a2w1k2m1_0",
            "50":"a2w2k0m0_0",
            "51":"a2w2k0m1_0",
            "52":"a2w2k1m0_0",
            "53":"a2w2k1m1_0",
            "54":"a2w2k2m0_0",
            "55":"a2w2k2m1_0",
            "56":"a0w0k0m0_1",
            "57":"a0w0k0m1_1",
            "58":"a0w0k1m0_1",
            "59":"a0w0k1m1_1",
            "60":"a0w0k2m0_1",
            "61":"a0w0k2m1_1",
            "62":"a0w1k0m0_1",
            "63":"a0w1k0m1_1",
            "64":"a0w1k1m0_1",
            "65":"a0w1k1m1_1",
            "66":"a0w1k2m0_1",
            "67":"a0w1k2m1_1",
            "68":"a0w2k0m0_1",
            "69":"a0w2k0m1_1",
            "70":"a0w2k1m0_1",
            "71":"a0w2k1m1_1",
            "72":"a0w2k2m0_1",
            "73":"a0w2k2m1_1",
            "74":"a1w0k0m0_1",
            "75":"a1w0k0m1_1",
            "76":"a1w0k1m0_1",
            "77":"a1w0k1m1_1",
            "78":"a1w0k2m0_1",
            "79":"a1w0k2m1_1",
            "80":"a1w1k0m0_1",
            "81":"a1w1k0m1_1",
            "82":"a1w1k1m0_1",
            "83":"a1w1k1m1_1",
            "84":"a1w1k2m0_1",
            "85":"a1w1k2m1_1",
            "86":"a1w2k0m0_1",
            "87":"a1w2k0m1_1",
            "88":"a1w2k1m0_1",
            "89":"a1w2k1m1_1",
            "90":"a1w2k2m0_1",
            "91":"a1w2k2m1_1",
            "92":"a2w0k0m0_1",
            "93":"a2w0k0m1_1",
            "94":"a2w0k1m0_1",
            "95":"a2w0k1m1_1",
            "96":"a2w0k2m0_1",
            "97":"a2w0k2m1_1",
            "98":"a2w1k0m0_1",
            "99":"a2w1k0m1_1",
            "100":"a2w1k1m0_1",
            "101":"a2w1k1m1_1",
            "102":"a2w1k2m0_1",
            "103":"a2w1k2m1_1",
            "104":"a2w2k0m0_1",
            "105":"a2w2k0m1_1",
            "106":"a2w2k1m0_1",
            "107":"a2w2k1m1_1",
            "108":"a2w2k2m0_1",
            "109":"a2w2k2m1_1",
            "110":"a0w0k0m0_2",
            "111":"a0w0k0m1_2",
            "112":"a0w0k1m0_2",
            "113":"a0w0k1m1_2",
            "114":"a0w0k2m0_2",
            "115":"a0w0k2m1_2",
            "116":"a0w1k0m0_2",
            "117":"a0w1k0m1_2",
            "118":"a0w1k1m0_2",
            "119":"a0w1k1m1_2",
            "120":"a0w1k2m0_2",
            "121":"a0w1k2m1_2",
            "122":"a0w2k0m0_2",
            "123":"a0w2k0m1_2",
            "124":"a0w2k1m0_2",
            "125":"a0w2k1m1_2",
            "126":"a0w2k2m0_2",
            "127":"a0w2k2m1_2",
            "128":"a1w0k0m0_2",
            "129":"a1w0k0m1_2",
            "130":"a1w0k1m0_2",
            "131":"a1w0k1m1_2",
            "132":"a1w0k2m0_2",
            "133":"a1w0k2m1_2",
            "134":"a1w1k0m0_2",
            "135":"a1w1k0m1_2",
            "136":"a1w1k1m0_2",
            "137":"a1w1k1m1_2",
            "138":"a1w1k2m0_2",
            "139":"a1w1k2m1_2",
            "140":"a1w2k0m0_2",
            "141":"a1w2k0m1_2",
            "142":"a1w2k1m0_2",
            "143":"a1w2k1m1_2",
            "144":"a1w2k2m0_2",
            "145":"a1w2k2m1_2",
            "146":"a2w0k0m0_2",
            "147":"a2w0k0m1_2",
            "148":"a2w0k1m0_2",
            "149":"a2w0k1m1_2",
            "150":"a2w0k2m0_2",
            "151":"a2w0k2m1_2",
            "152":"a2w1k0m0_2",
            "153":"a2w1k0m1_2",
            "154":"a2w1k1m0_2",
            "155":"a2w1k1m1_2",
            "156":"a2w1k2m0_2",
            "157":"a2w1k2m1_2",
            "158":"a2w2k0m0_2",
            "159":"a2w2k0m1_2",
            "160":"a2w2k1m0_2",
            "161":"a2w2k1m1_2",
            "162":"a2w2k2m0_2",
            "163":"a2w2k2m1_2"
        }

        self.colour_alias = {
            "1":[70,70,70,0],
            "164":[45,60,45,0],
            "165":[105,120,105,0],
            "166":[45,45,60,0],
            "167":[105,105,120,0],
            "168":[60,45,45,0],
            "169":[120,105,105,0],
            "170":[0,200,0,0],
            "171":[0,0,200,0],
            "172":[200,0,0,0]
        }
        colscheme = 1
        #""" Symbol colouring - Default
        if colscheme == 1:
            self.colour_alias.update(dict.fromkeys([str(x) for x in range(2,20)],[255,190,190,0]))
            self.colour_alias.update(dict.fromkeys([str(x) for x in range(20,38)],[255,140,140,0]))
            self.colour_alias.update(dict.fromkeys([str(x) for x in range(38,56)],[255,90,90,0]))

            self.colour_alias.update(dict.fromkeys([str(x) for x in range(56,74)],[190,255,190,0]))
            self.colour_alias.update(dict.fromkeys([str(x) for x in range(74,92)],[140,255,140,0]))
            self.colour_alias.update(dict.fromkeys([str(x) for x in range(92,110)],[90,255,90,0]))

            self.colour_alias.update(dict.fromkeys([str(x) for x in range(110,128)],[190,190,255,0]))
            self.colour_alias.update(dict.fromkeys([str(x) for x in range(128,146)],[140,140,255,0]))
            self.colour_alias.update(dict.fromkeys([str(x) for x in range(146,164)],[90,90,255,0]))

        elif colscheme == 3:

            #""" For random colours
            for x in range(2,164):
                self.colour_alias[str(x)] = [random.randint(0,255),random.randint(0,255),random.randint(0,255),0]

        elif colscheme == 2:

            #""" For w-k colouring
            # YELLOW and MAGENTA are k
            # RED means swap needed
            # GREEN means no swap needed
            # GREY means undecided if swap needed
            for x in range(2,164):
                if int((x-2)/2) % 3 == 0:
                    if int((x-2)/6) % 3 == 1:
                        self.colour_alias[str(x)] = [255,180,180,0]
                    elif int((x-2)/6) % 3 == 2:
                        self.colour_alias[str(x)] = [180,255,180,0]
                    else:
                        self.colour_alias[str(x)] = [180,180,180,0]
                elif int((x-2)/2) % 3 == 1:
                    self.colour_alias[str(x)] = [255,180,255,0]
                elif int((x-2)/2) % 3 == 2:
                    self.colour_alias[str(x)] = [255,255,180,0]


        elif colscheme == 4:
            #""" For greyscale colouring
            for x in range(2,164):
                self.colour_alias[str(x)] = [30+x,30+x,30+x,0]




    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = SPACE

        ###
        # This rule set is an adapted form of my previous string sort, which used external clock signals
        # This CA is very very similar, I have essentially just replaced the 3 timestep options
        # to 3 sets of all the states, 54 apart. This means state 20 is basically identical to state 74
        # Where state 74 is in transition 0
        # Transition 0: 3-56, k flag solving
        # Transition 1: 57-109 w flag solving
        # Transition 2: 110-163 a solving
        # If the state is not in transition 0, it (and its neighbours) are minus 54, so the right flags
        # can be solved with my previous function.
        # This could have been done better if I'd started with this method but this was easier to adapt into
        # at the end of a transition, the state is either +54 or -108 to flip to the next transition band
        ###


        # Gets to the states to the sides of the current
        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))

        # Works out flags from state
        a,w,k,m = self.awkm_from_state(last_cell_state)

        # If the last state is too high, due to it being in the transitional stages
        # Then it is incremented to appear as the equivalent state in transition 0
        if last_cell_state[0] >= 56 and last_cell_state[0] <= 109:
            top,bot,left,right = ([state[0]-54] for state in [top,bot,left,right])
            a,w,k,m = self.awkm_from_state([last_cell_state[0]-54])
        if last_cell_state[0] >= 110 and last_cell_state[0] <= 163:
            top,bot,left,right = ([state[0]-108] for state in [top,bot,left,right])
            a,w,k,m = self.awkm_from_state([last_cell_state[0]-108])


        # Visualiser aid rules
        if last_cell_state == spaceship:
            return spaceship_2
        if last_cell_state == spaceship_2:
            return spaceship_3
        if left == spaceship_3:
            return spaceship
        if last_cell_state == spaceship_3:
            return SPACE
        if last_cell_state == SPACE:
            return SPACE

        # Border k inheritance rules
        if last_cell_state == BORDER and \
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1))[0] <= 56 and \
            self.awkm_from_state(left)[2] == 1:
            return BORDER_1_0
        elif last_cell_state == BORDER and \
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1))[0] <= 56 and \
            self.awkm_from_state(left)[2] == 2:
            return BORDER_2_0
        elif last_cell_state == BORDER:
            return BORDER

        # Border persistance/transition rules
        if last_cell_state in BORDERS:
            if last_cell_state == BORDER_1_0:
                return BORDER_1_1
            if last_cell_state == BORDER_2_0:
                return BORDER_2_1
            if last_cell_state == BORDER_1_1:
                return BORDER_1_2
            if last_cell_state == BORDER_2_1:
                return BORDER_2_2
            if last_cell_state == BORDER_1_2:
                return BORDER
            if last_cell_state == BORDER_2_2:
                return BORDER

        # k rules and border progression.
        # Only occurs in transition 0
        if last_cell_state[0] <= 55:

            # k front progression
            if left != BORDER and left != BORDER_1_2 and left != BORDER_2_2:
                k = self.awkm_from_state(left)[2]
            elif left == BORDER:
                k = 0
            elif m == 0 and left == BORDER_1_2:
                k = 2
            elif m == 0 and left == BORDER_2_2:
                k = 1
            elif m == 1 and left == BORDER_1_2:
                k = 1
            elif m == 1 and left == BORDER_2_2:
                k = 2
            else:
                k = k

            # Increment to transition 1
            return [self.state_from_awkm(a,w,k,m)[0]+54]


        # delta rules, performed on transition 1 and 2
        if last_cell_state[0] >= 56 and last_cell_state[0] <= 163:

            # if k like below, compare side = bot
            if self.awkm_from_state(bot)[2] == k and k != 0 and all([bot != cell for cell in [SPACE,spaceship,spaceship_2,spaceship_3,spaceship_4]]):
                delta = bot
                #print(a,w,k,m,"  | step",self.get_evolution_step()," | delta top, awkm delta = ", self.awkm_from_state(bot))
            elif self.awkm_from_state(top)[2] == k and k != 0 and all([top != cell for cell in [SPACE,spaceship,spaceship_2,spaceship_3,spaceship_4]]):
                delta = top
                #print(a,w,k,m,"  | step",self.get_evolution_step()," | delta bot, awkm delta = ", self.awkm_from_state(top))
            else:
                # switch to right transition.
                # if in 1, go to 2,
                # if in 2, go to 0
                if last_cell_state[0] <= 109:
                    return [self.state_from_awkm(a,w,k,m)[0]+108]
                else:
                    return self.state_from_awkm(a,w,k,m)

        # w rules, completed on a 1 transition
        if last_cell_state[0] >= 56 and last_cell_state[0] <= 109:

            # Resetting compare front, so nothing swapped out when not on front
            if w != 0:
                w = 0
            # inheriting a 'dont swap' signal
            if self.awkm_from_state(left)[1] == 2:
                w = 2
            elif ( # Figuring out a swap signal
                (
                    (delta == top and a < self.awkm_from_state(delta)[0]) or
                    (delta == bot and a > self.awkm_from_state(delta)[0])
                )) or \
                (self.awkm_from_state(left)[1] == 1  and all([left != cell for cell in BORDERS])):

                w = 1

            elif ( # Figuring out a dont swap signal
                (
                    (delta == top and a > self.awkm_from_state(delta)[0]) or
                    (delta == bot and a < self.awkm_from_state(delta)[0])
                )):
                w = 2
            return [self.state_from_awkm(a,w,k,m)[0]+108]


        # a rules, completed on a 2 transition
        if last_cell_state[0] >= 109 and last_cell_state[0] <= 163:
            # Swap if both agree to a swap
            if (self.awkm_from_state(delta)[1] == 1 and w == 1):
                a = self.awkm_from_state(delta)[0]
            elif w != self.awkm_from_state(delta)[1]:
                a = a
            return self.state_from_awkm(a,w,k,m)
            # returns the 0 transiton state

        print("Error")
        return SPACE

    # converts an input state into flag and symbol components
    def state_from_awkm(self,a,w,k,m):
        state = 0
        state += 2
        state += 18*a
        state += 6*w
        state += 2*k
        state += m
        return [state]

    # calculates the state given the flags
    def awkm_from_state(self,state):
        m = (state[0]-2) % 2
        k = int((state[0]-2)/2) % 3
        w = int((state[0]-2)/6) % 3
        a = int((state[0]-2)/18) % 3
        return (a,w,k,m)
