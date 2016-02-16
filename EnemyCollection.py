class EnemyCollection():
    collection = []

    def add_enemy(self,item):
        self.collection.append(item)

    def draw(self):
        for enemy in self.collection:
            if enemy.lives > 0:
                enemy.draw()


    def update_all(level, dt, window_width, window_height, state_x, state_y):
        for enemy in self.collection:
            if enemy.lives <= 0:
                self.collection.remove(enemy)
            else:    
                enemy.update_all(level, dt, window_width, window_height, state_x, state_y)
