class BulletsCollection:
    collection = []

    def add_bullet(self, item):
       self.collection.append(item)

    def draw(self):
        for item in self.collection:
            item.draw()

    def update(self):
       for item in self.collection:
           item.update()

    def collision(self,char_x,char_y):
        for item in self.collection:
            if(char_x < item.x < char_x + char_width or char_x < item.x + item.width < char_x + char_width) and (char_y < item.y < char_y + char_height or char_y < item.y + item.height < char_y + char_height):
                    collection.remove(item)
 
