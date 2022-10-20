import random

class Agent():
    def __init__(self, model, row, col, ID):
        self.model = model
        self.col = col
        self.row = row 
        self.dx = 0
        self.dy = 0
        self.id = ID
        self.vision = random.randint(1, self.model.max_vision )
        