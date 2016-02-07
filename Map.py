from CollectionOfItems import CollectionOfItems
from Platform import Platform
import math

platform_width = 32
platform_height = 32

class Map:
    map = None
    items = CollectionOfItems()
    map_x = 0
    map_y = 0

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
        self.items.draw()        

    def set_platform(self, name, x, y):
        self.map[x][y] = platform = Platform(name)
        platform.x = x * platform_width
        platform.y = y * platform_height

    def redraw_right(self,char_x):
       for column in self.map:
           for cell in column:
               if not cell: continue
               cell.x = cell.x - char_x

    def redraw_left(self,char_x):
       for column in self.map:
           for cell in column:
               if not cell: continue
               cell.x = cell.x + char_x


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
        new_x = xk
        new_y = yk
        col_x, col_y = False, False
        if xp > xk: range_x = reversed(range_x)
        for x in range_x:
            range_y = range(min_y, max_y)
            if yp > yk: range_y = reversed(range_y)
            for y in range_y:
                if self.map[x][y]: # and self.check_collision_points(xk,yk,x,y): 
                    if not (xk > (x+1)*platform_width or xk+w < x*platform_width) and not (yp+h <= y*platform_height or yp >= (y+1)*platform_height):
                        if xp < x*platform_width:
                            new_x = x*platform_width - w
                        elif xp > x*platform_width:
                            new_x = (x+1)*platform_width
                        col_x = True
                    
                    if not (yk > (y+1)*platform_height or yk+h < y*platform_height) and not (new_x+w <= x*platform_width or new_x >= (x+1)*platform_width):
                        if yp < y*platform_height:
                            new_y = y*platform_height - h
                        elif yp > y*platform_height:
                            new_y = (y+1)*platform_height
                        col_y = True
                    
                    if col_x and col_y: return (new_x, new_y)
                    if(col_x): return (new_x, None)
                    if(col_y): return (None, new_y)
          
        return False
 
