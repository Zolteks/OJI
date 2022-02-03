import pyxel
import tweening

class Bonus:

    def __init__(self, game, bonus="stimPack"):
        self.g = game
        self.y = 0
        self.bonus = bonus
        self.stimX = tweening.TimedValue(116, offset=0, duration=120, f="linear", bounce=True)
        self.stimY = tweening.TimedValue(10, duration=30, f="easeInOutBack", bounce=True)
        self.w = 12
        self.h = 8

    def update(self):
        self.x = self.stimX.value()
        self.y += 0.2

    def collision(self, rect):
        return self.g.rect_overlap(self.x, rect.x, self.y + self.stimY.value(), rect.y, self.w, rect.w, self.h, rect.h)

    def draw(self):
        if self.bonus == "stimPack":
            pyxel.blt(self.x, self.y + self.stimY.value(), 1, 2, 36, 12, 8, 0)