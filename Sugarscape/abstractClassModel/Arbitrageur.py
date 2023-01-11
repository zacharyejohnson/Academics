import copy
from Agent import Agent
import random
import numpy as np 
from scipy.stats import gmean

class Arbitrageur(Agent): 
    def __init__(self, model, row, col, ID, hasParent, **kwargs):
        super().__init__(model, row, col, ID, hasParent, **kwargs)
        self.color = "magenta"
        
    def update_params(self):
        super().update_params()
        #arbitrageur exchanges for the good that is cheaper than his WTP
        WTP = self.reservation_demand["sugar"]["price"] 
        self.exchange_target = "sugar" if self.expected_price < WTP else "water"
        


