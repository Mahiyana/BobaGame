import pyglet

class Character(pyglet.sprite.Sprite):
        
    def __init__(self,image):
        super().__init__(pyglet.image.load(image))
        self.standing_left = pyglet.image.load("boba_standing_left.png")
        self.moving_left_1 = pyglet.image.load("boba_moving_left_1.png")
        self.moving_left_2 = pyglet.image.load("boba_moving_left_2.png")
        self.animation_left = pyglet.image.Animation.from_image_sequence([
            self.standing_left, self.moving_left_1, self.moving_left_2],0.1,True)

        self.standing_right = pyglet.image.load("boba_standing_right.png")
        self.moving_right_1 = pyglet.image.load("boba_moving_right_1.png")
        self.moving_right_2 = pyglet.image.load("boba_moving_right_2.png")
        self.animation_right = pyglet.image.Animation.from_image_sequence([
            self.standing_right, self.moving_right_1, self.moving_right_2],0.1,True)

    def move_left(self):
        self.image = self.animation_left
        return self

    def move_right(self):
        self.image = self.animation_right
        return self

    def stand_left(self):
        self.image = self.standing_left
        return self

    def stand_right(self):
        self.image = self.standing_right
        return self


