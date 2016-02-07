import pyglet
from Character import Character

class Player():
    dx = 0
    dy = 0 
    vy = 0
    vx = 0
    ay = 0
    ax = 0
    x = 0
    y = 0
    standing = True
    standing_x = True
    last_direction = None
     
    postac = Character("boba_standing_right.png")
    def jump(self):
        if self.standing:
            self.vy = 2
            self.standing = False
    
    def left(self):
        if self.standing_x:
            self.postac = self.postac.move_left()
            self.standing_x = False
            self.last_direction = "left"

    def right(self):
        if self.standing_x:
            self.postac = self.postac.move_right()
            self.standing_x = False    
            self.last_direction = "right"
    
    def stop_left(self):
        self.postac = self.postac.stand_left()
        self.standing_x = True

    def stop_right(self):
        self.postac = self.postac.stand_right()
        self.standing_x = True
    
    def stop_moving(self):
        if self.last_direction == "left":
            self.stop_left()
        else:
            self.stop_right()


