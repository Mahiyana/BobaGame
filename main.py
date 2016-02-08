#! /usr/bin/env python
import pyglet
from pyglet.window import key
import math

from Character import Character
from Platform import Platform
from CollectableItem import CollectableItem
from CollectionOfItems import CollectionOfItems
from Map import Map
from Level import Level
from Camera import *

config = pyglet.gl.Config(alpha_size=8, double_buffer=True)
window = pyglet.window.Window(config=config )
fps_display = pyglet.clock.ClockDisplay()

platform_width = 32
platform_height = 32
char_width = 32
char_height = 64

keys = key.KeyStateHandler()
window.push_handlers(keys)

state = Character("boba_standing_right","boba.png")
         
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
level.map.set_platform('trawa', 18, 3)
level.map.set_platform('trawa', 19, 3)
level.map.set_platform('trawa', 20, 3)
level.map.set_platform('trawa', 22, 3)
level.map.set_platform('trawa', 23, 3)
level.map.set_platform('trawa', 24, 3)
level.map.set_platform('trawa', 26, 5)
level.map.set_platform('trawa', 27, 5)
level.map.set_platform('trawa', 30, 1)
level.map.set_platform('trawa', 31, 1)
level.map.set_platform('trawa', 32, 1)
level.map.set_platform('trawa', 34, 3)
level.map.set_platform('trawa', 35, 3)

level.map.items.add_item(CollectableItem("star",200,200,20,20)) 
level.map.items.add_item(CollectableItem("star",250,150,20,20)) 
level.map.items.add_item(CollectableItem("star",500,300,20,20)) 
level.map.items.add_item(CollectableItem("star",800,300,20,20)) 

background_img = pyglet.resource.image("background.png")
background = pyglet.sprite.Sprite(background_img)

@window.event
def on_draw():
    window.clear()
    background.draw()
    level.map.draw()
    state.draw()
    fps_display.draw()
    window.flip()

def update(dt):
    if keys[key.RIGHT]:
        state.vx += (1 - state.vx)*5.0*dt
        if state.vx > 1:
            state.vx = 1
        state.right()
    elif keys[key.LEFT]:
        state.vx += (-1 - state.vx)*5.0*dt
        if state.vx < -1:
            state.vx = -1
        state.left()
    elif -0.1 < state.vx < 0.1:
        state.vx = 0
    elif state.vx > 0:
        state.vx = state.vx/(1+dt*10)
    elif state.vx < 0:
        state.vx = state.vx/(1+dt*10)

    if keys[key.SPACE]:
         state.jump() 
    
    if keys[key.X]:
        state.punch()

    old_x, old_y = state.x, state.y
    state.x += state.vx * dt * 500
    state.y += state.vy * dt * 500
    state.check_borders(window.width, window.height)
    state.vy -= 7 * dt
    new_xy = level.map.collision(old_x, old_y, state.x, state.y, state.width, state.height)
    state.update_xy(new_xy, old_y)
    level.map.items.collision(state.x, state.y)
    camera.x = state.x - 0.5 * window.width

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
