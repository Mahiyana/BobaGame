#! /usr/bin/env python
import pyglet
from pyglet.window import key
import math
from intersection import intersection

config = pyglet.gl.Config(alpha_size=8, double_buffer=True)
window = pyglet.window.Window(config=config )
fps_display = pyglet.clock.ClockDisplay()

platform_width = 32
platform_height = 32
collision_points = [[9,9],[32,0],[9,54],[32,32],[54,54],[32,64],[9,54],[0,32]] 

keys = key.KeyStateHandler()
window.push_handlers(keys)

class Character(pyglet.sprite.Sprite):
    def __init__(self,image):
        super().__init__(image)

    def move_left(self):
        self.image = pyglet.image.load("boba_standing_left.png")
        print("ODWRACAM SIEM W LEWO")
        return self

    def move_right(self):
        print("ODWRACAM SIEM W PRAWO")
        self.image = pyglet.image.load("boba_standing_right.png")
        return self

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
     
    postac = Character(pyglet.image.load("boba_standing_right.png"))
    def jump(self):
        if self.standing:
            self.vy = 2
            self.standing = False
    def left(self):
        self.postac = self.postac.move_left()

    def right(self):
        self.postac = self.postac.move_right()


state = Player()

class Platform(pyglet.sprite.Sprite):
    def __init__(self, name):
        image = pyglet.resource.image(name+".png")
        super().__init__(image)

class Map:
    map = None

    def __init__(self, width=10, height=10):
        self.map = []
        self.width = width
        self.height = height
        for x in range(width):
            column = []
            self.map.append(column)

            for y in range(height):
                column.append(None)

    def draw(self):
        for column in self.map:
            for cell in column:
                if not cell: continue
                cell.draw()

    def set_platform(self, name, x, y):
        self.map[x][y] = platform = Platform(name)
        platform.x = x * platform_width
        platform.y = y * platform_height

    def check_collision_points(self, x_postaci, y_postaci, x_platform, y_platform):
      for point in collision_points:
        if(x_platform*platform_width < point[0] + x_postaci < (x_platform+1)*platform_width) and (y_platform*platform_height < point[1] + y_postaci < (y_platform+1)*platform_height):
            return True
      return False


    def collision(self, xp, yp, xk, yk, w, h):
        xp, yp, xk, yk = int(xp), int(yp), int(xk), int(yk)
       
        min_x = int(xk/platform_width)
        max_x = min([self.width-1, math.ceil((xk+w)/platform_width)])
        min_y = int(yk/platform_height)
        max_y = min([self.height-1, math.ceil((yk+h)/platform_height)])
        

        range_x = range(min_x, max_x)
        new_x = None
        new_y = None
        if xp > xk: range_x = reversed(range_x)
        for x in range_x:
            range_y = range(min_y, max_y)
            if yp > yk: range_y = reversed(range_y)
            for y in range_y:
                if self.map[x][y]: # and self.check_collision_points(xk,yk,x,y): 
                    if(xk+w<x*platform_width or (x+1)*platform_width > xk):  #(x*platform_width < xk < (x+1)*platform_width or x*platform_width < xk+w < (x+1)*platform_width):
                        if(xp+w <= x*platform_width): #left side
                            new_x = x*platform_width - w
                        elif(x*platform_width<xp): #right side
                            new_x = (x+1)*platform_width
                    
                    if(yk+h<y*platform_width or (y+1)*platform_height > yk):  #(y*platform_height < yk < (y+1)*platform_width):
                        if(yp<y*platform_height): #under
                            new_y = y*platform_height - h
                        else:
                            new_y = (y+1)*platform_height
                    
                    if(new_x): return (new_x, None)
                    if(new_y): return (None, new_y)
          
        return False
          
class Level:
    map = None

    def __init__(self):
        self.map = Map()

level = Level()
level.map.set_platform('trawa', 4, 3)
level.map.set_platform('trawa', 4, 4)
level.map.set_platform('trawa', 4, 5)
level.map.set_platform('trawa', 5, 0)
level.map.set_platform('trawa', 6, 0)
level.map.set_platform('trawa', 7, 0)

@window.event
def on_draw():
    window.clear()
    level.map.draw()
    state.postac.draw()
    fps_display.draw()
    window.flip()

def update(dt):
    state.vx = 0
    if keys[key.RIGHT]:
        state.vx = 1
        state.right()

    if keys[key.LEFT]:
        state.vx = -1
        state.left()

    if keys[key.SPACE]:
         state.jump() 

    old_x, old_y = state.postac.x, state.postac.y
    
    state.postac.x += state.vx * dt * 500
    state.postac.y += state.vy * dt * 500
    
    if state.postac.x < 0: state.postac.x = 0
    elif state.postac.x > window.width - state.postac.width: state.postac.x = window.width - state.postac.width
    
    if state.postac.y <= 0: 
        state.postac.y = 0
        state.standing = True
        state.vy = 0
    elif state.postac.y > window.height - state.postac.height: state.postac.y = window.height - state.postac.height
   
    state.vy -= 9.82 * dt
    new_xy = level.map.collision(old_x, old_y, state.postac.x, state.postac.y, state.postac.width, state.postac.height)
    if new_xy:
        print(new_xy)
        if new_xy[0]:
            state.postac.x = new_xy[0]
            state.vx = 0
            postac_y = old_y
        if new_xy[1]:
            state.postac.y = new_xy[1]
            state.vy = 0
            state.standing = True
            state.postac.x = old_x

    

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
