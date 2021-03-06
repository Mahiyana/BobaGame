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
from EnemyCollection import EnemyCollection
from Sprite import Sprite


config = pyglet.gl.Config(alpha_size=8, double_buffer=True)
window = pyglet.window.Window(config=config )
fps_display = pyglet.clock.ClockDisplay()

platform_width = 32
platform_height = 32
char_width = 32
char_height = 64

keys = key.KeyStateHandler()
window.push_handlers(keys)

state = Character("boba_fett_right","boba_fett.png")
         
level = Level(100,100)
level.map.set_platform('sand', 4, 4)
level.map.set_platform('sand', 4, 5)
level.map.set_platform('sand', 5, 0)
level.map.set_platform('sand', 6, 0)
level.map.set_platform('sand', 7, 0)
level.map.set_platform('sand', 8, 0)
level.map.set_platform('sand', 9, 0)
level.map.set_platform('sand', 10, 0)
level.map.set_platform('sand', 14, 5)
level.map.set_platform('sand', 15, 5)
level.map.set_platform('sand', 16, 5)
level.map.set_platform('sand', 18, 3)
level.map.set_platform('sand', 19, 3)
level.map.set_platform('sand', 20, 3)
level.map.set_platform('sand', 21, 3)
level.map.set_platform('sand', 22, 3)
level.map.set_platform('sand', 23, 3)
level.map.set_platform('sand', 24, 3)
level.map.set_platform('sand', 26, 5)
level.map.set_platform('sand', 27, 5)
level.map.set_platform('sand', 30, 1)
level.map.set_platform('sand', 31, 1)
level.map.set_platform('sand', 32, 1)
level.map.set_platform('sand', 34, 3)
level.map.set_platform('sand', 35, 3)

level.map.items.add_item(CollectableItem("star",200,200,20,20)) 
level.map.items.add_item(CollectableItem("star",250,150,20,20)) 
level.map.items.add_item(CollectableItem("star",500,300,20,20)) 
level.map.items.add_item(CollectableItem("star",800,300,20,20)) 

background = Sprite("tatooine1")
background.x = (state.x - 0.5 * window.width)
background2 = Sprite("tatooine2")
background2.x = background.x + background.width

enemies = EnemyCollection()
han = Enemy("boba_fett_ghost_right","boba_fett_ghost.png",300,32)
han2 = Enemy("boba_fett_ghost_right","boba_fett_ghost.png",600,100)
enemies.add_enemy(han)
enemies.add_enemy(han2)

heart_image = pyglet.resource.image('heart.png')
heart = pyglet.sprite.Sprite(heart_image)
heart.x = window.width*0.9
heart.y = window.height*0.9
heart2 = pyglet.sprite.Sprite(heart_image)
heart2.x = window.width*0.9 - 25
heart2.y = window.height*0.9
heart3 = pyglet.sprite.Sprite(heart_image)
heart3.x = window.width*0.9 - 50
heart3.y = window.height*0.9

menu = pyglet.text.Label('Press SPACE to start the game',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    if camera.level == 0:
        window.clear()
        menu.draw()     
        window.flip()
    elif camera.level == 1: 
        window.clear()
        background.draw()
        background2.draw()
        
        level.map.draw()
        state.draw()
        fps_display.draw()
        enemies.draw() 
        if state.lives > 2:
            heart.draw()
        if state.lives > 1:
            heart2.draw() 
        if state.lives > 0:
            heart3.draw() 
        window.flip()

def update(dt):
       print(camera.level)
       if camera.level == 0:
           if keys[key.SPACE]:
               camera.level = 1
       elif camera.level == 1:
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
           
           if state.lives <= 0:
               state.x = 0
               state.y = 50
               state.lives = 3
               state.image = state.standing_right
 
           old_x, old_y = state.x, state.y
           state.x += state.vx * dt * 500
           state.y += state.vy * dt * 500
           state.check_borders(window.width, window.height)
           new_xy = level.map.collision(old_x, old_y, state.x, state.y, state.width, state.height)
           state.update_xy(dt, new_xy, old_y)
           level.map.items.collision(state.x, state.y)
           camera.x = state.x - 0.5 * window.width
           level.map.update_bullets()
           state.update_bullets(level.map.bullets.collection)
           level.map.bullet_collision()

           enemies.update_all(level, dt, window.width, window.height, state.x, state.y)
   # except NameError:
   #     print("NameError")
   #     level_counter = 0

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
