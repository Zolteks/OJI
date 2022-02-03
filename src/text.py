from tools import Tools

class Text:

    def __init__(self, x, y, t, l):
        self.x = x
        self.y = y
        self.text = t
        self.life = l
    
    def update(self):
        self.life -= 1
        self.y -= 0.5