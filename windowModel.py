import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from player import Player

import copy

import math

################################################################################
### Window model, contains the 3D view of the model and allows exploration #####
################################################################################

class WindowModel(pyglet.window.Window):

    # Pushes the openGL transformation matrix, add transformations to make the world
    # move around the camera to simulate first person movement
    def push(self,pos,rot):
        glPushMatrix()
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # Sets 3D view
    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    # Describes mouse lock, player can only rotate the camera with the mouse when
    # the mouse is not locked (using e key by default)
    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)


    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self, model, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.model = model
        self.player = player
        self.steplock = False

        self.mouse_connect = True

        self.zdist = (GLfloat * 1)(0)

        self.pattern_window_size = 0

        self.causal_depth = 3

        self.selecting_zone = False
        self.selection_finished = False

        self.observed_object = [0,0,0]




    # Sends mouse move data to player class, if in 3d view
    def on_mouse_motion(self,x,y,dx,dy):

        if self.mouse_lock:
            self.player.mouse_motion(dx,dy)

            if not self.mouse_connect: return

            # Moves the camera according to change in x and y from mouse movement

            # Reads the value of the normalised depth buffer at the pixel in the middle of the screen
            self.context.set_current()
            glReadPixels(int(self.width/2), int(self.height/2), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, self.zdist)

            # Uses a method from here
            # https://stackoverflow.com/questions/51315865/glreadpixels-how-to-get-actual-depth-instead-of-normalized-values
            # To work out the actual distance by using near and far viewing planes
            zNorm = 2 * self.zdist[0] - 1
            zView = 2 * 0.05 * 1000 / ((1000 - 0.05) * zNorm - 0.05 - 1000)

            # Works out the y value of the observed pixel
            object_y = zView * math.sin(math.radians(-(self.player.rot[0])))
            # Works out the other side of this triangle, corresponding to (x^2 + z^2)**0.5
            r = zView * math.cos(math.radians(abs(self.player.rot[0])))

            # Solves for x and z given the y value and the other viewing angle
            object_x = r * math.sin(math.radians(self.player.rot[1])) + self.player.pos[0]
            object_z = r * math.cos(math.radians(self.player.rot[1])) + self.player.pos[2]

            # Subtracts or adds the player height depending on if theyre above or below the target
            # This is necessary because the angle varies between -90 and 90 rather than 0 and 180
            object_y += self.player.pos[1]-1

            # Unused, figure out which direction the player is looking in
            #is_looking_posx = math.cos(math.radians(self.player.rot[1])) < 0
            #is_looking_posz = math.sin(math.radians(self.player.rot[1])) < 0

            # Passes the location of the observed pixel to the model where a selection box will be drawn


            self.model.update_crosshair(object_x,object_y,object_z)





    # Non-movement controls
    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock


        # Next two commands step through the evolution
        # If in 2d view, will also increment the users position accordingly
        elif KEY == key.UP:
            self.model.increment_nodraw(increase=True)
            if self.steplock:
                self.player.pos[1] -= 1
        elif KEY == key.DOWN:
            self.model.increment_nodraw(increase=False)
            if self.steplock:
                self.player.pos[1] += 1

        elif KEY == key.LEFT:
            self.context.set_current()
            self.model.increment_linewidth(increase=False)
        elif KEY == key.RIGHT:
            self.context.set_current()
            self.model.increment_linewidth(increase=True)

        # Add pattern from crosshair or zone, will prioritise zone if there is one
        elif KEY == key.ENTER:
            if self.selection_finished:
                expand = self.pattern_window_size
                self.model.add_pattern_from_selection(pattern_window_size = expand)
                self.selection_finished = False
                self.selecting_zone = False
            else:
                self.model.add_pattern_from_crosshair(windowsize = self.pattern_window_size)

        elif KEY == key.V:
            self.model.cell_specific_causal_analysis()

        elif any(KEY == k for k in [key.BRACKETRIGHT,key.BRACKETLEFT,key.APOSTROPHE,key.SEMICOLON,key.SLASH,key.HASH,key.SLASH]):
            dirs = [int(KEY==key.BRACKETLEFT)-int(KEY==key.APOSTROPHE),int(KEY==key.BRACKETRIGHT)-int(KEY==key.SLASH),int(KEY==key.HASH)-int(KEY==key.SEMICOLON)]
            self.model.move_crosshair(dirs)

        elif KEY == key.B:
            if self.selection_finished:
                self.model.lightcone(region=True)
                self.selection_finished = False
                self.selecting_zone = False
            else:
                self.model.lightcone(region=False)

        elif KEY == key.N:
            self.model.lightcone_based_causal_analysis(self.causal_depth)


        # Remove last pattern, or cancel selection, prioritise cancel selection
        elif KEY == key.BACKSPACE:
            if self.selection_finished or self.selecting_zone:
                self.model.clear_selection()
                self.selection_finished = False
                self.selecting_zone = False
            else:
                self.model.remove_last_pattern()

        elif KEY == key.H:
            if not self.selecting_zone:
                self.selection_finished = False
                # If they successfully start selecting a zone, toggle param
                if self.model.start_selecting_zone():
                    self.selecting_zone = True
            # If they are selecting a zone
            else:
                # if the selection finishes ok:
                if self.model.finish_selecting_zone():
                    self.selection_finished = True
        elif KEY == key.J:
            if self.selection_finished:
                self.model.flip_selection_borders()


    def set_playerpos(self,pos):
        self.player.pos = pos

    def set_playerrot(self,rot):
        self.player.rot = rot
        self.player.mouse_motion(0,0) # Needed to update view

    # Asks the player class to check for held down movement keys
    def update(self, dt):
        self.player.update(dt, self.keys)

    def change_background(self,options):
        self.context.set_current()
        self.model.change_background(options)

    def save_pos_orient(self):
        self.saved_position = [self.player.pos[:],self.player.rot[:]]

    def load_pos_orient(self):
        self.player.pos,self.player.rot = copy.deepcopy(self.saved_position)

    # On draw, will clear scene and then rotate/translate the world, redraw scene
    def on_draw(self):
        self.clear()
        self.set3d()


        self.push(self.player.pos,self.player.rot)
        self.model.draw()
        glPopMatrix()
