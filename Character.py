import pyglet
from Sprite import Sprite
from BulletsCollection import BulletsCollection
from Bullet import Bullet

class Character(Sprite):
    dx = 0
    dy = 0 
    vy = 0
    vx = 0
    ay = 0
    ax = 0
    lives = 3
    shot_cooldown = 0
    def __init__(self,name,grid):
        super().__init__(name)
        grid_image = pyglet.image.load(grid)
        grid_seq = pyglet.image.ImageGrid(grid_image, 2, 4)
        self.standing_left = grid_seq[4]
        self.animation_left = pyglet.image.Animation.from_image_sequence(grid_seq[4:7],0.1,True)
        self.shot_left = grid_seq[7]

        self.standing_right = grid_seq[0]
        self.animation_right = pyglet.image.Animation.from_image_sequence(grid_seq[0:3],0.1,True)
        self.shot_right = grid_seq[3]

    standing = True
    standing_x = True
    last_direction = 0

    def draw(self):
        if self.vx < 0 and self.image != self.animation_left:
            self.last_direction = -1
            self.image = self.animation_left
        elif self.vx > 0 and self.image != self.animation_right:
            self.last_direction = 1
            self.image = self.animation_right
        elif self.vx == 0 and self.image == self.animation_right:
            self.image = self.standing_right
        elif self.vx == 0 and self.image == self.animation_left:
            self.image = self.standing_left

        return super().draw()
     
    def jump(self):
        if self.standing:
            self.vy = 2
            self.standing = False
    
    def move(self, dt, moving):
        if moving == 1: #move right
            self.vx += (1 - self.vx)*5.0*dt
            if self.vx > 1:
                self.vx = 1
        elif moving == -1: #move left
            self.vx += (-1 - self.vx)*5.0*dt
            if self.vx < -1:
                self.vx = -1
        elif -0.1 < self.vx < 0.1:
            self.vx = 0
        elif self.vx > 0:
            self.vx = self.vx/(1+dt*10)
        elif self.vx < 0:
            self.vx = self.vx/(1+dt*10)


    def shot(self):
        if self.shot_cooldown <= 0:
            if self.last_direction < 0:
                self.image = self.shot_left
                right = False
                bullet =  Bullet("bullet",self.x, self.y + int(0.75*self.height), right)
            else:
                self.image = self.shot_right
                right = True
                bullet =  Bullet("bullet",self.x + self.width, self.y + int(0.75*self.height), right)
            self.shot_cooldown = 20
            return bullet
        else:
            return False
    
    def check_borders(self, window_width, window_height):
        if self.x < 0: self.x = 0
        elif self.x > 2*window_width - self.width: self.x = 2*window_width - self.width
        
        if self.y <= 0: 
            self.y = 0
            self.standing = True
            self.vy = 0
        elif self.y > window_height - self.height: self.y = window_height - self.height

    def update_xy(self, dt, new_xy, old_y):
        self.vy -= 7 * dt
        if new_xy:
          if new_xy[0]:
              self.x = new_xy[0]
              self.vx = 0
          
          if new_xy[1]:
              self.y = new_xy[1]
              self.vy = 0
              if new_xy[1] == old_y:
                  self.standing = True

    def update_bullets(self, bullets):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        for bullet in bullets:
            if self.x < bullet.x < self.x + self.width and self.y < bullet.y < self.y + self.height:
                self.lives -= 1
                bullets.remove(bullet)
