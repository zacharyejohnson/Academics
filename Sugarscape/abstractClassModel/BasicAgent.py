from Agent import Agent
import random
import numpy as np 


class BasicAgent(Agent): 
    def __init__(self, model, row, col, ID, has_parent=False, **kwargs):
        super().__init__(model, row, col, ID, has_parent, **kwargs)
        self.color = "red"

    
