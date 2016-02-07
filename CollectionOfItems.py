char_width = 32
char_height = 64

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


