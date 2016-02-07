import pyglet

platform_width = 32
platform_height = 32

class Platform(pyglet.sprite.Sprite):
    def __init__(self, name):
        image = pyglet.resource.image(name+".png")
        super().__init__(image)


