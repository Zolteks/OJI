import pyxel

class Danger:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = 8
        self.h = 8

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pyxel.blt(
            self.x-self.w/2,
            self.y-self.h/2,
            1,
            96, 
            48, 
            self.w, 
            self.h, 
            0)

