import random

class MazeEngine:
    def __init__(self, size=3):
        self.size = size
        self.reset()

    def reset(self):
        self.x, self.y = 0, 0 
        self.inventory = []
        self.rooms = {}
        
        # Room Types -> 0: Hallway, 1: Key Room, 2: Portal
        types = [0] * 9
        key_spots = random.sample(range(1, 8), 3)
        for spot in key_spots: types[spot] = 1
        types[8] = 2 

        for i, t in enumerate(types):
            self.rooms[(i % 3, i // 3)] = t

    def move(self, direction):
        old_pos = (self.x, self.y)
        if direction == "north" and self.y < self.size - 1: self.y += 1
        elif direction == "south" and self.y > 0: self.y -= 1
        elif direction == "east" and self.x < self.size - 1: self.x += 1
        elif direction == "west" and self.x > 0: self.x -= 1
        return (self.x, self.y) != old_pos