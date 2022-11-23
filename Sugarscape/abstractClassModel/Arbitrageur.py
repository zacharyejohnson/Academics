import copy
from Agent import Agent
import random
import numpy as np 

class Arbitrageur(Agent): 
    def __init__(self, model, row, col, ID, hasParent, **kwargs):
        super().__init__(model, row, col, ID, hasParent, **kwargs)
        self.color = "magenta"
        # if average prices is below price agent believes is correct,
        min_denominator = 10 if not model.mutate or "present_price_weight" not in kwargs else\
            int(kwargs["present_price_weight"] / (1 + self.mutate_rate))
        max_denominator = 100 if not model.mutate  or "present_price_weight" not in kwargs else\
            int(kwargs["present_price_weight"] * (1 + self.mutate_rate))
        self.present_price_weight = random.randint(min_denominator, max_denominator)
        self.expected_price = self.reservation_demand["sugar"]["price"]
        targets = copy.copy(self.model.goods)
        random.shuffle(targets)
        self.target = targets.pop()
        self.not_target = targets[0]

    def update_params(self):
        super().update_params()
        # arbitrageur exchanges for the good that is cheaper than his WTP
        WTP = self.reservation_demand["sugar"]["price"] 
        self.exchange_target = "sugar" if self.expected_price < WTP else "water"
        self.not_exchange_target = "water" if self.exchange_target == "sugar" else "sugar"