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
from Enemy import Enemy

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

enemy = Enemy("han_right","han.png",150,32)

@window.event
def on_draw():
    window.clear()
    #background.draw()
    level.map.draw()
    state.draw()
    fps_display.draw()
    enemy.draw()
    window.flip()

def update(dt):
    moving = None
    if keys[key.RIGHT]:
        moving = 1 
    elif keys[key.LEFT]:
        moving = -1
    
    if keys[key.SPACE]:
         state.jump() 
    
    if keys[key.X]:
        level.map.bullets.add_bullet(state.shot())

    state.move(dt,moving)

    old_x, old_y = state.x, state.y
    state.x += state.vx * dt * 500
    state.y += state.vy * dt * 500
    state.check_borders(window.width, window.height)
    new_xy = level.map.collision(old_x, old_y, state.x, state.y, state.width, state.height)
    state.update_xy(dt, new_xy, old_y)
    level.map.items.collision(state.x, state.y)
    camera.x = state.x - 0.5 * window.width
    level.map.update_bullets()
    state.update_bullets()
    level.map.bullet_collision()

    old_enem_x, old_enem_y = enemy.x, enemy.y
    enemy.move_self(dt)
    new_enem_xy = level.map.collision(old_enem_x, old_enem_y, enemy.x, enemy.y, enemy.width, enemy.height)
    will_fall = level.map.collision(enemy.x + enemy.direction*enemy.width+enemy.vx*20, old_enem_y, enemy.x + enemy.direction*enemy.width+enemy.vx*20, old_enem_y-1, enemy.width, enemy.height)
    will_fall = not (will_fall and will_fall[1] == old_enem_y)
    enemy.check_borders(window.width, window.height)
    if new_enem_xy:
        if new_enem_xy[0] :
            enemy.change_direction() 
    if will_fall:
        enemy.y = old_enem_y
        enemy.x = old_enem_x
        enemy.change_direction()
    enemy.update_xy(dt, new_enem_xy, old_enem_y)
            
    if enemy.notice(state.x, state.y): level.map.bullets.add_bullet(enemy.shot())
    enemy.update_bullets()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
