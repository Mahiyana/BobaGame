import pyglet

class CollectableItem(pyglet.sprite.Sprite):
    def __init__(self, name,x,y,width,height):
       #self.width = width
       #self.height = height
        self.taken = False
        image = pyglet.resource.image(name+".png")
        super().__init__(image)
        self.x = x
        self.y = y
 
