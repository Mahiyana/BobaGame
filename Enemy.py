import pyglet
from Character import Character

class Enemy(Character):
    direction = 1
    def __init__(self,name,grid,x,y):
        super().__init__(name,grid)
        self.x = x
        self.y = y

    def move_self(self,dt):
        #x_old = self.x
        self.x += self.vx * dt * 500
        self.move(dt, self.direction)
        """
        if self.direction == 1:
            self.move(dt,1)
            if x_old == self.x:
                self.direction = -1
                self.x -= 10
        else:
            self.move(dt,-1)
            if x_old == self.x:
                self.direction = 1
                self.x += 10
        """

    def change_direction(self):
        self.direction = 0 - self.direction
