from Agent import Agent
import random
import numpy as np 


class BasicAgent(Agent): 
    def __init__(self, model, row, col, ID, hasParent=False, **kwargs):
        super().__init__(model, row, col, ID, hasParent, **kwargs)
        self.color = "red"

    
