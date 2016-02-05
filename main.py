#! /usr/bin/env python
import pyglet
from pyglet.window import key
import math

config = pyglet.gl.Config(alpha_size=8, double_buffer=True)
window = pyglet.window.Window(config=config )
fps_display = pyglet.clock.ClockDisplay()

platform_width = 32
platform_height = 32
char_width = 32
char_height = 64
collision_points = [[9,9],[32,0],[9,54],[32,32],[54,54],[32,64],[9,54],[0,32]] 

keys = key.KeyStateHandler()
window.push_handlers(keys)

class Character(pyglet.sprite.Sprite):
        
    def __init__(self,image):
        super().__init__(image)
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
     
    postac = Character(pyglet.image.load("boba_standing_right.png"))
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

    def __init__(self,width,height):
        self.map = Map(width,height)

class CollectibleItem(pyglet.sprite.Sprite):
    def __init__(self, name,x,y,width,height):
       #self.width = width
       #self.height = height
        self.taken = False
        image = pyglet.resource.image(name+".png")
        super().__init__(image)
        self.x = x
        self.y = y
        

class CollectionOfItems():
    collection = []

    def add_item(self,item):
        self.collection.append(item)

    def draw(self):
        for item in self.collection:
            if not item.taken:
                item.draw()

    def collision(self,char_x,char_y):
        for item in self.collection:
            if not item.taken:
                if(char_x < item.x < char_x + char_width or char_x < item.x + item.width < char_x + char_width) and (char_y < item.y < char_y + char_height or char_y < item.y + item.height < char_y + char_height):
                        item.taken = True

level = Level(100,100)
level.map.set_platform('trawa', 4, 3)
level.map.set_platform('trawa', 4, 4)
level.map.set_platform('trawa', 4, 5)
level.map.set_platform('trawa', 5, 0)
level.map.set_platform('trawa', 6, 0)
level.map.set_platform('trawa', 7, 0)
level.map.set_platform('trawa', 10, 3)
level.map.set_platform('trawa', 11, 3)
level.map.set_platform('trawa', 12, 3)
level.map.set_platform('trawa', 14, 5)
level.map.set_platform('trawa', 15, 5)
level.map.set_platform('trawa', 16, 5)

items = CollectionOfItems()
items.add_item(CollectibleItem("star",200,200,20,20)) 
items.add_item(CollectibleItem("star",250,150,20,20)) 
items.add_item(CollectibleItem("star",500,300,20,20)) 

background_img = pyglet.resource.image("background.png")
background = pyglet.sprite.Sprite(background_img)

@window.event
def on_draw():
    window.clear()
    background.draw()
    level.map.draw()
    state.postac.draw()
    fps_display.draw()
    items.draw()
    window.flip()

def update(dt):
    state.vx = 0
    if keys[key.RIGHT]:
        state.vx = 1
        state.right()

    if keys[key.LEFT]:
        state.vx = -1
        state.left()
    
    if not(keys[key.RIGHT] or keys[key.LEFT]):
        state.stop_moving()

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
        #print(new_xy)
        if new_xy[0]:
            state.postac.x = new_xy[0]
            state.vx = 0
        
        if new_xy[1]:
            state.postac.y = new_xy[1]
            state.vy = 0
            state.standing = True
            state.postac.x = old_x
    items.collision(state.postac.x, state.postac.y)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
