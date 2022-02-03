import pyxel
import math
import tweening
from random import randint
from danger import Danger
from joueur import Joueur
from bullet import Bullet
from missile import Missile
from enemy import Enemy
from boss import Boss
from explosion import Explosion
from puff import Puff
from text import Text
from bonus import Bonus
from tools import Tools
from pop import Pop

import os
from os.path import expanduser

class Jeu:

    def __init__(self):

        Jeu.version = "1.6.2"

        pyxel.init(
            128,
            128,
            fps=30,
            quit_key=pyxel.KEY_TAB,
            capture_sec=30
        )

        Jeu.etat = "Menu"
        Jeu.controller = "gamepad"

        pyxel.image(0).load(0, 0, "../assets/ships.png")
        pyxel.image(1).load(0, 0, "../assets/tiles_packed.png")

        Jeu.bullets = []
        Jeu.missiles = []
        Jeu.ennemi = []
        Jeu.danger = []
        Jeu.bossFight = False
        Jeu.explosions = []
        Jeu.pops = []
        Jeu.text = []
        self.bonus = None
        Jeu.lines = ["Credits",
                    "", 
                    "Orange Juice Invasion", 
                    "a game by",
                    "Arthus Meuret", 
                    "", 
                    "Additional Help", 
                    "Arthur Pelletier", 
                    "Louis Persin", 
                    "",
                    "Graphics",
                    "Kenney",
                    "aka Jesus of assets",
                    "",
                    "Technical support",
                    "Arnaud Meuret",
                    "",
                    "Kickstart",
                    "Laurent \"the real\" Abbal",
                    "",
                    "Pyxel creator",
                    "Kitao",
                    str(pyxel.PYXEL_VERSION),
                    "",
                    "Thanks for playing",
                    "Please follow me on itch.io",
                    "Stay tuned for updates...",
                    ""]

        Jeu.LINE_DELAY = 40
        Jeu.next_line = 0
        Jeu.time_to_next_line = 0
        Jeu.credits_time = 0
        Jeu.bossSpawnRate = 10000
        self.score = 0
        self.menuPos = 0
        self.alarm = False
        self.v1 = tweening.TimedValue(16, f='easeOutBounce')
        self.v2 = tweening.TimedValue(64, f='easeOutBounce')
        self.v3 = tweening.TimedValue(32, f='easeOutBounce')
        self.grace = tweening.TimedBool(30)
        self.accurTw = tweening.TimedValue(100, 200, f='easeOutExpo')
        self.v5 = tweening.TimedValue(48, f='easeOutBounce')
        self.testTw = tweening.TimedValue(128-16, offset=16, duration=15, f='easeInOutSine', bounce=True)
        self.test2Tw = tweening.TimedValue(30, duration=40, f="easeInElastic", inverted=True)

        self.stimX = tweening.TimedValue(116, offset=0, duration=120, f="linear", bounce=True)
        self.stimY = tweening.TimedValue(70, offset=60, duration=30, f="easeInOutBack", bounce=True)        

        self.xDemoBoss = tweening.TimedValue(128, offset=-26, duration=60, f='easeInOutSine', bounce=True)
        self.yDemoBoss = tweening.TimedValue(110, offset=80, duration=30, f='easeInOutSine', bounce=True)

        self.timeToStim = tweening.TimedBool(30 * 60 * 2, autoreset=True)

        self.accurDelay = tweening.TimedBool(45)
        self.delay2 = tweening.TimedBool(90)
        self.delay3 = tweening.TimedBool(90, autoreset=True)
        self.resetDone = False

        self.accurSound1 = False
        self.accurSound2 = False
        self.accurSound3 = False
        self.accurSound4 = False
        self.accurColor = 11
        self.accurPerfect = False
        self.accurBlink = tweening.TimedBool(4)
        
        self.helpDisplay = tweening.TimedBool(30 * 10)

        self.scoreFilePath = expanduser("~") + "/OJI-Highscores"
        self.readHighscore()

        pyxel.load("../assets/oji.pyxres", image=False)
        pyxel.run(self.update, self.draw)

    def initNormal(self):
        self.initActorStores()
        self.initStats()
        self.initPlayer()
        Jeu.spawnRate = 20
    
    def initAttrition(self):
        self.initActorStores()
        self.initStats()
        self.initPlayer()
        self.player.life = 30
        self.player.ammo = 0

    def initPlayer(self):
        self.player = Joueur(self)

    def initStats(self):
        self.score = 0
        self.shotCount = 0.0
        self.hitCount = 0.0
        self.timeToStim.reset()
        self.helpDisplay.reset()
        self.playStart = pyxel.frame_count

    def initActorStores(self):
        # List comprehensions: https://www.geeksforgeeks.org/python-list-comprehension/
        Jeu.bullets = [None for x in range(20)]
        Jeu.missiles = [None for x in range(20)]
        Jeu.enemies = [None for x in range(20)]
        Jeu.explosions = [None for x in range(20)]
        Jeu.danger = [None for x in range(50)]
        Jeu.pops = [None for x in range(20)]
        Jeu.boss = None

    def playTime(self):
        return pyxel.frame_count - self.playStart

    def shoot(self, type="bullet"):
        self.shotCount += 1
        pyxel.play(0, [0], loop=False)
        if type == "bullet":
            for i in range(len(Jeu.bullets)):
                if Jeu.bullets[i] == None:
                    Jeu.bullets[i] = Bullet(self.player.x + self.player.ship["w"]//2 ,self.player.y)
                    break
        elif type == "missile":
            for i in range(len(Jeu.missiles)):
                if Jeu.missiles[i] == None:
                    Jeu.missiles[i] = Missile(self.player.x + self.player.ship["w"]//2 - 2,self.player.y + self.player.ship["h"]//2, self)
                    break
    
    def rect_overlap(self, x1, x2, y1, y2, w1, w2, h1, h2):
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

    def enemyBulletColision(self, e, b):
        return self.rect_overlap(e.x, b.x, e.y, b.y, e.w, 1, e.h, 4)
    
    def enemyPlayerColision(self, e, p):
        return self.rect_overlap(e.x, p.x + 5, e.y, p.y, e.w, self.player.w, e.h, self.player.h)

    def dangerPlayerCollision(self, d, p):
        return self.rect_overlap(d.x-1, p.x + 5, d.y-1, p.y, d.w, self.player.w, d.h, self.player.h)

    def spawn_explosion(self, ship):
        for i in range(len(Jeu.explosions)):
            if not Jeu.explosions[i]:
                newExplosion = Explosion(ship.x, ship.y, ship.w, ship.h)
                Jeu.explosions[i] = newExplosion
                return newExplosion

    def spawn_puff(self, ship):
        for i in range(len(Jeu.explosions)):
            if not Jeu.explosions[i]:
                newPuff = Puff(ship.x, ship.y, ship.w, ship.h)
                Jeu.explosions[i] = newPuff
                return newPuff

    def spawnDanger(self, x, y, vx, vy):
        for i in range(len(Jeu.danger)):
            if not Jeu.danger[i]:
                Jeu.danger[i] = Danger(x, y, vx, vy)
                pyxel.play(1, [9], loop=False)
                break

    def spawnPop(self, x, y, text, tf="easeOutElastic", dx=10, dy=10, tx=30, ty=30, life=40):
        for i in range(len(Jeu.pops)):
            if not Jeu.pops[i]:
                newPop = Jeu.pops[i] = Pop(x, y, text, tweeningFunc=tf, dx=dx, dy=dy, tx=tx, ty=ty, life=life)
                return newPop

############################################################################################

    def switchToGameOverNormal(self):
        self.v1.reset()
        self.v2.reset()
        self.v3.reset()
        self.v5.reset()
        self.accurDelay.reset()
        self.delay2.reset()
        if self.shotCount > 0:
            self.accurTw.setValue(self.hitCount/self.shotCount*100)

        self.resetDone = False
        pyxel.play(0, [5], loop=False)
        Jeu.etat = "GameOverNormal"
        Jeu.text = []
        Jeu.credits_time = 0
        Jeu.next_line = 0

        self.accurSound1 = False
        self.accurSound2 = False
        self.accurSound3 = False
        self.accurSound4 = False
        self.accurPerfect = False

    def switchToGameOverAttrition(self):
        self.v1.reset()
        self.v2.reset()
        self.v3.reset()
        self.v5.reset()
        self.accurDelay.reset()
        self.delay2.reset()
        if self.shotCount > 0:self.accurTw.setValue(self.hitCount/self.shotCount*100)
        self.resetDone = False
        pyxel.play(0, [5], loop=False)
        Jeu.etat = "GameOverAttrition"
        Jeu.text = []
        Jeu.credits_time = 0
        Jeu.next_line = 0

############################################################################################

    def update(self):
        if Jeu.etat == "NormalGame":
            self.updateNormalGame()
        elif Jeu.etat == "AttritionGame":
            self.updateAttritionGame()
        elif Jeu.etat == "Menu":
            self.updateMenu()
        elif Jeu.etat == "GameSelect":
            self.updateGameSelect()
        elif Jeu.etat == "Pause":
            self.updatePause()
        elif Jeu.etat == "GameOverNormal":
            self.updateGameOverNormal()
        elif Jeu.etat == "GameOverAttrition":
            self.updateGameOverAttrition()
        elif Jeu.etat == "Credits":
            self.updateCredits()

############################################################################################

    def updateCredits(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Menu"

        for i in range(len(self.text)):
            cur = self.text[i]
            if not cur:
                continue
            cur.update()
            if cur.life <= 0:
                self.text[i] = None

        Jeu.time_to_next_line -= 1
        if self.time_to_next_line <= 0 and Jeu.next_line < len(Jeu.lines):
            Jeu.text.append(Text(64, 136, Jeu.lines[Jeu.next_line], 600))
            Jeu.time_to_next_line = self.LINE_DELAY
            Jeu.next_line += 1

        if pyxel.frame_count % 5 == 0:
            self.spawn_explosion(Enemy(randint(0, 128),randint(0, 128), self))

        for i in range(len(Jeu.explosions)):
            if Jeu.explosions[i]:
                Jeu.explosions[i].update()
                if Jeu.explosions[i].life <= 0:
                    Jeu.explosions[i] = None

        if self.credits_time >= len(Jeu.lines) * self.LINE_DELAY + 350:
            Jeu.etat = "Menu"

        self.credits_time += 1

###########################################################################################

    def updateNormalGame(self):

        if self.timeToStim.true() and not self.bonus:
            self.bonus = Bonus(self)
        
        if self.bonus:
            self.bonus.update()
            if self.bonus.collision(self.player):
                self.bonus = None
                pyxel.play(0, [14])
                if self.player.life < 3:
                    self.player.life += 1
                else:
                    self.score += 1000
                    self.spawnPop(self.player.x + self.player.w, self.player.y,"1000",tf="easeOutExpo")

        if pyxel.frame_count%Jeu.spawnRate == 0: # and not Jeu.bossFight:
            for i in range(len(Jeu.enemies)):
                if not Jeu.enemies[i]:
                    Jeu.enemies[i] = Enemy(randint(10, 118),-10, self)
                    break
        
        if not Jeu.boss:
            if self.score % Jeu.bossSpawnRate == 0 and self.score > 0:
                Jeu.bossFight = True
                Jeu.spawnRate = 45
                pyxel.play(2, [7], loop=False)
                Jeu.boss = Boss(self, 64 - 13 , -20)
        
        if Jeu.boss:
            Jeu.boss.update()
            if Jeu.boss.life <= 0:
                pyxel.play(1, [2], loop=False)
                self.score += 1000
                Jeu.spawnRate = 15
                Jeu.boss = None
                Jeu.bossFight = False

        self.player.update()

        if self.score > self.highscoreNormal:
            self.highscoreNormal = self.score

        if self.player.life <= 0:
            self.switchToGameOverNormal()

        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Pause"
            pyxel.stop(0)
        
        for i in range(len(Jeu.bullets)):
            cur_bullet = Jeu.bullets[i]
            if cur_bullet:
                cur_bullet.update()
                if cur_bullet.y <= -4:
                    Jeu.bullets[i] = None
                for j in range(len(Jeu.enemies)):
                    cur_enemy = Jeu.enemies[j]
                    if cur_enemy and self.enemyBulletColision(cur_enemy, cur_bullet):
                        self.spawnPop(cur_enemy.x, cur_enemy.y, str(cur_enemy.points), dx=16, dy=16)
                        cur_enemy.life -= 1
                        self.hitCount += 1
                        Jeu.bullets[i] = None
                        pyxel.play(1, [3], loop=False)
                if Jeu.boss and self.enemyBulletColision(Jeu.boss, cur_bullet):
                    Jeu.boss.takeHit()
                    Jeu.bullets[i] = None
                    self.hitCount += 1
        
        for i in range(len(Jeu.missiles)):
            cur_missile = Jeu.missiles[i]
            if cur_missile:
                cur_missile.update()
                if cur_missile.y <= -4:
                    Jeu.missiles[i] = None
                for j in range(len(Jeu.enemies)):
                    cur_enemy = Jeu.enemies[j]
                    if cur_enemy and self.enemyBulletColision(cur_enemy, cur_missile):
                        self.spawnPop(cur_enemy.x, cur_enemy.y, str(cur_enemy.points), dx=16, dy=16)
                        cur_enemy.life -= 10
                        self.hitCount += 1
                        pyxel.play(1, [3], loop=False)
                if Jeu.boss and self.enemyBulletColision(Jeu.boss, cur_missile):
                    Jeu.boss.takeHit(dType="missile")
                    Jeu.missiles[i] = None
                    self.hitCount += 1
                        
        for i in range(len(Jeu.danger)):
            curD = Jeu.danger[i]
            if curD:
                curD.update()
                if curD.x <= -4 or curD.x >= 130 or curD.y <= -4 or curD.y >= 130:
                    Jeu.danger[i] = None
                if self.dangerPlayerCollision(curD, self.player) and self.grace.elapsed():
                    self.grace.reset()
                    Jeu.danger[i] = None
                    self.spawn_puff(self.player)
                    self.player.life -= 1
                    pyxel.play(2, [2], loop=False)


        for i in range(len(Jeu.enemies)):
            cur_enemy = Jeu.enemies[i]
            if cur_enemy:
                cur_enemy.update()
                if cur_enemy.y >= 137:
                    Jeu.enemies[i] = None
                if self.enemyPlayerColision(cur_enemy, self.player) and self.grace.elapsed():
                    self.grace.reset()
                    Jeu.enemies[i] = None
                    self.spawn_explosion(cur_enemy)
                    self.spawn_puff(self.player)
                    self.player.life -= 1
                    pyxel.play(2, [2], loop=False)
                if cur_enemy.life <= 0:
                    Jeu.enemies[i] = None
                    self.score += 100
                    self.spawn_explosion(cur_enemy)
                    pyxel.play(1, [1], loop=False)
        
        for i in range(len(Jeu.explosions)):
            if Jeu.explosions[i]:
                Jeu.explosions[i].update()
                if Jeu.explosions[i].life <= 0:
                    Jeu.explosions[i] = None
        
        self.updatePops()
    
    def updatePops(self):
        for i in range(len(Jeu.pops)):
            if Jeu.pops[i]:
                Jeu.pops[i].update()
                if Jeu.pops[i].life <= 0:
                    Jeu.pops[i] = None

############################################################################################

    def updateAttritionGame(self):
        if pyxel.frame_count%15 == 0:
            for i in range(len(Jeu.enemies)):
                if not Jeu.enemies[i]:
                    Jeu.enemies[i] = Enemy(randint(10, 118), 0, self)
                    break
        
        if pyxel.frame_count%30 == 0:
            self.player.life -= 1
        
        if self.player.life > 30:
            self.player.life = 30
        
        self.player.update()

        if self.score > self.highscoreAttrition:
            self.highscoreAttrition = self.score

        if self.player.life <= 0:
            self.switchToGameOverAttrition()

        # elif self.player.life <= 20 and not self.alarm:
        #     self.alarm = True
        #     pyxel.playm(0, loop=True)
        # elif self.player.life > 20:
        #     pyxel.stop(0)
        #     self.alarm = False


        if pyxel.btnp(pyxel.KEY_BACKSPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Pause"
            pyxel.stop(0)
        
        for i in range(len(Jeu.bullets)):
            cur_bullet = Jeu.bullets[i]
            if cur_bullet:
                cur_bullet.update()
                if cur_bullet.y <= -4:
                    Jeu.bullets[i] = None
                    self.player.life -= 3
                for j in range(len(Jeu.enemies)):
                    cur_enemy = Jeu.enemies[j]
                    if cur_enemy and self.enemyBulletColision(cur_enemy,cur_bullet):
                        cur_enemy.life -= 1
                        self.hitCount += 1
                        self.player.life += 2
                        Jeu.bullets[i] = None
                        pyxel.play(0, [3], loop=False)

        for i in range(len(Jeu.enemies)):
            cur_enemy = Jeu.enemies[i]
            if cur_enemy:
                cur_enemy.update()
                if cur_enemy.y >= 137:
                    Jeu.enemies[i] = None
                    self.player.life -= 10
                if self.enemyPlayerColision(cur_enemy, self.player) and self.grace.elapsed():
                    Jeu.enemies[i] = None
                    self.grace.reset()
                    self.spawn_explosion(cur_enemy)
                    self.spawn_puff(self.player)
                    self.player.life -= 10
                    pyxel.play(2, [2], loop=False)
                if cur_enemy.life <= 0:
                    Jeu.enemies[i] = None
                    self.score += 100
                    self.spawn_explosion(cur_enemy)
                    pyxel.play(1, [1], loop=False)
        
        for i in range(len(Jeu.explosions)):
            if Jeu.explosions[i]:
                Jeu.explosions[i].update()
                if Jeu.explosions[i].life <= 0:
                    Jeu.explosions[i] = None

        for i in range(len(Jeu.pops)):
            if Jeu.pops[i]:
                Jeu.pops[i].update()
                if Jeu.pops[i].life <= 0:
                    Jeu.pops[i] = None

############################################################################################

    def updateMenu(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE): self.test2Tw.reset()

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            Jeu.etat = "GameSelect"
            pyxel.play(0, [3], loop=False)

        if pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_BACK):
            Jeu.etat = "Credits"
            Jeu.text = []
            Jeu.credits_time = 0
            Jeu.next_line = 0
            Jeu.initActorStores(self)
            pyxel.play(0, [3], loop=False)

############################################################################################

    def updatePause(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "NormalGame"
        if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Menu"

############################################################################################

    def updateGameOverNormal(self):

        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Menu"
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            Jeu.etat = "NormalGame"
            pyxel.play(0, [4], loop=False)
            Jeu.initNormal(self)
        if pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_BACK):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Credits"
        if pyxel.btnp(pyxel.KEY_R):
            self.switchToGameOverNormal()
        
        self.updatePops()

        if self.accurDelay.elapsed():
                
            if self.accurBlink.elapsed():
                self.accurColor = 11
            else:
                self.accurColor = 7

            if self.accurPerfect:
                if pyxel.frame_count%4==0:
                    self.accurColor = 7
                else:
                    self.accurColor = 10
            
            if not self.resetDone:
                self.accurTw.reset()
                self.resetDone = True
            
            if self.score > 0:
                scoreX = 76+len(str(self.score))*4
                if self.score >= self.highscoreNormal:
                    scoreY = self.v2.value()
                else:
                    scoreY = self.v3.value()

            self.accurTw.debug = True
            if self.accurTw.crossed(50):
                pyxel.play(0, 10)
                self.accurBlink.reset()
                self.spawnPop(scoreX, scoreY, "500", tf="easeOutCirc", life=75)
                self.score += 500

            if self.accurTw.crossed(85):
                pyxel.play(0, 11)
                self.accurSound2 = True
                self.accurBlink.reset()
                self.spawnPop(scoreX, scoreY, "1000", tf="easeOutCirc", life=75)
                self.score += 1000

            if self.accurTw.crossed(95):
                pyxel.play(0, 12)
                self.accurSound3 = True
                self.accurBlink.reset()
                self.spawnPop(scoreX, scoreY, "2000", tf="easeOutCirc", life=75)
                self.score += 2000

            if self.accurTw.value() == 100 and  self.accurTw.justFinished():
                pyxel.play(3, 13)
                self.accurSound4 = True
                self.accurPerfect = True
                self.spawnPop(scoreX, scoreY, "5000", tf="easeOutCirc")
                self.score += 5000


    def updateGameOverAttrition(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Menu"
        if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            Jeu.etat = "AttritionGame"
            pyxel.play(0, [4], loop=False)
            Jeu.initAttrition(self)
        if pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_BACK):
            pyxel.play(0, [3], loop=False)
            Jeu.etat = "Credits"
        if self.accurDelay.elapsed():
            if not self.resetDone:
                self.accurTw.reset()
                self.resetDone = True   

    def updateGameSelect(self):
        
        self.stickX = Tools.normalizeStickVal(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX))
        self.stickY = Tools.normalizeStickVal(pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY))
        up =  self.stickY < 0.4 or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)
        down = self.stickY > 0.6 or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
        
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            if self.menuPos == 0:
                Jeu.etat = "NormalGame"
                self.initNormal()
                pyxel.play(1, [4], loop=False)
            elif self.menuPos == 1:
                Jeu.etat = "AttritionGame"
                # pyxel.playm(0, loop=True)
                self.initAttrition()
        if up:
            pyxel.play(0, [3], loop=False)
            self.menuPos -= 1

        if down:
            pyxel.play(0, [3], loop=False)
            self.menuPos += 1

        if self.menuPos < 0:
            self.menuPos = 1
        if self.menuPos > 1:
            self.menuPos = 0

        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
            Jeu.etat = "Menu"

    def draw(self):
        if Jeu.etat == "NormalGame":
            self.drawNormalGame()
        elif Jeu.etat == "AttritionGame":
            self.drawAttritionGame()
        elif Jeu.etat == "Menu":
            self.drawMenu()
        elif Jeu.etat == "GameSelect":
            self.drawGameSelect()
        elif Jeu.etat == "Pause":
            self.drawPause()
        elif Jeu.etat == "GameOverNormal":
            self.drawGameOverNormal()
        elif Jeu.etat == "GameOverAttrition":
            self.drawGameOverAttrition()
        elif Jeu.etat == "Credits":
            self.drawCredits()
        
    def drawCredits(self):
        pyxel.cls(1)

        for ex in self.explosions:
            if ex: ex.draw()

        for text in self.text:
            if not text: continue
            self.centeredText(text.text, text.y)
    
    def drawGameSelect(self):
        pyxel.cls(1)
        self.centeredText("Choose your game mode", 16, 9)
        self.centeredText("Classic", 48)
        self.centeredText("Attrition", 56)
        self.centeredText("ESC: Back", 118, 5)
        self.centeredText(">              <", 48 + self.menuPos * 8, 10)
        if self.menuPos == 0:
            self.centeredText("Classic shoot'em up",90, 7)
        else:
            self.centeredText("Lose health over time",90, 7)

####################################################################################################

    def drawNormalGame(self):

        pyxel.cls(1)


        if self.bonus:
            self.bonus.draw()

        for b in self.bullets:
            if b: b.draw()
        
        for m in self.missiles:
            if m: m.draw()

        self.player.draw()

        for d in self.danger:
            if d: d.draw()

        for e in self.enemies:
            if e: e.draw()

        if Jeu.boss:
            Jeu.boss.draw()
        
        for pop in self.pops:
            if pop: pop.draw()

        for ex in self.explosions:
            if ex: ex.draw()

        self.centeredText(str(self.highscoreNormal), 5, 10)
        pyxel.text(5, 5, "SCORE: " + str(self.score), 11)
        for i in range(self.player.life):
            pyxel.blt(5 + i * 8, 12, 1, 96, 56, 7, 5, 0)

        for i in range(self.player.ammo):  
            pyxel.blt(5 + i * 5, 19, 1, 6, 20, 4, 8, 0)

        if self.shotCount == 0:
            if self.playTime() > 30 and not self.helpDisplay.elapsed():
                self.centeredText("<Z> for main weapon", 50, 10)
                self.centeredText("<X> for special weapon", 58, 10)

    
#######################################################################################################

    def drawAttritionGame(self):
        pyxel.cls(1)

        if self.alarm:
            pyxel.rect(0, 0, 2, 127, 8)
            pyxel.rect(127, 0, 2, 127, 8)

        self.player.draw()

        self.drawLifeBar(5, 16)

        for b in self.bullets:
            if b: b.draw()

        for e in self.enemies:
            if e: e.draw()
        
        for ex in self.explosions:
            if ex: ex.draw()

        pyxel.text(5, 5, "SCORE: " + str(self.score), 11)
        self.centeredText(str(self.highscoreAttrition), 5, 10)

#######################################################################################################

    def drawGameOverNormal(self):
        pyxel.cls(1)

        self.centeredText("GAME OVER", self.v1.value(), 8)

        if self.score > 0 and self.score >= self.highscoreNormal:
            self.centeredText("CONGRATULATIONS !", self.v3.value(), 7)
            self.centeredText("New High Score", self.v5.value(), 10)
            self.centeredText(str(self.highscoreNormal), self.v2.value(), 10)
            self.saveHighscore()
        else:
            self.centeredText("Score : " + str(self.score), self.v3.value(), 10)
            self.centeredText("High Score : " + str(self.highscoreNormal), self.v2.value(), 10)

        if self.shotCount > 0:
            if self.accurDelay.elapsed():
                self.centeredText(f"Accuracy: {self.accurTw.value(True)}%", 80, self.accurColor)

        if self.delay2.elapsed():
            self.centeredText("Press ENTER to play again", 100)
            self.centeredText("Press ESC for menu", 110)
            self.centeredText("press C for Credits", 120, 5)
        
        for pop in self.pops:
            if pop: pop.draw()

#######################################################################################################

    def drawGameOverAttrition(self):
        pyxel.cls(1)

        self.centeredText("GAME OVER", self.v1.value(), 8)

        if self.score > 0 and self.score >= self.highscoreAttrition:
            self.centeredText("CONGRATULATIONS !", self.v3.value(), 7)
            self.centeredText("New High Score", self.v5.value(), 10)
            self.centeredText(str(self.highscoreAttrition), self.v2.value(), 10)
            self.saveHighscore()
        else:
            self.centeredText("Score : " + str(self.score), self.v3.value(), 10)
            self.centeredText("High Score : " + str(self.highscoreAttrition), self.v2.value(), 10)

        if self.shotCount > 0:
            if self.accurDelay.elapsed():
                self.centeredText(f"Accuracy: {math.ceil(self.accurTw.value())}%", 80)

        if self.delay2.elapsed():
            self.centeredText("Press ENTER to play again", 100)
            self.centeredText("Press ESC for menu", 110)
            self.centeredText("press C for Credits", 120, 5)

    def drawMenu(self):
        odd = pyxel.frame_count % 2

        pyxel.cls(1)

        self.centeredText("ORANGE JUICE INVASION", 16, 9)
        pyxel.text(108, 122, Jeu.version, 5)

        if (pyxel.frame_count % 30) < 15: self.centeredText("> START NEW GAME <", 64)

        pyxel.blt(64-8, 128//3-6,
                    0,
                    Joueur.ship["small"]["x"][odd], 
                    Joueur.ship["small"]["y"][odd], 
                    Joueur.ship["small"]["w"], 
                    Joueur.ship["small"]["h"], 
                    0)
        
        pyxel.blt(64-Boss.ship["large"]["w"]/2, 128//2+32,
                    0,
                    Boss.ship["large"]["x"][odd], 
                    Boss.ship["large"]["y"][odd], 
                    Boss.ship["large"]["w"], 
                    Boss.ship["large"]["h"], 
                    0)

        pyxel.blt(64-4, 128//2+24-3,1,96, 48, 8, 8, 0)
        
        # ship = Enemy.ship["Type B"]
        # pyxel.blt(self.xDemoBoss.value(), self.yDemoBoss.value(),
        #             0,
        #             ship["x"][odd], 
        #             ship["y"][odd], 
        #             ship["w"], 
        #             ship["h"], 
        #             0)

    def centeredText(self, t, l, c=11):
        x = 128/2 - len(t) / 2 * 4
        pyxel.text(x, l, t, c)
    
    def drawLifeBar(self, x, y):
        h = 2 * self.player.life
        pyxel.rect(x, 118 - h, 3, h, 10)
        pyxel.rectb(x-1, 118 - Joueur.totalLife*2, 5, Joueur.totalLife*2, 13)
        pyxel.text(x, 122, str(math.ceil(self.player.life)), 10)

    def readHighscore(self):
        try:
            f = open(self.scoreFilePath,'r')
        except FileNotFoundError:
            self.highscoreNormal = 0
            self.highscoreAttrition = 0
        else:
            self.highscoreNormal = int(f.readline())
            self.highscoreAttrition = int(f.readline())
            f.close()

    def saveHighscore(self):
        f = open(self.scoreFilePath,'w+')
        f.write(str(self.highscoreNormal)+"\n")
        f.write(str(self.highscoreAttrition)+"\n")
        f.close()

    def drawPause(self):
        self.centeredText("GAME PAUSED", 64)
        self.centeredText("ESC to continue", 64 + 8)
        self.centeredText("Q to quit", 64 + 16)
