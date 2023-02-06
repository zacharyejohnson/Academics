from Agent import Agent
import random
import numpy as np 


class BasicAgent(Agent): 
    def __init__(self, model, row, col, ID, parent = None):
        super().__init__(model, row, col, ID, parent)
        self.color = "red"
        self.outline_width = 0
        self.parent = parent
        self.herder = False
        self.arbitrageur = False

    def select_breed_parameters(self, mutate, parent, herding = False, partner = None):
        good1 = self.model.goods[0]
        good2 = self.model.goods[1]
        self.exchange_target = random.choice(self.model.goods)
        self.not_exchange_target = good1 if self.exchange_target == good2 else good2

    def decrease_count(self): 
        if self.parent is not None:
            self.model.num_basicsbasics -= 1

    
