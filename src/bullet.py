import pyxel

class Bullet:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= 3

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 4, 10)
