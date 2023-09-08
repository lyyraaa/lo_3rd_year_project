import pyglet
from pyglet.gl import *

from cellular_automaton.neighborhood import MooreNeighborhood
from cellular_automaton.neighborhood import VonNeumannNeighborhood
from cellular_automaton.neighborhood import EdgeRule

import ca_dict

from permutations import PERMUTATIONS_VN, FUNDAMENTAL_DIRECTIONS_VN, DIRECTIONS_VN, DIRECTIONS_MOORE, FUNDAMENTAL_DIRECTIONS_MOORE, PERMUTATIONS_MOORE

from colourdict import colourdict

import math

import copy

import time

import numpy as np
################################################################################
### Model class holds the CA and draws the objects in the 3D view ##############
################################################################################

CA_DICT = ca_dict.ca_dict

# Axis parallel vectors for normals for a cube, makes them lit by lighting
CUBE_NORMALS = (0,0,-1)*4+(0,0,1)*4+(-1,0,0)*4+(1,0,0)*4+(0,-1,0)*4+(0,1,0)*4

# Default highlight colours for matched patterns
HIGHLIGHT_COLOURS = [
    (255, 0, 0, 0), #red
    (127, 255, 0, 0), #green
    (0, 0, 255, 0), #blue
    (0, 255, 255, 0), #aqua
    (255, 255, 0, 0), #yellow
    (255, 0, 255, 0), #fuschia
    (148, 0, 211, 0), #darkviolet
    (255, 140, 0, 0), #darkorange
    (0, 255, 127, 0), #springgreen
    (0, 139, 139, 0), #darkcyan
    (255, 192, 203, 0), #pink
    (154, 205, 50, 0), #yellowgreen
    (139, 0, 139, 0), #darkmagenta
    (255, 99, 71, 0), #tomato
    (30, 144, 255, 0), #dodgerblue
    (255, 222, 173, 0), #navajowhite
    (85, 107, 47, 0), #darkolivegreen
    (173, 216, 230, 0), #lightblue
    (0, 0, 139, 0), #darkblue
    (160, 82, 45, 0), #sienna
    (255, 20, 147, 0), #deeppink
    (70, 130, 180, 0), #steelblue
    (184, 134 ,11, 0) , #darkgoldenrod
    (143, 188, 143, 0), #darkseagreen
    (255, 160, 122, 0), #lightsalmon
    (123, 104, 238, 0), #mediumslateblue
    (219, 112, 147, 0), #palevioletred
    (144, 238, 144, 0), #lightgreen
    (218, 112, 214, 0), #orchid
    (72, 61, 139, 0), #darkslateblue
    (34, 139, 34, 0), #forestgreen
]

ca_line_cols = [(0,0,0,0),(255,0,0,0),(0,0,255,0),(0,255,0,0),(0,255,255,0),(255,255,0,0),(255,0,255,0),(255,169,0,0),(160,32,240,0),(255,255,255,0)]

class Model:

    # Method to add a cube of 6 quads to the scene, takes x,y,z coord params
    # as well as a colour/cell state integer
    def add_block(self,x,y,z,colour):

        colourvec =  (*self.colourdict.getColour(colour)[:3],0)
        cube_obj = self.batchlist[colour].add(24, GL_QUADS, None,
            ('v3f/static',self.cube_vertices_from_point(x,y,z)),
            ('n3f/static',CUBE_NORMALS),
            ('c4B/static',colourvec*24)
        )

        return cube_obj

    # Creates a set of vertices given a point, corresponding to 6 quads making a cube
    def cube_vertices_from_point(self,x,y,z,scale=0):
        X, Y, Z = x+1+scale, y+1+scale, z+1+scale
        x, y, z = x-scale, y-scale, z-scale

        cube_points = (X, y, z,  x, y, z,  x, Y, z,  X, Y, z,
            x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z,
            x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z,
            X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z,
            x, y, z,  X, y, z,  X, y, Z,  x, y, Z,
            x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)

        return cube_points

    # Assembles the activity overlay
    # SImply adds a red cube wherever the cell is active in the evolution
    # Activity is calculated elsewhere in init, as the evolution is solved
    def construct_activelens_blocks(self,rackArr):
        active_vertexlist = []
        active_vertex_count = 0
        active_cube_count = 0

        for rowC,row in enumerate(rackArr):
            for colC,col in enumerate(reversed(row)):
                for rackC,rack in enumerate(col):
                    if rack:
                        active_vertexlist += self.cube_vertices_from_point(colC,-rowC,rackC)
                        active_vertex_count += 24
                        active_cube_count += 1
        active_cubeobject = self.batch_activelens.add(active_vertex_count, GL_QUADS, None,
            ('v3f/static', active_vertexlist),
            ('n3f/static',CUBE_NORMALS*active_cube_count),
            ('c4B/static',(255,0,0,0)*active_vertex_count))
        return active_cubeobject

    def causal_analysis_to_object(self,array,directions):

        # set up line verts
        line_verts_array = [[] for x in range(len(directions))]
        # set up line colours
        line_colours_array = [[] for x in range(len(directions))]

        line_obj_array = [None for x in range(len(directions))]

        #flag = self.ca.edge_rule == EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS or self.ca.edge_rule == EdgeRule.IGNORE_EDGE_CELLS

        for step,rack in enumerate(array):
            step = 1+step-self.evolution_steps

            for row,cellrow in enumerate(rack):

                for col,cell in enumerate(cellrow):

                    if not cell: continue
                    for dir_idx,direct in enumerate(cell):
                        if not direct: continue

                        if (row+directions[dir_idx][0]) >= self.ca.rowC or (row+directions[dir_idx][0]) < 0 or (col+directions[dir_idx][1]) >= self.ca.colC or (col+directions[dir_idx][1]) < 0:
                            #if flag: continue
                            up_neighbor_row = (self.ca.rowC-(row+directions[dir_idx][0])%self.ca.rowC)
                            up_neighbor_col = (col+directions[dir_idx][1]) %self.ca.colC

                            # Adding lines the layer above
                            line_verts_array[direct-1] += (up_neighbor_row,step+1,up_neighbor_col)
                            line_verts_array[direct-1] += (up_neighbor_row + directions[dir_idx][0],step,up_neighbor_col - directions[dir_idx][1])
                            line_colours_array[direct-1] += (ca_line_cols[direct])*2

                        line_verts_array[direct-1] += (self.ca.rowC-row,step,col)
                        line_verts_array[direct-1] += (self.ca.rowC-(row+directions[dir_idx][0]),step+1,col+directions[dir_idx][1])
                        line_colours_array[direct-1] += (ca_line_cols[direct])*2

        #print(len(line_verts_array))
        for choose_idx,line_verts in enumerate(line_verts_array):
            #print(choose_idx,len(line_verts))
            for ind in range(0,len(line_verts),3):
                line_verts[ind] -= 0.5
                line_verts[ind+1] += 0.5
                line_verts[ind+2] += 0.5

            # Creating actual line object
            line_obj = self.batchlist_causal_lines[choose_idx].add(int(len(line_verts)/3), GL_LINES, None,
                ('v3f/static', line_verts),
                ('c4B/static', line_colours_array[choose_idx])
            )

            line_obj_array.append(line_obj)

        return line_obj_array


    # Performs the causal analysis on every cell
    def causal_analysis(self,tier_limit = None):

        # The neighborhood type of the CA dictates certain things it has to check
        if type(self.ca._neighborhood) == MooreNeighborhood:
            choice_tiers = [0,9,45,129,255,381,465,501,510] # The indexes in the list of permuations where one more cell is removed
            directions = DIRECTIONS_MOORE # The list of tuples corresponding to row_offset, columns_offset
            permutations = PERMUTATIONS_MOORE # Permutations of removing combinations of cells in a neighborhood
            fundamental_directions = FUNDAMENTAL_DIRECTIONS_MOORE # Binary representations of the direction list
            neighbour_count = 9
            consider_count = 511 # Number of permutations, number to consider
        elif type(self.ca._neighborhood) == VonNeumannNeighborhood:
            choice_tiers = [0,5,15,25,30]
            # left,top,bot,right
            directions = DIRECTIONS_VN
            permutations = PERMUTATIONS_VN
            fundamental_directions = FUNDAMENTAL_DIRECTIONS_VN
            neighbour_count = 5
            consider_count = 31
        else:
            return None

        flag = self.ca.edge_rule == EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS or self.ca.edge_rule == EdgeRule.IGNORE_EDGE_CELLS

        if tier_limit:
            tier_limit = min(tier_limit,len(choice_tiers)-1) # Clipping tier to max value that could distinguish things (so 9C8 or 5C4)
            consider_count = choice_tiers[tier_limit]



        total_permutations_tested = 0
        total_cells = 0

        causal_analysis_array = []

        # Iterates over every single cell
        for evolution in range(self.evolution_steps-1,0,-1):
            causal_rack = []
            for row in range(self.ca.rowC):
                causal_row = []
                for col in range(self.ca.colC):

                    total_cells += 1

                    # Gets current cell to observe any changes when neighbors are changed
                    reference = [self.cellarr[evolution][row][col],]

                    #if reference == [0,]: causal_row.append(None); continue # Skips quiescent cells

                    last_cell_state = [self.cellarr[evolution-1][row][col],] # Gets last cell, one evo up
                    # Gets neighbours in previous step from list of directions
                    neighbors_last_states = [[self.cellarr[evolution-1][(row+direction[0])%self.ca.rowC][(col+direction[1])%self.ca.colC],] for direction in directions[:-1]]

                    # This list is length of no. permutations, boolean says whether to bother trying it
                    consider = [True]*consider_count

                    # This bit removes any permutations involving removing a quiescent cell
                    # Since it will not matter nor be different from the same permutation without quiescent removed
                    # Removal works by performing bitwise AND with the permutation binary and every remaining permutation binary
                    # If after AND, it = the first value, then the current permutation is a subset of the examined one; can be removed
                    dummy_neighbours = neighbors_last_states[:]+[last_cell_state[:],]
                    for fundam_direction_idx,cell in enumerate(dummy_neighbours):
                        if cell == [0,] or (flag and ((row+directions[fundam_direction_idx][0]) >= self.ca.rowC or (row+directions[fundam_direction_idx][0]) < 0 or (col+directions[fundam_direction_idx][1]) >= self.ca.colC or (col+directions[fundam_direction_idx][1]) < 0)):
                            for perm_idx,permutations_future in enumerate(permutations[:consider_count]):
                                if permutations_future[0] & fundamental_directions[fundam_direction_idx] == fundamental_directions[fundam_direction_idx]:
                                    consider[perm_idx] = False

                    # For every permutation of possible cells to remove
                    causal_cell_summary = [0]*neighbour_count

                    for idx, permutation in enumerate(permutations[:consider_count]): # only goes up to the choice tier specified

                        if not consider[idx]: # Skip if not considering this
                            continue

                        total_permutations_tested += 1
                        # make copy of neighborhood
                        dummy_neighbours = neighbors_last_states[:]+[last_cell_state[:],]

                        # convert permutation to dummy neighborhood, replacing certain cells with quiescent
                        for dir_idx,direct in enumerate(permutation[1]):
                            if direct:
                                dummy_neighbours[dir_idx] = [0,]

                        # run dummy neighborhood through the rules
                        dummy_out = self.ca.evolve_rule(dummy_neighbours[-1],dummy_neighbours[:-1])

                        # If the result of dummy neighborhood is different, cells removed must have been important
                        if dummy_out != reference:

                            # Gets a colour for the line corresponding to how many cells must have been removed
                            tier = neighbour_count
                            for colour_ind,choice in enumerate(choice_tiers):
                                if idx < choice:
                                    tier = colour_ind
                                    break

                            #causal_row.append([tier*permutation_direction for permutation_direction in permutation[1]])

                            for dir_idx,direct in enumerate(permutation[1]): # For every direction in the permutation
                                if permutation[1][dir_idx]: # If the permutation removed something in this direction
                                    # If the info transfer was over a border, two lines are drawn
                                    causal_cell_summary[dir_idx] = tier
                                    # We know this one is important, so obviously anything containing it will be too, so no need to test
                                    for perm_idx,permutations_future in enumerate(permutations[idx:consider_count]):
                                        if permutations_future[0] & permutation[0] == permutation[0]:
                                            consider[perm_idx+idx] = False
                    causal_row.append(causal_cell_summary)
                causal_rack.append(causal_row)
            causal_analysis_array.append(causal_rack)

        # Putting some darker lines going from all non-quiesent_states in the initial setup
        causal_rack = []
        intro_set = [0]*(neighbour_count-1) + [1]
        for row in range(self.ca.rowC):
            causal_row = []
            for col in range(self.ca.colC):
                if self.cellarr[0][row][col] != self.ca.quiesent_state:
                    causal_row.append(intro_set)
                else: causal_row.append(None)
            causal_rack.append(causal_row)
        causal_analysis_array.append(causal_rack)

        print(f"\nPermutations tested total: {total_permutations_tested}")
        print(f"Average tests per cell: {total_permutations_tested/total_cells}")

        line_obj_array = self.causal_analysis_to_object(causal_analysis_array,directions)
        #for rack in causal_analysis_array:
        #    for row in rack:
        #        print(row)
        #    print("\n")
        # returns reversed because I parse it in reverse order initially
        return line_obj_array,list(reversed(causal_analysis_array))

    # Makes a big object with all the coloured cubes for  the ghostly overlay
    def construct_ghosts(self,rackArr):
        ghost_vertexlist = []
        ghost_colourlist = []
        ghost_vertex_count = 0
        ghost_cube_count = 0

        for rowC,row in enumerate(rackArr):
            for colC,col in enumerate(reversed(row)):
                for rackC,rack in enumerate(col):
                    if rack:
                        ghost_vertexlist += self.cube_vertices_from_point(colC,-rowC,rackC)
                        ghost_colourlist += (*self.colourdict.getColour(rack)[:3],160)*24
                        ghost_vertex_count += 24
                        ghost_cube_count += 1
        ghost_cubeobject = self.batch_ghosts.add(ghost_vertex_count, GL_QUADS, None,
            ('v3f/static', ghost_vertexlist),
            ('n3f/static',CUBE_NORMALS*ghost_cube_count),
            ('c4B/static', ghost_colourlist))

        return ghost_cubeobject

    # Function that taskes the list of locations for matches of a given pattern
    # and draws them over the top of the main evolution, in the right places
    def construct_match_blocks(self,pattern,pattern_locs,override_colour = None):

        # uses a 'base' pattern for the match, which is then duplicated and translated
        # for every instance of a match
        patternbase_vertexlist = []
        patternbase_colourlist = []
        patternbase_vertex_count = 0
        patternbase_cube_count = 0

        pattern = [pattern,]

        # Assembling the base pattern object
        for rowC,row in enumerate(pattern):
            for colC,col in enumerate(reversed(row)):
                for rackC,rack in enumerate(col):
                    if rack and rack[0] != -1:

                        # Better explained elsewhere, just makes a cube from the point
                        patternbase_vertexlist += self.cube_vertices_from_point(colC,-rowC,rackC)
                        if override_colour:
                            patternbase_colourlist += (override_colour)*24
                        else:
                            patternbase_colourlist += (*self.colourdict.getColour(rack[0])[:3],0)*24
                        patternbase_vertex_count += 24
                        patternbase_cube_count += 1

        patterns_vertexlist = []
        patternbase_colourlist *= len(pattern_locs)
        patternbase_vertex_count *= len(pattern_locs)
        patternbase_cube_count *= len(pattern_locs)

        # Placing a pattern object at every match location

        for match_location in pattern_locs:
            # Makes a copy of the vertexlist to translate
            new_vertexlist = patternbase_vertexlist[:]

            # Steps through vertexlist a cube at a time (24 verts per cube, 3 numbers per vert)
            for ind in range(0,len(new_vertexlist),24*3):

                # Works out if the current cube is outside the evo space,
                # and if the cube needs to be put back at the top of the space
                row_offset = 0
                if (new_vertexlist[ind]+((self.ca.rowC-match_location[1])-len(pattern[0]))) < 1:
                    row_offset = -self.ca.rowC
                col_offset = 0
                if new_vertexlist[ind+2]+(match_location[2]) >= self.ca.colC:
                    col_offset = self.ca.colC

                # Steps through x,y,z coords and scales them according to the location of the match
                for increment in range(0,24*3,3):
                    # x coords
                    new_vertexlist[ind+increment] += (self.ca.rowC-match_location[1])-len(pattern[0])
                    new_vertexlist[ind+increment] -= row_offset
                for increment in range(1,24*3,3):
                    # y coords
                    new_vertexlist[ind+increment] -= match_location[0]
                for increment in range(2,24*3,3):
                    #z coords
                    new_vertexlist[ind+increment] += (match_location[2])
                    new_vertexlist[ind+increment] -= col_offset

            patterns_vertexlist += new_vertexlist

        # Final object for all the matches to this pattern is created in a single vertexlist
        patterns_cubeobject = self.batchlist_highlights[self.patterns_matched].add(patternbase_vertex_count, GL_QUADS, None,
            ('v3f/static', patterns_vertexlist),
            ('n3f/static',CUBE_NORMALS*patternbase_cube_count),
            ('c4B/static', patternbase_colourlist))

        return patterns_cubeobject





    def __init__(self,ca,evol_steps,matchlist,max_patterns=5,choice_tier_depth=None,quickload=False):

        # If enabled, will only compute the globjects for certain things as they're done
        self.quickload = quickload

        # Setting up CA object, this is used to evolve the cells
        self.ca = ca
        ca_cells = self.ca.get_cells()
        self.dimensions = ca.get_dimension()
        self.evolution_steps = evol_steps

        # Setting up batches
        # These contain the objects that are drawn to the screen
        # Moving things between batches can be slow, so its faster to have a few batches
        # Which can be drawn/not drawn per frame

        # Default batch, contains a batch for every colour so it can be unloaded quickly
        self.batchlist = [pyglet.graphics.Batch() for state in range(ca.stateC)]
        # Nodraw batch to hold undrawn default objects, used in time slicing
        self.batch_nodraw = pyglet.graphics.Batch()

        # Batch for active blocks and lines respectively
        self.batch_activelens = pyglet.graphics.Batch()

        self.batch_cs_ca = pyglet.graphics.Batch()

        self.batch_lightcone = pyglet.graphics.Batch()

        self.batch_lightcone_causal = pyglet.graphics.Batch()

        self.batch_lightcone_causal_cubes = pyglet.graphics.Batch()

        self.batch_neighborhoods = pyglet.graphics.Batch()

        self.batch_ghosts = pyglet.graphics.Batch()

        # List of batches for the patterns matched, initially all blank, they stay blank until patterns supplied
        self.batchlist_highlights = [pyglet.graphics.Batch() for x in range(max_patterns)]

        self.batchlist_causal_lines = [pyglet.graphics.Batch() for x in range(self.get_neighbor_count())]

        # A separate final batch for the crosshair, the only thing always drawn
        self.batch_crosshair = pyglet.graphics.Batch()


        # These variables define the current time view slice.
        # Initiialised at 0,n-1 to represent the entire evolution of n steps
        self.start = 0
        self.end = evol_steps - 1

        # Defines the lenses; different views one can take of the system
        # Initally set so only the default view is on, with everything else as 0
        self.lens = [True,True] + [False]*9
        # Background update flag, set to 0

        # Holds the name of the state the player is currently looking at
        self.observed_state = "None"

        # sets up colour dictionary with any color aliases from the CA
        self.colourdict = colourdict(self.ca.get_colour_alias())

        # This variable defines which colours are drawn, initially all of them
        self.colourdraw_list = [True for x in range(self.ca.stateC)]

        self.linewidth = 1
        glLineWidth(1)

        # Calculates the evolution of the CA over the number of steps specified
        # Creates an array holding all the steps in the whole evolution
        rackArr = []
        # Holds the location of all active cells in the evolution
        self.active_rackArr = []
        # Steps through time, evolving the CA and recording the states of every cell
        count=0
        total =0
        for evolution in range(evol_steps):
            ca_cells = self.ca.get_cells()
            array = []

            active_array = []
            for row in range(ca.rowC):
                rowArr = []

                active_rowArr = []
                for column in range(ca.colC):
                    rowArr.append(int(ca_cells[(row,column)].state[0]))
                    total+=1
                    if int(ca_cells[(row,column)].state[0]) != 0: count += 1
                    active_rowArr.append((ca_cells[(row,column)]).is_active)

                array.append(rowArr)

                active_array.append(active_rowArr)

            rackArr.append(array)

            self.active_rackArr.append(active_array)

            self.ca.evolve()
        print(count,total)
        # This variable holds the values of the cells throughout evolution
        self.cellarr = rackArr



        # The following variables hold the actual references to objects within the batches
        # This variable holds the opengl objects representing the cubes
        self.cubelist = self.draw_from_array(rackArr)
        # This holds the active overview red blocks
        self.active_cubeobject = None #self.construct_activelens_blocks(active_rackArr)

        self.activelines_objects,self.causal_analysis_array = None,None #self.causal_analysis(choice_tier_depth)

        self.cell_specific_ca_object = None

        self.lightcone_objectlist = []

        self.lcba_object = None
        self.lcba_cube_object = None
        self.responsible_cells = 0
        self.choice_tier_depth = choice_tier_depth

        self.ghost_objects = None
        # This holds the crosshair wireframe, initially set at  0 0 0
        self.crosshair_object = self.batch_crosshair.add(24, GL_LINES, None,
            ('v3f/stream', self.wireframe_cube_from_point(0,0,0)),
            ('c4B/dynamic', (0,0,0,0)*24))
        self.crosshair_loc = [0,0,0]
        self.crosshair_loc_real = [0,0,0]

        # The following is concerned with pattern matching
        # There is an n long list of things, for n maximum patterns
        # This flag defines if the UI needs to update its match labels
        self.updated_matches = True
        # Defines a maximum number of patterns allowed to match
        self.max_patterns = max_patterns
        # Holds the number of times each pattern is matched in the cell array
        self.match_counts = [0]*self.max_patterns
        # The pointer to the top of the stack of patterns
        self.patterns_matched = -1
        # Holds the objects corresponding to patterns on the screen
        self.highlight_objects = [None]*self.max_patterns
        # The names of the patterns
        self.match_names = [""]*self.max_patterns
        # Definining if each pattern is drawn
        self.matchdraw_list = [False]*self.max_patterns

        self.causaldraw_list = [True]*self.get_neighbor_count()
        # Matching commandline supplied patterns
        for match_name,match_pattern in matchlist:
            self.add_pattern_match(match_pattern,match_name)

        # Zone selection variables
        # Stores indexes of the start of selection
        self.selection_start = [0,0,0]
        # Stores world coords of start of selection
        self.selection_start_real = [0,0,0]
        # Stores the vertexlist object for the selection wireframe
        self.selection_object = None
        # Stores the start and end indexes of the selection zone
        self.selection_region = [0,0,0,0,0,0]

        self.selection_region_real = [0,0,0,0,0,0]

        self.selection_border_mode = 0
        self.selection_reorder_flag = False

        self.selection_region_size = [0,0,0]

        self.neighborhood_count = None #self.count_unique_neighborhoods()

        # Unless loading as quick as possible, compute all the data flow information
        if not self.quickload:
            self.neighborhood_count = self.count_unique_neighborhoods()
            self.active_cubeobject = self.construct_activelens_blocks(self.active_rackArr)
            self.activelines_objects,self.causal_analysis_array = self.causal_analysis(choice_tier_depth)
            self.ghost_objects = self.construct_ghosts(rackArr)




    # Counts the number of unique neighborhoods in the evolution
    # And colours each one differently
    def count_unique_neighborhoods(self):
        if type(self.ca._neighborhood) == MooreNeighborhood:
            directions = DIRECTIONS_MOORE
            neighbour_count = 9
        elif type(self.ca._neighborhood) == VonNeumannNeighborhood:
            directions = DIRECTIONS_VN
            neighbour_count = 5
        else:
            return None

        unique_neighborhoods = 0
        neighborhoods = 0
        vertices = []
        colours = []
        # maps neighborhoods to state
        unique_neighbor_mapping = dict()

        # Doesnt want to draw completely blank neighborhoods,making it impossible to see
        # So a blank neighborhood is drawn seperately
        blank_neigbors = (0,)*neighbour_count

        for rack in range(1,self.evolution_steps):
            for row in range(self.ca.rowC):
                for col in range(self.ca.colC):

                    cell_neighbors = tuple([self.cellarr[rack-1][(row+direction[0])%self.ca.rowC][(col+direction[1])%self.ca.colC] for direction in directions])

                    if cell_neighbors == blank_neigbors:
                        continue

                    if not unique_neighbor_mapping.get(cell_neighbors):
                        unique_neighbor_mapping[cell_neighbors] = unique_neighborhoods
                        colours += self.colourdict.get_default_Colour(unique_neighborhoods)*24
                        unique_neighborhoods += 1
                    else:
                        colours += self.colourdict.get_default_Colour(unique_neighbor_mapping.get(cell_neighbors))*24#

                    neighborhoods += 1
                    vertices += self.cube_vertices_from_point(-1+self.ca.rowC-row,-rack,col)

        self.batch_neighborhoods.add(neighborhoods*24, GL_QUADS, None,
            ('v3f/static', vertices),
            ('n3f/static',CUBE_NORMALS*neighborhoods),
            ('c4B/static',colours))

        return len(unique_neighbor_mapping.keys())


    # Takes evolution array, and a pattern and returns all the locations
    # a matching pattern is found at.
    def match_2d_pattern(self, input_array, pattern_array):

        # array will hold tuples corresponding to the places in the evolution
        # where a match is found
        matches = []

        # flattens the pattern array from having cells as [1] to 1
        pattern_array_flat = []
        for row in pattern_array:
            pattern_row = []
            for col in row:
                pattern_row.append(col[0])
            pattern_array_flat.append(pattern_row)

        match_rowC = len(pattern_array_flat)
        match_colC = len(pattern_array_flat[0])


        # Flag defining if matches could possibly wrap around the borders
        flag = self.ca.edge_rule == EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS or self.ca.edge_rule == EdgeRule.IGNORE_EDGE_CELLS

        # scanning through evolution layer by layer
        for rackC,rack in enumerate(input_array):

            # These two loops will scan every cell in a row, but will stop early if the pattern could not wrap around
            # If the pattern is 10 wide and theres 8 cells left, and it cant wrap around, then it wont bother checking
            # and by extension will not find false matches
            for rowC in range(self.ca.rowC - flag * (match_rowC-1)):
                for colC in range(self.ca.colC - flag * (match_colC-1)):


                    # Assumes match found, breaks if not
                    found_match = True

                    # Loops through every cell in the pattern
                    for m_rowC in range(match_rowC):
                        for m_colC in range(match_colC):

                            # Compares every cell in the pattern to the next one in the evolution,
                            # wraps around borders if applicable
                            # Will always accept if the cell in the pattern is a '-1'
                            # On a non-match it will break and start checking elsewhere
                            if pattern_array[m_rowC][m_colC][0] != -1 and pattern_array_flat[m_rowC][m_colC] != rack[(rowC+m_rowC)%self.ca.rowC][(colC+m_colC)%self.ca.colC]:
                                found_match = False
                                break
                        if not found_match:
                            break

                    # Matches are added as a tuple to a list
                    if found_match:
                        matches.append([rackC,rowC,colC])

        return matches


    # Draws the cubes from a given array of cells
    def draw_from_array(self, drawArr):

        # This list will store the cube objects as they are created
        cubeList = []

        # Series of loops will go through the 3D array of cells
        # First dimension is time/evolutions, next are rows/columns
        for rowC,row in enumerate(drawArr):
            rowarr = []
            # This is reversed so the pattern of cells is not mirrored from its appearance in a file
            for colC,col in enumerate(reversed(row)):
                colarr = []
                for rackC,rack in enumerate(col):
                    # if rack corresponds to if the cell there is not a 0 ie, not quiescent ie, having a colour needing a cube
                    if rack:
                        cube = self.add_block(colC,-rowC,rackC,rack)
                        colarr.append(cube)
                    else:
                        # Appending a none so the dimensions of the cube array remains constant
                        colarr.append(None)
                rowarr.append(colarr)
            cubeList.append(rowarr)
        return cubeList


    # Drawing the model equates to drawing every colour batch that isnt unchecked
    # This also depends on the lens being used, to draw other batches and change bg colour
    def draw(self):

        # Light position of the central light must be re-defined every time the scene is drawn
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat*4)(0,15,0,1))


        # Draws the crosshair no matter what
        if self.lens[0]:
            self.batch_crosshair.draw()
        if self.lens[8]:
            self.batch_neighborhoods.draw()
        if self.lens[5]:
            self.batch_cs_ca.draw()
        if self.lens[4]:
            glLineWidth(self.linewidth)
            for ind,pattern in enumerate(self.causaldraw_list):
                if pattern:
                    self.batchlist_causal_lines[ind].draw()
            glLineWidth(1)
        if self.lens[7]:
            for ind,pattern in enumerate(self.matchdraw_list):
                if pattern:
                    self.batchlist_highlights[ind].draw()
        if self.lens[9]:
            glLineWidth(self.linewidth*2)
            self.batch_lightcone_causal.draw()
            glLineWidth(1)
        if self.lens[10]:
            self.batch_lightcone_causal_cubes.draw()
        if self.lens[3]:
            self.batch_activelens.draw()
        if self.lens[1]:
            for ind,colour in enumerate(self.colourdraw_list):
                if colour:
                    self.batchlist[ind].draw()
        if self.lens[6]:
            self.batch_lightcone.draw()
        if self.lens[2]:
            self.batch_ghosts.draw()



        # Checks whether a background colour update is needed
        # This flag prevents the background colour needing to be set every frame
        #if self.bg_change:
        #
        #    if self.lens[5]:
        #        glClearColor(0.605,0.72,0.75,1)
        #    elif any(self.lens[2:5]):
        #        glClearColor(0.85,0.85,0.85,1)
        #    else:
        #        glClearColor(0.2,0.25,0.5,1)
        #    self.bg_change = False

    def change_background(self,options):
        bg_colours = [
            (0.2,0.25,0.5,1), # Blue
            (0.85,0.85,0.85,1), # Beige
            (0,0,0,1), # Black
            (1,1,1,1) # White
        ]
        for opt,option in enumerate(options):
            if option:
                glClearColor(*bg_colours[opt])
                if opt == 2:
                    self.crosshair_object.colors = (255,255,255,0)*24
                else:
                    self.crosshair_object.colors = (0,0,0,0)*24


    # This function takes starts and end parameters for what to show in time,
    # then works out which racks (time slices) need updating and moves
    # cubes in those layers to the appropriate draw/no draw batch
    def set_nodraw(self,start,end):
        start_prev = self.start
        end_prev = self.end

        # Working out the list of racks needing updating
        tot_range = range(min(start_prev,start),max(end_prev,end)+1)
        noupdt_range = range(max(start_prev,start),min(end_prev,end)+1)
        updt_range = list(set(tot_range) - set(noupdt_range))

        self.start = start
        self.end = end

        self.update_nodraw(updt_range)

    # This function increments the evolution by 1 or -1, a single step through time
    # Migrating hundreds of vertexlists between batches is very slow, hence all the framework
    # for doing as few moves as possible
    def increment_nodraw(self,increase=True):

        inc = -1
        if increase:
            inc = 1

        self.start += inc
        self.end += inc

        # Clamping the values if it would go into regions not corresponding to cells
        if self.start < 0:
            self.start = 0
        if self.start > self.evolution_steps - 1:
            self.start = self.evolution_steps - 1
        if self.end > self.evolution_steps - 1:
            self.end = self.evolution_steps - 1
        if self.end < 0:
            self.end = 0

        if increase:
            self.update_nodraw([self.start-1,self.end])
        else:
            self.update_nodraw([self.start,max(self.end+1,0)])

    # This function actually carries out the updating of time slices
    # It takes a list of layers to update as a parameter, and moves cubes
    # between batches to be drawn-not drawn
    def update_nodraw(self,layerlist):
        rackList = map(self.cubelist.__getitem__, layerlist)

        # no longer *as* ugly :)
        for rackC,rack in enumerate(rackList):
            for rowC,row in enumerate(reversed(rack)):
                for colC,cube in enumerate(row):
                    if cube:
                        cube_state = self.cellarr[layerlist[rackC]][rowC][colC]

                        if layerlist[rackC] > self.end or layerlist[rackC] < self.start:
                            # migrate cube to no draw
                            self.batchlist[cube_state].migrate(cube, GL_QUADS, None, self.batch_nodraw)
                        else:
                            # migrate cube to draw
                            self.batch_nodraw.migrate(cube, GL_QUADS, None, self.batchlist[cube_state])


    # This function just takes an input from the UI about which
    # colours to draw, then updates the variable here
    def update_highlight(self,colourlist):

        updt_colour = []
        for ind,colour in enumerate(colourlist):
            if self.colourdraw_list[ind] != colour:
                updt_colour.append(ind)
                self.colourdraw_list[ind] = colour

    # Changes width of lines, helps see things better
    def increment_linewidth(self,increase):
        amount = -1
        if increase: amount = 1
        self.linewidth = max(1,self.linewidth+amount)
        #glLineWidth(self.linewidth)


    # Generates a set of lines corresponding to a minecraft-style wireframe around a central point
    # This frame is slightly larger than a unit cube, so it can be seen through
    def wireframe_cube_from_point(self,x,y,z):
        X, Y, Z = x+1.05, y+1.05, z+1.05
        x -= 0.05
        y -= 0.05
        z -= 0.05

        wireframe_points = (
            x,y,z, X,y,z, X,y,z, X,y,Z, X,y,Z, x,y,Z, x,y,Z, x,y,z,
            x,y,Z, x,Y,Z, X,y,Z, X,Y,Z, x,y,z, x,Y,z, X,y,z, X,Y,z,
            x,Y,z, X,Y,z, X,Y,z, X,Y,Z, X,Y,Z, x,Y,Z, x,Y,Z, x,Y,z)

        return wireframe_points

    def wireframe_from_point(self,x,y,z,X,Y,Z):

        if x>X: x, X = X, x
        if y>Y: y, Y = Y, y
        if z>Z: z, Z = Z, z

        X, Y, Z = X+1.05, Y+1.05, Z+1.05
        x -= 0.05
        y -= 0.05
        z -= 0.05

        wireframe_points = (
            x,y,z, X,y,z, X,y,z, X,y,Z, X,y,Z, x,y,Z, x,y,Z, x,y,z,
            x,y,Z, x,Y,Z, X,y,Z, X,Y,Z, x,y,z, x,Y,z, X,y,z, X,Y,z,
            x,Y,z, X,Y,z, X,Y,z, X,Y,Z, X,Y,Z, x,Y,Z, x,Y,Z, x,Y,z)

        return wireframe_points

    def cell_specific_ca_to_object(self,loclist):
        vertices = []
        for loc in loclist:
            vertices += self.cube_vertices_from_point(*loc)
        cs_ca_obj = self.batch_cs_ca.add(len(loclist)*24, GL_QUADS, None,
            ('v3f/static', vertices),
            ('n3f/static',CUBE_NORMALS*len(loclist)),
            ('c4B/static',(255,0,0,0)*len(loclist)*24))

        return cs_ca_obj

    # Im near the end of my project so I dont have much time to detail everything
    # But this basically does a breadth-first search on cells up and down from the selection
    def lightcone(self,region=False):
        row,rack,col = self.crosshair_loc
        queue_inital = [(rack,row,col),]
        if region:
            queue_inital = []
            x,y,z, X,Y,Z = self.selection_region

            X+=1
            Z+=1
            colrange = range(z,Z)
            rowrange = range(x,X)
            if self.selection_border_mode == 1:
                colrange = list(range(max(z,Z),self.ca.colC))+list(range(0,min(z,Z)))
            elif self.selection_border_mode == 2:
                rowrange = list(range(max(x,X),self.ca.rowC))+list(range(0,min(x,X)))
            elif self.selection_border_mode == 3:
                rowrange = list(range(x,self.ca.rowC))+list(range(0,X))
                colrange = list(range(z,self.ca.colC))+list(range(0,Z))

            for xval in rowrange:
                for zval in colrange:
                    queue_inital.append((Y,xval,zval))

        queue = queue_inital[:]
        present = len(queue)

        if not region and (row < 0 or row >= self.ca.rowC or rack < 0 or rack >= len(self.cellarr) or col < 0 or col >= self.ca.colC):
            if self.lightcone_objectlist:
                # Removes the object from the screen
                for obj in self.lightcone_objectlist:
                    obj.delete();
                # Removes the reference to it
                self.lightcone_objectlist = []

            return None

        if type(self.ca._neighborhood) == MooreNeighborhood:
            directions = DIRECTIONS_MOORE # The list of tuples corresponding to row_offset, columns_offset
            neighbour_count = 9
        elif type(self.ca._neighborhood) == VonNeumannNeighborhood:
            directions = DIRECTIONS_VN
            neighbour_count = 5
        else:
            return None
        past_colour = (255,154,0,180)
        future_colour = (0,162,255,180)
        present_colour = (0,0,0,180)

        finished = []
        past,future = -present,-present

        queue_pointer = 0
        while queue_pointer < len(queue):
            rack,row,col = queue[queue_pointer]
            if rack < 0: break
            for direction in directions:
                next_cell = (rack-1,(row+direction[0])%self.ca.rowC,(col+direction[1])%self.ca.colC)
                if next_cell not in queue[queue_pointer:]:
                    queue.append(next_cell)

            finished.append(((self.ca.rowC-row)-1,-rack,col))
            past += 1
            queue_pointer+=1


        queue = queue_inital[:]

        row,rack,col = self.crosshair_loc
        queue_pointer = 0
        while queue_pointer < len(queue):
            rack,row,col = queue[queue_pointer]
            if rack >= self.evolution_steps: break
            for direction in directions:
                next_cell = (rack+1,(row+direction[0])%self.ca.rowC,(col+direction[1])%self.ca.colC)
                if next_cell not in queue[queue_pointer:]:
                    queue.append(next_cell)

            finished.append(((self.ca.rowC-row)-1,-rack,col))
            future += 1
            queue_pointer+=1

        finished = list(set(finished))
        # This makes it so cells are sorted along all three axes, so it looks correct with transparency from one direction
        finished.sort(key = lambda x: (x[1],x[0],x[2]),reverse=True)


        vertices = []
        for loc in finished:
            vertices += self.cube_vertices_from_point(*loc,0.1)

        colours = past_colour*past*24 + present_colour*present*24 + future_colour*future*24

        self.lightcone_objectlist.append(self.batch_lightcone.add((past+future+present)*24, GL_QUADS, None,
            ('v3f/static', vertices),
            ('n3f/static',CUBE_NORMALS*(past+future+present)),
            ('c4B/static',colours)))

        self.clear_selection()

    # Tests every cell in the past lightcone to a certain depth, if removing them changes the focus cell,
    # then it is highlighted as being important
    def lightcone_based_causal_analysis(self,depth=5):

        row,rack,col = self.crosshair_loc
        self.responsible_cells = 0
        if self.lcba_object:
            self.lcba_object.delete();
            self.lcba_object = None
        if self.lcba_cube_object:
            self.lcba_cube_object.delete();
            self.lcba_cube_object = None

        if row < 0 or row >= self.ca.rowC or rack < 0 or rack >= len(self.cellarr) or col < 0 or col >= self.ca.colC:
            return None


        backstop = max(0,rack-depth)

        vertices_lines = []
        colours_lines = []
        vertices_cubes = self.cube_vertices_from_point(-1 + self.ca.rowC - row,-rack,col)

        focus = [self.cellarr[rack][row][col],]
        #print("FOCUS:",focus)
        relevant_racks = self.cellarr[backstop:rack]
        #print(f"relevant racks {relevant_racks}")

        for rackC,rack_array in enumerate(reversed(relevant_racks), 1):

            focus_coords = [rackC,rackC]
            if 2*rackC + 1 > self.ca.rowC:
                relevant_rows_idx = list(range(self.ca.rowC))
                focus_coords[0] = row
            else:
                relevant_rows_idx = list(map(lambda x: (row+x)%(self.ca.rowC), [i for i in range(-rackC,rackC+1)]))[:self.ca.rowC]
            if 2*rackC + 1 > self.ca.colC:
                relevant_cols_idx = list(range(self.ca.colC))
                focus_coords[1] = col
            else:
                relevant_cols_idx = list(map(lambda x: (col+x)%(self.ca.colC), [i for i in range(-rackC,rackC+1)]))[:self.ca.colC]

            eden = []
            #relevant_rows_idx = list(map(lambda x: (row+x)%(self.ca.rowC), [i for i in range(-rackC,rackC+1)]))[:self.ca.rowC]
            #relevant_cols_idx = list(map(lambda x: (col+x)%(self.ca.colC), [i for i in range(-rackC,rackC+1)]))[:self.ca.colC]
            #print(f"relevant rows: {relevant_rows_idx}")
            #print(f"POTENTIAL relative rows {list(map(lambda x: (row+x)%(self.ca.rowC), [i for i in range(-rackC,rackC+1)]))}")
            #print(f"relevant cols: {relevant_cols_idx}")
            #print(f"focus point at {focus_coords} in eden")
            relevant_rows = np.array(rack_array)[relevant_rows_idx]

            for relrow in relevant_rows:
                relevant_cols = np.reshape(relrow[relevant_cols_idx],(len(relrow[relevant_cols_idx]),1)).tolist()
                eden += [relevant_cols,]

            #print("\nEDEN CREATED\n")
            #for gorp in eden:
            #    print(gorp)
            #print("\n\n")
            edensize = (len(eden),len(eden[0]))

            for row_offset in range(-rackC,rackC+1):
                for col_offset in range(-rackC,rackC+1):

                    dummy_eden = copy.deepcopy(eden)
                    if rackC+row_offset > edensize[0]-1 or rackC+row_offset < 0 or rackC+col_offset > edensize[1]-1 or rackC+col_offset < 0: continue
                    if dummy_eden[rackC+row_offset][rackC+col_offset] == [0,]: continue

                    dummy_eden[rackC+row_offset][rackC+col_offset] = [0,]
                    #print("DUMMY EDEN\n")
                    #for gopre in dummy_eden:
                    #    print(gopre)
                    #print("\n")

                    ca = CA_DICT[self.ca.name](dummy_eden)
                    #if len(relevant_cols_idx) != self.ca.colC or len(relevant_rows_idx) != self.ca.rowC:
                    #    ca.edge_rule = EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS
                    # THIS NEVER NEEDS TO HAPPEN WRITE WHY IN REPORT

                    for step in range(rackC):
                        ca.evolve()

                    new_focus = ca.get_cells()[tuple(focus_coords)].state
                    #print("OLD FOCUS",focus)
                    #print("NEW FOCUS",new_focus,end="")
                    # see if different
                    if new_focus != focus:
                        #print(" DIFFERENT",end="")
                        #print(f"vertices += [{self.ca.rowC}-{row},-{rack},{col}]")
                        #print(f"vertices += [{self.ca.rowC}-({row}+{row_offset}),{rackC}-{rack},{col}+{col_offset}]")
                        vertices_lines += [self.ca.rowC-row,-rack,col]
                        vertices_lines += [
                            self.ca.rowC - ((-focus_coords[0] + rackC + row_offset + row)%self.ca.rowC),
                            rackC-rack + (0.25*(depth-rackC)/depth),
                            (-focus_coords[1]+rackC + col_offset + col)%self.ca.colC]

                        vertices_cubes += self.cube_vertices_from_point(
                            -1 + self.ca.rowC - ((-focus_coords[0] + rackC + row_offset + row)%self.ca.rowC),
                            rackC-rack,
                            (-focus_coords[1]+rackC + col_offset + col)%self.ca.colC)

                        if rackC >= len(HIGHLIGHT_COLOURS):
                            colours_lines += (255,255,255,0)*2
                        else:
                            colours_lines += HIGHLIGHT_COLOURS[rackC-1]*2
                        #vertices += [self.ca.rowC - ((-focus_coords[0] + rackC + row_offset + row)%self.ca.rowC),rackC-rack,(focus_coords[1]-rackC + col_offset + col)%self.ca.colC]
                        #print(f"{self.ca.rowC} - (({rackC}+ {row_offset} + {row})%{self.ca.rowC})")

                    #print("")
        #print(f"{len(vertices)//6} cells directly responsible within lightcone of depth {depth}")
        self.responsible_cells = len(vertices_lines)//6

        for ind in range(0,len(vertices_lines),3):
            vertices_lines[ind] -= 0.5
            vertices_lines[ind+1] += 0.5
            vertices_lines[ind+2] += 0.5

        self.lcba_object = self.batch_lightcone_causal.add(len(vertices_lines)//3, GL_LINES, None,
            ('v3f/static', vertices_lines),
            ('c4B/static', colours_lines))

        self.lcba_cube_object = self.batch_lightcone_causal_cubes.add(len(vertices_cubes)//3, GL_QUADS, None,
            ('v3f/static', vertices_cubes),
            ('n3f/static', CUBE_NORMALS*(len(vertices_cubes)//72)),
            ('c4B/static', (255,0,255,0)*(len(vertices_cubes)//3)))


    def cell_specific_causal_analysis(self):
        row,rack,col = self.crosshair_loc

        # In the case of quick load
        if not self.causal_analysis_array:
            return
        if self.cell_specific_ca_object:
            # Removes the object from the screen
            self.cell_specific_ca_object.delete();
            # Removes the reference to it
            self.cell_specific_ca_object = None

        if row < 0 or row >= self.ca.rowC or rack < 0 or rack >= len(self.cellarr) or col < 0 or col >= self.ca.colC:
            return None


        # get direction set needed
        if type(self.ca._neighborhood) == MooreNeighborhood:
            directions = DIRECTIONS_MOORE # The list of tuples corresponding to row_offset, columns_offset
            neighbour_count = 9
        elif type(self.ca._neighborhood) == VonNeumannNeighborhood:
            directions = DIRECTIONS_VN
            neighbour_count = 5
        else:
            return None
        # start at
        finished = []
        queue = [(rack,row,col),]
        queue_pointer = 0


        while queue_pointer < len(queue):
            if queue_pointer > 100000: return
            rack,row,col = queue[queue_pointer]
            current_cell_dir = self.causal_analysis_array[rack][row][col]
            if current_cell_dir and rack > 0:
                for dir_idx,direction in enumerate(current_cell_dir):
                    if direction:
                        next_cell = (rack-1,(row+directions[dir_idx][0])%self.ca.rowC,(col+directions[dir_idx][1])%self.ca.colC)
                        if next_cell not in queue[queue_pointer:]:
                            queue.append(next_cell)

            finished.append(((self.ca.rowC-row)-1,-rack,col))
            queue_pointer+=1

        finished = list(set(finished))

        self.cell_specific_ca_object = self.cell_specific_ca_to_object(finished)

    # Updates where the crosshair is drawn on the screen depending on the x/y/z value
    # which is solved in the windowModel.py file
    def update_crosshair(self,x,y,z):

        # These three conditions round values very close to integer values
        # This is needed because with the small values involved, you sometimes get a block at y=1
        # wth a value of 0.995 or 1.0005, so rounding very close values means you should get the right observed cell
        # This comes at the cost of losing some accuracy elsewhere, but this makes definite cases more reliable
        if abs(round(y) - y) < 0.1:
            y = round(y)
        if abs(round(x) - x) < 0.1:
            y = round(y)
        if abs(round(y) - y) < 0.1:
            y = round(y)

        # Floor functions effectively turn the exact value of cursor position and snap it to a consistent corner of a block
        # This should mean looking at any point on a block will yield the same xyz values
        x = math.floor(x)
        y = math.floor(y)
        z = math.floor(z)

        self.crosshair_loc_real = [x,y,z]

        # Creates the points for the wireframe based on cell coordinates
        self.crosshair_object.vertices = self.wireframe_cube_from_point(x,y,z)

        # Converts world coordinates into indexes for the cell array
        x = self.ca.rowC - (x+1)
        y = abs(y)

        # Saves the location of the crosshair for use later
        self.crosshair_loc = [x,y,z]

        # If the observered cell is in the evolution array, set the observed state parameter
        # Otherwise set it as none
        # This is needed so it doesnt try and index out of bounds of the cell array
        if x >= 0 and x < self.ca.rowC and y >= 0 and y < len(self.cellarr) and z >= 0 and z < self.ca.colC:
            observed_state = str(self.cellarr[y][x][z]) + ": "+ str(self.ca.statenames.get(str(self.cellarr[y][x][z])))
            if observed_state:
                self.observed_state = observed_state
            else:
                self.observed_state = str(self.cellarr[y][x][z])
        else:
            self.observed_state = "None"

    # Attempts to match a pattern based on a cell where the user is looking
    # Takes a parameter of windowsize, the number of neighborhood steps it will radiate out
    # from the centre cell
    def add_pattern_from_crosshair(self,windowsize):
        x,y,z = self.crosshair_loc

        # Exits if max patterns reached
        if self.patterns_matched >= self.max_patterns - 1:
            return None

        # Exits if not looking within cell array borders
        if x < 0 or x >= self.ca.rowC or y < 0 or y >= len(self.cellarr) or z < 0 or z >= self.ca.colC:
            return None

        # Assembling the array of cells corresponding to the neighborhood around the cell
        # Where the user is looking
        # This will assemble a square pattern
        pattern = []
        for x_offset in range(-windowsize,windowsize+1):
            pattern_row = []
            for z_offset in range(-windowsize,windowsize+1):
                pattern_row.append([self.cellarr[y][(x+x_offset)%self.ca.rowC][(z+z_offset)%self.ca.colC],])
            pattern.append(pattern_row)

        # If the CA uses VN neighborhood, then some of the cells in a square pattern
        # arent actually neighbours within equal numbers of steps (in the corners)
        # This filters those out, replacing them with wildcard matching operators (-1)
        if type(self.ca._neighborhood) == VonNeumannNeighborhood:
            for row in range(windowsize*2+1):
                for col in range(windowsize*2+1):
                    if row+col < windowsize or row+col > 3*windowsize or row-col > windowsize or col-row > windowsize:
                        # replace this with universal matcher later
                        pattern[row][col] = [-1,]

        # Makes a simple name for a pattern based on where it was created from
        pattern_name = f"{self.cellarr[y][x][z]} @ ({x},{y},{z})"

        # Attempts to match the created pattern
        self.add_pattern_match(pattern,match_name=pattern_name)

    # Does the high level work of setting up a match in the system, like adding into batches
    def add_pattern_match(self,match_pattern,match_name="None"):

        # Will exit if number of patterns at max
        if self.patterns_matched >= self.max_patterns - 1:
            return None

        self.patterns_matched += 1
        # Update match flag set to true to trigger UI update
        self.updated_matches = True
        # Sets toggle draw to true for new pattern
        self.matchdraw_list[self.patterns_matched] = True
        # Sets name for new pattern
        self.match_names[self.patterns_matched] = match_name

        # Gets the locations where matches occur for this pattern
        match_locs = self.match_2d_pattern(self.cellarr,match_pattern)
        # Gets number of places it matches
        self.match_counts[self.patterns_matched] = len(match_locs)
        # If there are matches, will add the shapes to the batches with construct_match_blocks
        # and stores the objects in a list of objects
        if match_locs:
            self.highlight_objects[self.patterns_matched] = self.construct_match_blocks(match_pattern,match_locs,override_colour = HIGHLIGHT_COLOURS[self.patterns_matched])

    # Removes the last pattern matches, effectively does the inverse of add_pattern_match
    def remove_last_pattern(self):
        if self.patterns_matched < 0:
            return None

        self.updated_matches = True
        # If there was an associated object for this match, then it is deleted
        if self.highlight_objects[self.patterns_matched]:
            self.highlight_objects[self.patterns_matched].delete()
            self.highlight_objects[self.patterns_matched] = None
        self.matchdraw_list[self.patterns_matched] = True
        self.match_counts[self.patterns_matched] = 0
        self.match_names[self.patterns_matched] = ""
        self.patterns_matched -= 1

    # Adds a pattern from a currently selected region
    def add_pattern_from_selection(self,pattern_window_size=0):
        # Start and end coords of the current region
        x,y,z, X,Y,Z = self.selection_region
        X += 1+pattern_window_size
        Y += 1
        Z += 1+pattern_window_size

        x -= pattern_window_size
        z -= pattern_window_size

        #print(f"self.cellarr[{y}:{Y}][{x}:{X}][{z}:{Z}]")
        # If there is a difference in y values > 1, then more than one layer is selected,
        # This currently is not implemented
        if Y-y > 1:
            print("Three-dimensional patterns currently not supported, aborting")
            return

        # Gets the right rack
        racks = self.cellarr[y]
        # This messy line gets the right x and z slices of the rack, and puts them in singleton list format [x,] because thats what
        # the pattern loader wants to see
        #pattern = [[[state,] for state in row[z:Z]] for row in racks[x:X]]
        #print(x,y,z,X,Y,Z)


        colrange = range(z,Z)
        rowrange = range(x,X)
        if self.selection_border_mode == 1:
            colrange = list(range(max(z,Z),self.ca.colC))+list(range(0,min(z,Z)))
        elif self.selection_border_mode == 2:
            rowrange = list(range(max(x,X),self.ca.rowC))+list(range(0,min(x,X)))
        elif self.selection_border_mode == 3:
            rowrange = list(range(x,self.ca.rowC))+list(range(0,X))
            colrange = list(range(z,self.ca.colC))+list(range(0,Z))

        pattern = []
        for row in rowrange:
            pattern_row = []
            for col in colrange:
                pattern_row.append([self.cellarr[y][(row)%self.ca.rowC][(col)%self.ca.colC],])

            pattern.append(pattern_row)

        pattern_width = len(pattern[0])-2*pattern_window_size
        pattern_height = len(pattern)-2*pattern_window_size

        if type(self.ca._neighborhood) == VonNeumannNeighborhood:
            for row in range(len(pattern)):
                for col in range(len(pattern[0])):
                    if (row + col < pattern_window_size or #hmmmmmmm idk
                        row + col >= 3*pattern_window_size+pattern_width+pattern_height-1 or
                        row-col >= pattern_height+pattern_window_size or
                        col-row >= pattern_width+pattern_window_size):
                        # replace this with universal matcher later
                        pattern[row][col] = [-1,]

        pattern_name = f"({x},{y},{z})-({X},{Y},{Z})"
        if pattern_window_size != 0:
            pattern_name+="+"
        # Sends the extracted pattern to be matched
        self.add_pattern_match(pattern,match_name=pattern_name)

        # Clears selection
        self.clear_selection()


    # Starts the zone selection process, returns True if successful
    def start_selecting_zone(self):
        # Gets current position of crosshair
        x,y,z = self.crosshair_loc
        # Checks if crosshair in cell array range
        if x >= 0 and x < self.ca.rowC and y >= 0 and y < len(self.cellarr) and z >= 0 and z < self.ca.colC:

            # Defines the starting point indexes as the corsshair loc indexes
            self.selection_start = self.crosshair_loc[:]
            # Defines the "real" start as the world coordinate of the crosshair
            self.selection_start_real = self.crosshair_loc_real[:]

            if self.selection_object:
                self.selection_object.delete()
                self.selection_object = None
            self.selection_object = self.batch_crosshair.add(24, GL_LINES, None,
                ('v3f', self.wireframe_cube_from_point(*self.selection_start_real)),
                ('c4B', (200,255,200,0)*24))

            return True
        else:
            return False

    # Finalises zone selection, returns True if successful
    def finish_selecting_zone(self):
        # Gets current position of crosshair
        x,y,z = self.crosshair_loc
        # Checks if crosshair in cell array range
        if x >= 0 and x < self.ca.rowC and y >= 0 and y < len(self.cellarr) and z >= 0 and z < self.ca.colC:

            # If there is an existing object (like the single cube wireframe), delete
            if self.selection_object:
                self.selection_object.delete()
                self.selection_object = None

            # Adds a wireframe corrsponding to the entire selection region
            # Uses the "real" coords for the crosshair ie not the array indexes
            self.selection_object = self.batch_crosshair.add(24, GL_LINES, None,
                ('v3f', self.wireframe_from_point(*self.selection_start_real,*self.crosshair_loc_real)),
                ('c4B', (200,255,200,0)*24))

            # Gets the indexes corresponding to the zone selected
            X,Y,Z = self.selection_start
            # Orders them so the patterns are a consistent orientation, no matter start/end
            self.selection_region = [min(x,X),min(y,Y),min(z,Z),max(x,X),max(y,Y),max(z,Z)]
            if (x<X and z>Z) or (X<x and Z>z):
                self.selection_reorder_flag = True
            else:
                self.selection_reorder_flag = False
            self.selection_region_real = [
                min(self.selection_start_real[0],self.crosshair_loc_real[0]),
                min(self.selection_start_real[1],self.crosshair_loc_real[1]),
                min(self.selection_start_real[2],self.crosshair_loc_real[2]),
                max(self.selection_start_real[0],self.crosshair_loc_real[0]),
                max(self.selection_start_real[1],self.crosshair_loc_real[1]),
                max(self.selection_start_real[2],self.crosshair_loc_real[2])]

            if self.selection_border_mode != 0:
                temp = self.selection_border_mode
                self.selection_border_mode = 0
                for dummy_border_mode in range(temp):
                    self.flip_selection_borders()


            self.update_selection_size()
            return True
        else:
            return False

    def flip_selection_borders(self):

        x,y,z,X,Y,Z = self.selection_region
        xr,yr,zr,Xr,Yr,Zr = self.selection_region_real

        self.selection_border_mode = (1 + self.selection_border_mode) % 4

        if self.selection_object:
            self.selection_object.delete()
            self.selection_object = None

        if self.selection_border_mode == 0: #Flip from last option to first
            self.selection_region = [X,y,Z,x,Y,z]
            self.selection_region_real = [Xr,yr,Zr,xr,Yr,zr]
            self.selection_object = self.batch_crosshair.add(24, GL_LINES, None,
                ('v3f', self.wireframe_from_point(*self.selection_region_real)),
                ('c4B', (200,255,200,0)*24))
        elif self.selection_border_mode == 1:
            self.selection_region = [x,y,Z,X,Y,z]
            self.selection_region_real = [xr,yr,Zr,Xr,Yr,zr]
            self.selection_object = self.batch_crosshair.add(48, GL_LINES, None,
                ('v3f', self.wireframe_from_point(xr,yr,Zr,Xr,Yr,self.ca.colC-1)+self.wireframe_from_point(xr,yr,0,Xr,Yr,zr)),
                ('c4B', (200,255,200,0)*48))
        elif self.selection_border_mode == 2:
            self.selection_region = [X,y,Z,x,Y,z]
            self.selection_region_real = [Xr,yr,Zr,xr,Yr,zr]
            self.selection_object = self.batch_crosshair.add(48, GL_LINES, None,
                ('v3f', self.wireframe_from_point(0,yr,Zr,xr,Yr,zr)+self.wireframe_from_point(Xr,yr,Zr,self.ca.rowC-1,Yr,zr)),
                ('c4B', (200,255,200,0)*48))
        elif self.selection_border_mode == 3:
            self.selection_region = [x,y,Z,X,Y,z]
            self.selection_region_real = [xr,yr,Zr,Xr,Yr,zr]
            if self.selection_reorder_flag:
                vline = ('v3f', self.wireframe_from_point(Xr,yr,0,0,Yr,zr)+self.wireframe_from_point(self.ca.rowC-1,yr,Zr,xr,Yr,self.ca.colC-1)+self.wireframe_from_point(Xr,yr,Zr,0,Yr,self.ca.colC-1)+self.wireframe_from_point(self.ca.rowC-1,yr,0,xr,Yr,zr))
            else:
                vline = ('v3f', self.wireframe_from_point(self.ca.rowC-1,yr,0,xr,Yr,zr)+self.wireframe_from_point(Xr,yr,Zr,0,Yr,self.ca.colC-1)+self.wireframe_from_point(xr,yr,Zr,self.ca.rowC-1,Yr,self.ca.colC-1)+self.wireframe_from_point(0,yr,0,Xr,Yr,zr))
            self.selection_object = self.batch_crosshair.add(96, GL_LINES, None,
                vline,
                ('c4B', (200,255,200,0)*96))
        self.update_selection_size()

    def update_selection_size(self):
        x,y,z,X,Y,Z = self.selection_region

        self.selection_region_size = []
        if self.selection_border_mode == 0:
            self.selection_region_size = [1+X-x,1+Y-y,1+Z-z]
        elif self.selection_border_mode == 1:
            if z==Z:Z-=1
            self.selection_region_size = [1+X-x,1+Y-y,1+Z+self.ca.colC-z]
        elif self.selection_border_mode == 2:
            if x==X:X-=1
            self.selection_region_size = [1+X+self.ca.rowC-x,1+Y-y,1+Z-z]
        elif self.selection_border_mode == 3:
            if z==Z:Z-=1
            if x==X:X-=1
            self.selection_region_size = [1+X+self.ca.rowC-x,1+Y-y,1+Z+self.ca.colC-z]

    # Clears the selection, restarting zone selection process and removing objects associated
    def clear_selection(self):
        if self.selection_object:
            # Removes the object from the screen
            self.selection_object.delete();
            # Removes the reference to it
            self.selection_object = None
        self.selection_region = [0,0,0,0,0,0]
        self.selection_region_real = [0,0,0,0,0,0]
        self.selection_start = [0,0,0]
        self.selection_border_mode = 0
        self.selection_region_size = [0,0,0]

    def move_crosshair(self,directions):
        self.crosshair_loc_real[0]+=directions[0]
        self.crosshair_loc_real[1]+=directions[1]
        self.crosshair_loc_real[2]+=directions[2]
        self.crosshair_loc[0]-=directions[0]
        self.crosshair_loc[1]-=directions[1]
        self.crosshair_loc[2]+=directions[2]
        self.crosshair_object.vertices = self.wireframe_cube_from_point(*self.crosshair_loc_real)

    # Updates the draw flags for each pattern, called from the UI through checkboxes
    def update_match_highlight(self,matchlist):
        for ind,pattern in enumerate(matchlist):
            if self.matchdraw_list[ind] != pattern:
                self.matchdraw_list[ind] = pattern

    def update_causal_draw(self,drawlist):
        for ind,pattern in enumerate(drawlist):
            if self.causaldraw_list[ind] != pattern:
                self.causaldraw_list[ind] = pattern

    def change_lens(self,lens):
        if self.quickload:
            if lens[2] and not self.ghost_objects:
                self.ghost_objects = self.construct_ghosts(self.cellarr)
            if lens[3] and not self.active_cubeobject:
                self.active_cubeobject = self.construct_activelens_blocks(self.active_rackArr)
            if (lens[4] or lens[5]) and not self.activelines_objects:
                self.activelines_objects,self.causal_analysis_array = self.causal_analysis(self.choice_tier_depth)
            if lens[8] and not self.neighborhood_count:
                self.neighborhood_count = self.count_unique_neighborhoods()

        self.lens = lens

    def get_neighbor_count(self):
        if type(self.ca._neighborhood) == MooreNeighborhood:
            return 9
        elif type(self.ca._neighborhood) == VonNeumannNeighborhood:
            return 5
        else:
            return None
