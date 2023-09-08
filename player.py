import math
from pyglet.window import key

################################################################################
### Player class allows for first-person flying around the scene ###############
################################################################################

class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    # Controls mouse motion, updates rot variable based on change in mouse
    # x and y values
    def mouse_motion(self, dx, dy):
        dx/= 8
        dy/= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        # Preventing player looking more than straight up or down
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    # Updates the position of the user based on currently pressed keys
    def update(self,dt,keys):
        # Params for controlling speed
        sens = 0.4
        s = dt*10
        # Adjusting direction so W will move player in direction facing, not just positive x
        rotY = -self.rot[1]/180*math.pi
        dx, dz = math.sin(rotY), math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE]:
            self.pos[1] += s*sens * 3
        if keys[key.LCTRL]:
            self.pos[1] -= s*sens * 3
