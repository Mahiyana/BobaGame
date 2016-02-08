import pyglet
from Sprite import Sprite

class Character(Sprite):
    dx = 0
    dy = 0 
    vy = 0
    vx = 0
    ay = 0
    ax = 0
    def __init__(self,name,grid):
        super().__init__(name)
        grid_image = pyglet.image.load(grid)
        grid_seq = pyglet.image.ImageGrid(grid_image, 2, 3)
        self.standing_left = grid_seq[3]
        self.moving_left_1 = grid_seq[4]
        self.moving_left_2 = grid_seq[5]
        self.animation_left = pyglet.image.Animation.from_image_sequence([
            self.standing_left, self.moving_left_1, self.moving_left_2],0.1,True)

        self.standing_right = grid_seq[0]
        self.moving_right_1 = grid_seq[1]
        self.moving_right_2 = grid_seq[2]
        self.animation_right = pyglet.image.Animation.from_image_sequence([
            self.standing_right, self.moving_right_1, self.moving_right_2],0.1,True)


    standing = True
    standing_x = True
    last_direction = None
     
    def jump(self):
        if self.standing:
            self.vy = 2
            self.standing = False
    
    def left(self):
        if self.standing_x:
            self.image = self.animation_left
            self.vx = -1
            #print(self.vy)
            self.standing_x = False
            self.last_direction = "left"

    def right(self):
        if self.standing_x:
            self.image = self.animation_right
            self.vx = 1
            self.standing_x = False    
            self.last_direction = "right"
    
    def stop_left(self):
        self.image = self.standing_left
        self.standing_x = True
        self.vx = 0

    def stop_right(self):
        self.image = self.standing_right
        self.standing_x = True
        self.vx = 0
    
    def stop_moving(self):
        if self.last_direction == "left":
            self.stop_left()
        else:
            self.stop_right()

    def check_borders(self, window_width, window_height):
        if self.x < 0: self.x = 0
        elif self.x > 2*window_width - self.width: self.x = 2*window_width - self.width
        
        if self.y <= 0: 
            self.y = 0
            self.standing = True
            self.vy = 0
        elif self.y > window_height - self.height: self.y = window_height - self.height

    def update_xy(self, new_xy, old_y):
        if new_xy:
          if new_xy[0]:
              self.x = new_xy[0]
              self.vx = 0
          
          if new_xy[1]:
              self.y = new_xy[1]
              self.vy = 0
              if new_xy[1] == old_y:
                  self.standing = True
   
