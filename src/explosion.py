import pyxel
from tools import Tools

class Explosion:

    def __init__(self, x, y, w, h):
        self.life = 30
        self.w = 16
        self.h = 16
        self.x, self.y = Tools.center(x, y, w, h, self.w, self.h,)
        self.v = 1

    def update(self):
        self.life -= 1
        self.y += self.v
        self.v *= 0.9

    def draw(self):
        if self.life > 20:
            pyxel.blt(self.x - 2, self.y - 2, 1, 80, 0, 16, 16, 0)
        elif self.life > 10:
            pyxel.blt(self.x - 2, self.y - 2, 1, 96, 0, 16, 16, 0)
        elif self.life > 0:
            pyxel.blt(self.x - 2, self.y - 2, 1, 112, 0, 16, 16, 0)
