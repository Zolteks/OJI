import pyxel
from random import randint
from bullet import Bullet
import tweening

from explosion import Explosion

class Boss:

    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.speed = -0.5
        self.life = Boss.maxLife
        self.size = "large"
        self.w = Boss.ship[self.size]["w"]
        self.h = Boss.ship[self.size]["h"]
        self.game = game
        self.fire = None
        self.fireReload = 15
        self.canonAngle = tweening.TimedValue(30, duration=120, f="easeInOutSine", bounce=True)

    def update(self):
        
        self.x += self.speed
        
        if self.y < 16:
            self.y += 0.5
        
        if self.x < -5 or self.x > 133-self.w:
            self.speed = -self.speed

        if pyxel.frame_count % self.fireReload == 0:
            x = self.x + self.w / 2
            y = self.y + self.h
            self.game.spawnDanger(x, y, (randint(0,30)-15)/10, 1)

        if self.life <= 10:
            self.fireReload = 12
            if self.speed <= -0.5:
                self.speed = -1
            else:
                self.speed = 1

            if pyxel.frame_count % 25 == 0:
                puff = self.game.spawn_puff(self)
                if puff: # puff can be None if no slot was available
                    puff.vx = randint(0,3) - 1.5
                    puff.vy = randint(0,3) - 2.5

            if self.fire:
                self.fire.x = self.x
                self.fire.y = self.y
                if self.fire.life <= 5: self.fire.life = 30
            else:
                self.fire = self.game.spawn_explosion(self)

        if self.life == 0:
            deathX = self.x
            deathY = self.y
            explosionRange = self.w * 2
            for i in range(0, 10):
                self.x = deathX + randint(0, explosionRange) - explosionRange / 2
                self.y = deathY + randint(0, self.h) - self.h / 2
                self.game.spawn_explosion(self)

    def takeHit(self, dType="bullet"):
        if dType == "bullet":
            self.life -= 1
        if dType == "missile":
            self.life -= 15
        puff = self.game.spawn_puff(self)
        if puff:
            puff.vx = randint(0,4) - 2
            puff.vy = randint(0,4) - 2

    def draw(self):
        odd = pyxel.frame_count % 2
        pyxel.blt(
                self.x,
                self.y,
                0,
                Boss.ship[self.size]["x"][odd], 
                Boss.ship[self.size]["y"][odd], 
                Boss.ship[self.size]["w"], 
                -Boss.ship[self.size]["h"], 
                0)

        barColor = 3 
        if self.life < Boss.maxLife * 0.5: barColor = 9 
        if self.life < Boss.maxLife * 0.2: barColor = 8 

        pyxel.rect(self.x, self.y - 3, self.w * self.life / Boss.maxLife, 1, barColor)
        pyxel.rectb(self.x - 1, self.y - 4, self.w + 1, 3, 13)

Boss.ship = {
    "small" : {"x":38,"y":74,"w":20,"h":13},
    "medium" : {"x":71,"y":41,"w":18,"h":14},
    "large" : {"x":[35, 35],"y":[0, 20],"w":26,"h":20}
}

Boss.maxLife = 30