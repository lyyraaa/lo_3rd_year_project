from windowModel import WindowModel

import ca_dict

from player import Player
from model import Model
from windowUI import WindowUI
import pyglet
from pyglet.gl import *
import sys
import argparse

from automata.cellloader import CellLoader

################################################################################
### High-level file that initialises everything then starts the pyglet loop ####
################################################################################

CA_dict = ca_dict.ca_dict

def argument_parse():
    parser = argparse.ArgumentParser(description="A 3D viewer to explore cellular automata")

    parser.add_argument("automata", metavar='A', type=str, nargs=1,
        choices=CA_dict.keys(),
        help="Cellular automata to use")
    parser.add_argument("world", metavar='W', type=str, nargs=1,
        help="Input file as starting state")
    parser.add_argument("-s","--steps", nargs=1, type=int, default=[25],
        help="The number of steps to evolve until, default 25")
    parser.add_argument("-cd","--choicedepth", nargs=1, type=int, default=None,
        help="Max number of states to try removing at once for causal analysis")
    parser.add_argument("-m","--match", nargs='*', type=str, default=None,
        help="Add pattern to match, given as *.txt in /patterns directory")
    parser.add_argument("--dark", action = "store_true",
        help="Disable lighting effects")
    parser.add_argument("-ql","--quickload", action = "store_true",
        help="Disable pre-computation of things like causal analysis, will allow larger simulations due to fewer objects in memory")

    args = parser.parse_args()
    return args

if __name__ == '__main__':


    arglist = vars(argument_parse())

    # Initialises the automata with some file pattern configuration
    ca = CA_dict[arglist.get("automata")[0]]("patterns/"+sys.argv[2])

    # Reads the list of files with the patterns to match in
    matchlist = arglist.get("match")

    max_patterns = 20
    match_patterns = []
    if matchlist:
        count = 0
        for match in matchlist:
            count += 1
            cell_loader = CellLoader("patterns/"+match)
            match_cell_pattern = cell_loader.get_cells()
            match_patterns.append((match,match_cell_pattern))
            if count >=max_patterns:
                break

    choice_tier_depth = arglist.get("choicedepth")
    if choice_tier_depth: choice_tier_depth = choice_tier_depth[0]

    # Initialises the player at some location
    player = Player((0.5,1.5,1.5),(-30,0))

    # Initialises the model with the CA and the number of evolutions
    model = Model(ca,arglist.get("steps")[0],match_patterns,max_patterns=max_patterns,choice_tier_depth=choice_tier_depth,quickload=arglist.get("quickload"))

    # Sets up the model window with the player and the model
    windowModel = WindowModel(model, player, width=600, height=450, caption='Model',resizable=True)


    # Sets background color
    glClearColor(0.2,0.25,0.5,1)
    # Allows transparency
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_ONE_MINUS_SRC_ALPHA, pyglet.gl.GL_SRC_ALPHA)


    # Makes sure further objects are not drawn closer
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    glEnable(GL_MULTISAMPLE_ARB)

    if not arglist.get("dark"):
        glEnable(GL_LIGHTING)

        glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat*4)(0.5,0.5,0.5,1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat*4)(0.35,0.35,0.35,1))
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat*4)(0,15,0,1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat*4)(0.15,0.15,0.15,1))
        #glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat*3)(0,10,0))

        glEnable(GL_COLOR_MATERIAL)

        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
        glEnable(GL_LIGHT0)

    # Sets up UI window, with access to the model window -> model
    windowUI = WindowUI(windowModel,width=1000, height=430, caption='UI',resizable=True)

    #windowModel.context.set_current()


    pyglet.app.run()
