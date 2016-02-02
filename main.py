#! /usr/bin/env python
import pyglet
from pyglet.window import key
import math
from intersection import intersection

config = pyglet.gl.Config(alpha_size=8, double_buffer=True)
window = pyglet.window.Window(config=config )
fps_display = pyglet.clock.ClockDisplay()

image = pyglet.resource.image('postac.png')
postac = pyglet.sprite.Sprite(image)
keys = key.KeyStateHandler()
window.push_handlers(keys)
class Player:
    dx = 0
    dy = 0 
    vy = 0
    vx = 0
    ay = 0
    ax = 0 
    standing = True
    
    def jump(self):
        if self.standing:
            self.vy = 2
            self.standing = False

state = Player()

class Platforma(pyglet.sprite.Sprite):
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
        self.map[x][y] = platform = Platforma(name)
        platform.x = x * 32
        platform.y = y * 32

    def kolizja(self, xp, yp, xk, yk, w, h):
        xp, yp, xk, yk = int(xp), int(yp), int(xk), int(yk)
        min_x = int(xk/32)
        max_x = min([self.width-1, math.ceil((xk+w)/32)])
        min_y = int(yk/32)
        max_y = min([self.height-1, math.ceil((yk+h)/32)])

        range_x = range(min_x, max_x)
        if xp > xk: range_x = reversed(range_x)
        for x in range_x:
            range_y = range(min_y, max_y)
            if yp > yk: range_y = reversed(range_y)
            for y in range_y:
                if self.map[x][y]:
                    nx, ny = xp, yp
                    left, right, up, down = 9001, 9001, 9001, 9001
                    if x*32 <= xk < (x+1)*32:
                        left = (x+1)*32-xk
                        nx = (x+1)*32
                    if x*32 <= xk+w < (x+1)*32:
                        right = xk+w - x*32
                        nx = x*32 - w
                    if y*32 <= yk < (y+1)*32:
                        up = (y+1)*42-yk
                        ny = (y+1)*32
                    if y*32 <= yk+h < (y+1)*32:
                        down = yk+h - y*32
                        ny = y*32 - h

                    if min([left, right]) < min([up, down]):
                        return (nx, None)
                    else:
                        return (None, ny)
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
    postac.draw()
    fps_display.draw()
    window.flip()

def update(dt):
    state.vx = 0
    if keys[key.RIGHT]:
            state.vx = 1
    if keys[key.LEFT]:
            state.vx = -1
    if keys[key.SPACE]:
         state.jump() 

    old_x, old_y = postac.x, postac.y
    postac.x += state.vx * dt * 500
    if postac.x < 0: postac.x = 0
    elif postac.x > window.width - postac.width: postac.x = window.width - postac.width
    postac.y += state.vy * dt * 500
    if postac.y <= 0: 
        postac.y = 0
        state.standing = True
        state.vy = 0
    elif postac.y > window.height - postac.height: postac.y = window.height - postac.height
    state.vy -= 9.82 * dt
    new_xy = level.map.kolizja(old_x, old_y, postac.x, postac.y, postac.width, postac.height)
    if new_xy:
        print(new_xy)
        if new_xy[0]:
            postac.x = new_xy[0]
            state.vx = 0
            postac_y = old_y
        if new_xy[1]:
            postac.y = new_xy[1]
            state.vy = 0
            state.standing = True
            postac.x = old_x

    

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
