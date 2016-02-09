import pyglet
from Sprite import Sprite

class Bullet(Sprite):
    def __init__(self,name,x,y,right):
        super().__init__(name)
        self.x = x
        self.y = y
        self.right = right
        self.span = 10

    def update(self):
        if self.right:
            self.x += 20
        else:
            self.x -= 20
        self.span -= 1    

    def draw(self):
        super().draw()


