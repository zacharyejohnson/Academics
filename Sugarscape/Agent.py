import random
from tkinter import * 

class Agent():
    def __init__(self, model, row, col, ID):
        self.model = model
        self.col = col
        self.row = row 
        self.dx = 0
        self.dy = 0
        self.id = ID
        self.vision = random.randint(1, self.model.max_vision )
        self.image = None
        #agents can only move to von neumann neighbors 
        self.move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.goods = {good:0 for good in self.model.goods}
        self.gui = self.model.GUI
        self.consumption_rate = {"sugar":0.5}

    #change row and col of agent and move image 
    def move(self): 
        move_patch = self.max_empty_neighbor()
        if move_patch is not None:
            self.move_image(move_patch)
            self.col = move_patch.col
            self.row = move_patch.row
            

    # move image of agent to desired row, col
    def move_image(self, patch):
        self.gui.canvas.move(self.image, 
                            (patch.col - self.col) * self.gui.dimPatch,
                            (patch.row - self.row) * self.gui.dimPatch)
        #self.model.GUI.canvas.update()

    #checks if identified patch is a real patch, i.e. is not out of bounds of the map
    def valid_patch(self, dx, dy):
        if(self.row + dy > 0 and self.row + dy < self.model.rows-1) and (self.col + dx > 0 and self.col + dx < self.model.cols-1): 
            return True
        else: 
            return False

    #checks if a patch can be moved to, i.e. no agent is already occupying the patch 
    def valid_move(self, dx, dy): 
        if(self.valid_patch(dx, dy) and self.model.patches_dict[self.row + dy][self.col + dy].agent == None): 
            return True
        else: 
            return False 

    # finds the von neumann neighbor with highest q and moves to it to consume 
    def max_empty_neighbor(self): 
        max_q = 0
        max_empty_neighbor = None
        random.shuffle(self.move_directions)
        for dy, dx in self.move_directions: 
            if self.valid_move(dx, dy):
                patch = self.model.patches_dict[self.row + dy][self.col + dx]
                if patch.Q > max_q: 
                    max_q = patch.Q
                    max_empty_neighbor = patch
        return max_empty_neighbor

    def harvest(self): 
        agent_patch = self.model.patches_dict[self.row][self.col]
        self.goods[agent_patch.good] += agent_patch.Q
        agent_patch.Q = 0

    def consume(self): 
        for good in self.goods: 
            self.goods[good] -= self.consumption_rate[good]








    


        