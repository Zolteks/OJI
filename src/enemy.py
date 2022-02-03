import pyxel

class Enemy:

    def __init__(self, x, y, g):
        self.x = x
        self.y = y
        self.life = 1
        self.size = "small"
        self.w = Enemy.ship[self.size]["w"]
        self.h = Enemy.ship[self.size]["h"]
        self.game = g
        self.points = 100

    def update(self):
        self.y += 1

    def draw(self):
        odd = pyxel.frame_count % 2
        pyxel.blt(
                self.x,
                self.y,
                0,
                Enemy.ship[self.size]["x"][odd], 
                Enemy.ship[self.size]["y"][odd], 
                Enemy.ship[self.size]["w"], 
                -Enemy.ship[self.size]["h"], 
                0)

Enemy.ship = {
    "small" : {"x":[38, 38],"y":[74, 88],"w":20,"h":13},
    "medium" : {"x":71,"y":41,"w":18,"h":14},
    "Type B" : {"x":[0, 0],"y":[109, 131],"w":28,"h":22},
    "large" : {"x":32,"y":0,"w":30,"h":20}
}
