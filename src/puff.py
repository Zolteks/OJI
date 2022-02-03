import pyxel
from tools import Tools

class Puff:

    def __init__(self, x, y, w, h):
        self.life = 30
        self.w = 16
        self.h = 16
        self.x, self.y = Tools.center(x, y, w, h, self.w, self.h,)
        self.vx = 1
        self.vy = 2

    def update(self):
        self.life -= 1
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.9
        self.vy *= 0.9

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 128, 0, 16, 16, 0)
