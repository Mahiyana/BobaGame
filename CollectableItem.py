import pyglet
from Sprite import Sprite

class CollectableItem(Sprite):
    def __init__(self, name,x,y,width,height):
       #self.width = width
       #self.height = height
        self.taken = False
        super().__init__(name)
        self.x = x
        self.y = y
 
