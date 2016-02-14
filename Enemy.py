import pyglet
from Character import Character

class Enemy(Character):
    direction = 1
    def __init__(self,name,grid,x,y):
        super().__init__(name,grid)
        self.x = x
        self.y = y

    def move_self(self,dt):
        self.x += self.vx * dt * 500
        self.y += self.vy * dt * 500
        self.move(dt, self.direction)
        
    def change_direction(self):
        self.direction = 0 - self.direction

    def notice(self, char_x, char_y):
        print(self.x, char_x, self.direction)
        if ((self.x + 100  > char_x and self.direction == 1 and char_x > self. x) or (char_x + 100 > self.x  and self.direction == -1 and char_x < self.x)) and char_y == self.y :
            self.vx = 0
            self.standing = True
            return True
        return False   

    def update_all(self, level, dt, window_width, window_height, char_x, char_y):
        old_enem_x, old_enem_y = self.x, self.y
        self.move_self(dt)
        new_enem_xy = level.map.collision(old_enem_x, old_enem_y, self.x, self.y, self.width, self.height)
        will_fall = level.map.collision(self.x + self.direction*self.width+self.vx*20, old_enem_y, self.x + self.direction*self.width+self.vx*20, old_enem_y-1, self.width, self.height)
        will_fall = not (will_fall and will_fall[1] == old_enem_y)
        self.check_borders(window_width, window_height)
        if new_enem_xy:
            if new_enem_xy[0] :
                self.change_direction() 
        if will_fall:
            self.y = old_enem_y
            self.x = old_enem_x
            self.change_direction()
        self.update_xy(dt, new_enem_xy, old_enem_y)
                
        if self.notice(char_x, char_y): level.map.bullets.add_bullet(self.shot())
        self.update_bullets()

