class GlobeGrid:
    def __init__(self, size=10, theme="Deep Sea"):
        self.size = size
        self.theme = theme
        self.x, self.y = 0, 0
        # The 3 items to find
        self.items = {(3, 4): "Golden Key", (7, 2): "Crystal Shard", (5, 8): "Ancient Emblem"}
        self.inventory = []

    def move(self, direction):
        if direction == "north": self.y = (self.y + 1) % self.size
        elif direction == "south": self.y = (self.y - 1) % self.size
        elif direction == "east": self.x = (self.x + 1) % self.size
        elif direction == "west": self.x = (self.x - 1) % self.size
        return self.get_state()

    def get_state(self):
        item_here = self.items.get((self.x, self.y))
        prompt = (
            f"A high-quality 2D top-down RPG map tile of a {self.theme}. "
            f"Perspective: Direct overhead bird's-eye view. Detailed textures, no characters."
        )
        if item_here:
            prompt += f" In the center, there is a glowing {item_here} on a stone altar."
            
        return {
            "pos": (self.x, self.y),
            "prompt": prompt,
            "item_found": item_here
        }