import pyglet
from Camera import *

class Sprite(pyglet.sprite.Sprite):
    
    def __init__(self, name):
        image = pyglet.resource.image(name+".png")
        super().__init__(image)

    def draw(self):
        self.x -= camera.x
        self.y -= camera.y
        super().draw()
        self.x += camera.x
        self.y += camera.y

