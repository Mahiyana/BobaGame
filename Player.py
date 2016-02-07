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
            self.vx = -1
            #print(self.vy)
            self.standing_x = False
            self.last_direction = "left"

    def right(self):
        if self.standing_x:
            self.postac = self.postac.move_right()
            self.vx = 1
            #print(self.vy)
            self.standing_x = False    
            self.last_direction = "right"
    
    def stop_left(self):
        self.postac = self.postac.stand_left()
        self.standing_x = True
        self.vx = 0

    def stop_right(self):
        self.postac = self.postac.stand_right()
        self.standing_x = True
        self.vx = 0
    
    def stop_moving(self):
        if self.last_direction == "left":
            self.stop_left()
        else:
            self.stop_right()

    def check_borders(self, window_width, window_height):
        if self.postac.x < 0: self.postac.x = 0
        elif self.postac.x > window_width - self.postac.width: self.postac.x = window_width - self.postac.width
        
        if self.postac.y <= 0: 
            self.postac.y = 0
            self.standing = True
            self.vy = 0
        elif self.postac.y > window_height - self.postac.height: self.postac.y = window_height - self.postac.height

    def update_xy(self, new_xy, old_y):
        if new_xy:
          #print(new_xy)
          if new_xy[0]:
              self.postac.x = new_xy[0]
              self.vx = 0
          
          if new_xy[1]:
              self.postac.y = new_xy[1]
              self.vy = 0
              if new_xy[1] == old_y:
                  self.standing = True
   
