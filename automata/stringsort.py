from automata.cellloader import CellLoader,CellularAutomaton
from cellular_automaton import MooreNeighborhood,VonNeumannNeighborhood,EdgeRule

SPACE = [0]
BORDER = [1]
BORDER_1 = [56]
BORDER_2 = [57]
spaceship = [58]
spaceship_2 = [59]
spaceship_3 = [60]
spaceship_4 = [61]

a0w0k0m0 = [2]
a0w0k0m1 = [3]
a0w0k1m0 = [4]
a0w0k1m1 = [5]
a0w0k2m0 = [6]
a0w0k2m1 = [7]

a0w1k0m0 = [8]
a0w1k0m1 = [9]
a0w1k1m0 = [10]
a0w1k1m1 = [11]
a0w1k2m0 = [12]
a0w1k2m1 = [13]

a0w2k0m0 = [14]
a0w2k0m1 = [15]
a0w2k1m0 = [16]
a0w2k1m1 = [17]
a0w2k2m0 = [18]
a0w2k2m1 = [19]

""""""

a1w0k0m0 = [20]
a1w0k0m1 = [21]
a1w0k1m0 = [22]
a1w0k1m1 = [23]
a1w0k2m0 = [24]
a1w0k2m1 = [25]

a1w1k0m0 = [26]
a1w1k0m1 = [27]
a1w1k1m0 = [28]
a1w1k1m1 = [29]
a1w1k2m0 = [30]
a1w1k2m1 = [31]

a1w2k0m0 = [32]
a1w2k0m1 = [33]
a1w2k1m0 = [34]
a1w2k1m1 = [35]
a1w2k2m0 = [36]
a1w2k2m1 = [37]

""""""

a2w0k0m0 = [38]
a2w0k0m1 = [39]
a2w0k1m0 = [40]
a2w0k1m1 = [41]
a2w0k2m0 = [42]
a2w0k2m1 = [43]

a2w1k0m0 = [44]
a2w1k0m1 = [45]
a2w1k1m0 = [46]
a2w1k1m1 = [47]
a2w1k2m0 = [48]
a2w1k2m1 = [49]

a2w2k0m0 = [50]
a2w2k0m1 = [51]
a2w2k1m0 = [52]
a2w2k1m1 = [53]
a2w2k2m0 = [54]
a2w2k2m1 = [55]

BORDERS = [BORDER,BORDER_1,BORDER_2]

class stringsort(CellularAutomaton):
    """ A CA to sort strings in the language abc"""

    def __init__(self,initcells):

        cell_loader = CellLoader(initcells)
        self.initcells = cell_loader.get_cells()
        self.rowC = cell_loader.get_rowC()
        self.colC = cell_loader.get_colC()

        self.edge_rule = EdgeRule.FIRST_AND_LAST_CELL_OF_DIMENSION_ARE_NEIGHBORS

        super().__init__(dimension=[cell_loader.get_rowC(),cell_loader.get_colC()],
                         neighborhood=VonNeumannNeighborhood(self.edge_rule))
        self.name = "stringsort"
        self.stateC = 62
        self.statenames = {
            "0":"SPACE",
            "1":"BORDER",
            "56":"BORDER_1",
            "57":"BORDER_2",
            "58":"spaceship",
            "59":"spaceship_2",
            "60":"spaceship_3",
            "61":"spaceship_4",
            "2":"a0w0k0m0",
            "3":"a0w0k0m1",
            "4":"a0w0k1m0",
            "5":"a0w0k1m1",
            "6":"a0w0k2m0",
            "7":"a0w0k2m1",
            "8":"a0w1k0m0",
            "9":"a0w1k0m1",
            "10":"a0w1k1m0",
            "11":"a0w1k1m1",
            "12":"a0w1k2m0",
            "13":"a0w1k2m1",
            "14":"a0w2k0m0",
            "15":"a0w2k0m1",
            "16":"a0w2k1m0",
            "17":"a0w2k1m1",
            "18":"a0w2k2m0",
            "19":"a0w2k2m1",
            "20":"a1w0k0m0",
            "21":"a1w0k0m1",
            "22":"a1w0k1m0",
            "23":"a1w0k1m1",
            "24":"a1w0k2m0",
            "25":"a1w0k2m1",
            "26":"a1w1k0m0",
            "27":"a1w1k0m1",
            "28":"a1w1k1m0",
            "29":"a1w1k1m1",
            "30":"a1w1k2m0",
            "31":"a1w1k2m1",
            "32":"a1w2k0m0",
            "33":"a1w2k0m1",
            "34":"a1w2k1m0",
            "35":"a1w2k1m1",
            "36":"a1w2k2m0",
            "37":"a1w2k2m1",
            "38":"a2w0k0m0",
            "39":"a2w0k0m1",
            "40":"a2w0k1m0",
            "41":"a2w0k1m1",
            "42":"a2w0k2m0",
            "43":"a2w0k2m1",
            "44":"a2w1k0m0",
            "45":"a2w1k0m1",
            "46":"a2w1k1m0",
            "47":"a2w1k1m1",
            "48":"a2w1k2m0",
            "49":"a2w1k2m1",
            "50":"a2w2k0m0",
            "51":"a2w2k0m1",
            "52":"a2w2k1m0",
            "53":"a2w2k1m1",
            "54":"a2w2k2m0",
            "55":"a2w2k2m1"
        }

        self.colour_alias = {
            "1":[70,70,70,0],
            "56":[45,45,45,0],
            "57":[105,105,105,0],
            "58":[0,200,0,0],
            "59":[0,0,200,0],
            "60":[200,0,0,0],
            "61":[60,160,5505]
        }

        self.colour_alias.update(dict.fromkeys([str(x) for x in range(2,20)],[255,190,190,0]))
        self.colour_alias.update(dict.fromkeys([str(x) for x in range(20,38)],[255,140,140,0]))
        self.colour_alias.update(dict.fromkeys([str(x) for x in range(38,56)],[255,90,90,0]))


    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = SPACE

        top,bot,left,right = (
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (-1, 0)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, -1)),
            self._neighborhood.get_neighbor_by_relative_coordinate(neighbors_last_states, (0, 1)))

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

        a,w,k,m = self.awkm_from_state(last_cell_state)

        # k rules and border progression.
        if self.get_evolution_step() % 3 == 0:

            # K rules to transfer cells to border
            if last_cell_state == BORDER and self.awkm_from_state(left)[2] == 1:
                return BORDER_1
            elif last_cell_state == BORDER and self.awkm_from_state(left)[2] == 2:
                return BORDER_2
            elif last_cell_state == BORDER:
                return BORDER

            # k border decays into normal border
            if last_cell_state == BORDER_1 or last_cell_state == BORDER_2:
                return BORDER

            # k front progression
            if left != BORDER and left != BORDER_1 and left != BORDER_2:
                k = self.awkm_from_state(left)[2]
            elif left == BORDER:
                k = 0
            elif m == 0 and left == BORDER_1:
                k = 2
            elif m == 0 and left == BORDER_2:
                k = 1
            elif m == 1 and left == BORDER_1:
                k = 1
            elif m == 1 and left == BORDER_2:
                k = 2
            else:
                k = k

            return self.state_from_awkm(a,w,k,m)

        # No use trying to change a border outside kstep
        if last_cell_state in BORDERS:
            return last_cell_state

        # delta rules
        if self.get_evolution_step() % 3 == 1 or self.get_evolution_step() % 3 == 2:

            # if k like below, compare side = bot
            if self.awkm_from_state(bot)[2] == k and k != 0 and all([bot != cell for cell in [SPACE,spaceship,spaceship_2,spaceship_3]]):
                delta = bot
                #print(a,w,k,m,"  | step",self.get_evolution_step()," | delta top, awkm delta = ", self.awkm_from_state(bot))
            elif self.awkm_from_state(top)[2] == k and k != 0 and all([top != cell for cell in [SPACE,spaceship,spaceship_2,spaceship_3]]):
                delta = top
                #print(a,w,k,m,"  | step",self.get_evolution_step()," | delta bot, awkm delta = ", self.awkm_from_state(top))
            else:
                return self.state_from_awkm(a,w,k,m)

        # w rules
        if self.get_evolution_step() % 3 == 1:
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
            return self.state_from_awkm(a,w,k,m)


        # a rules
        if self.get_evolution_step() % 3 == 2:
            """print(a,w,k,m,"  | step",self.get_evolution_step(),
                " | ","top" if delta == bot else "bot",
                " awkm delta =",
                 self.awkm_from_state(delta))"""
            # Swap if both agree to a swap
            if (self.awkm_from_state(delta)[1] == 1 and w == 1):
                a = self.awkm_from_state(delta)[0]
            elif w != self.awkm_from_state(delta)[1]:
                a = a
            return self.state_from_awkm(a,w,k,m)

        return self.state_from_awkm(a,w,k,m)

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
