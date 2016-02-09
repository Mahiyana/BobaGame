from Bullet import Bullet

class BulletsCollection:
    collection = []

    def add_bullet(self, item):
       if item: self.collection.append(item)

    def draw(self):
        for item in self.collection:
            #print("%s, %s" % (item.x,item.y) )
            #print("draw")
            item.draw()
            #print("drawn")
            #print("%s, %s" % (item.x,itey) )

    def update(self):
       for item in self.collection:
           if item.span <= 0:
               self.collection.remove(item)
           else:    
               item.update()

    def collision(self,char_x,char_y):
        for item in self.collection:
            if(char_x < item.x < char_x + char_width or char_x < item.x + item.width < char_x + char_width) and (char_y < item.y < char_y + char_height or char_y < item.y + item.height < char_y + char_height):
                    self.collection.remove(item)
 
