import pyxel
from tools import Tools

class Joueur:

    def __init__(self, g):
        self.game = g
        self.x = 55
        self.y = 100
        self.size = "small"
        self.speedX = 3
        self.speedY = 2.5
        self.life = 3
        self.ammo = 3
        self.ship = Joueur.ship[self.size]
        self.w = self.ship["w"] - 5 * 2
        self.h = self.ship["h"]

    def update(self):

        if self.life > 0:
            self.stickX = Tools.normalizeStickVal(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX))
            self.stickY = Tools.normalizeStickVal(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY))

            if self.game.controller == "gamepad":
                self.speedY = 2.5 
            if self.game.controller == "keyboard":
                self.speedY = 3
            
            up =  self.stickY < 0.4 or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W)
            down = self.stickY > 0.6 or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)
            left = self.stickX < 0.4 or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A)
            right = self.stickX > 0.6 or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)
            shootBullet = pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.KEY_Z)
            shootMissile = pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or pyxel.btnp(pyxel.KEY_X)

            if right:
                self.x = (self.x + self.speedX)
                if self.x > 128 - self.ship["w"]:
                    self.x = 128 - self.ship["w"]

            if left:
                self.x = (self.x - self.speedX)
                if self.x < 0:
                    self.x = 0

            if up:
                self.y = (self.y - self.speedY)
                if self.y < 0:
                    self.y = 0

            if down:
                self.y = (self.y + self.speedY)
                if self.y > 128 - self.ship["h"]:
                    self.y = 128 - self.ship["h"]
        
            if shootBullet:
                self.game.shoot()
                if self.game.etat == "AttritionGame":
                    self.life -= 1
            
            if shootMissile and self.ammo > 0:
                self.ammo -= 1
                self.game.shoot(type="missile")
                if self.game.etat == "AttritionGame":
                    self.life -= 1

            # analog controls
            # self.x += self.speedX * (self.stickX - 0.5)
            # self.y += self.speedY * (self.stickY - 0.5)

    def draw(self):
        odd = pyxel.frame_count % 2
        if self.life < 0:
            return

        if not self.game.grace.elapsed():
            if odd:
                return
                
        pyxel.blt(self.x, self.y,
                    0,
                    self.ship["x"][odd], 
                    self.ship["y"][odd], 
                    self.ship["w"], 
                    self.ship["h"], 
                    0)

Joueur.totalLife = 30

Joueur.ship = {
    "small" : {"x":[72, 72],"y":[74, 88],"w":16,"h":13},
    "medium" : {"x":71,"y":41,"w":18,"h":14},
    "large" : {"x":66,"y":6,"w":28,"h":20}
}
