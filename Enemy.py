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
        
    def change_direction(self):
        self.direction = 0 - self.direction

    def notice(self, char_x, char_y):
        print(self.direction)
        print("self.x = %s, char_x = %s" % (self.x,char_x))
        if ((self.x + 100  > char_x and self.direction == 1 and char_x > self. x) or (char_x + 100 > self.x  and self.direction == -1 and char_x < self.x)) and char_y == self.y :
            self.vx = 0
            self.standing = True
            return True
        return False   

