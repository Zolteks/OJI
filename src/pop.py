import pyxel
from tools import Tools
import tweening

class Pop:

    def __init__(self, x, y, text, tweeningFunc="easeOutElastic", dx=10, dy=10, tx=30, ty=30, life=40):
        self.life = life
        self.x = x
        self.y = y
        self.w = len(text) / 2 * 4
        self.h = 5
        self.initX, self.initY = Tools.center(x, y, self.w, self.h, self.w, self.h,)
        self.text = text
        self.xTween = tweening.TimedValue(dx, tx, f=tweeningFunc)
        self.yTween = tweening.TimedValue(dy, ty, f=tweeningFunc)

    def update(self):
        self.life -= 1
        self.x = self.initX + self.xTween.value()
        self.y = self.initY - self.yTween.value()

    def draw(self):
        color = 10
        if self.life < 30:
            color = 9
        if self.life < 15:
            color = 4
        pyxel.text(self.x, self.y, self.text, color)
