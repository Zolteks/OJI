import pyxel
import tweening

class Missile:

    def __init__(self, x, y, g):
        self.x = x
        self.y = y
        self.game = g
        self.speed = tweening.TimedValue(7,45,f"easeInBack")
    
    def update(self):
        self.y -= self.speed.value()
    
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 6, 20, 4, 8, 0)