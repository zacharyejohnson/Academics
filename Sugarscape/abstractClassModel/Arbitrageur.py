import copy
from Agent import Agent
import random
import numpy as np 
from scipy.stats import gmean

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
        self.expected_price = {}
        for good in self.model.goods: 
            self.expected_price[good] = self.reservation_demand[good]["price"]
        

    def update_params(self):
        super().update_params()
        #arbitrageur exchanges for the good that is cheaper than his WTP
        for good in self.model.goods: 
            if len(self.transaction_prices[good]) > 0: 
                self.expected_price[good] = gmean(self.transaction_prices[good])
        good1 = random.choice(self.model.goods)
        good2 = self.model.goods[0] if good1 == self.model.goods[1] else self.model.goods[1]
        WTP = self.reservation_demand[good1]["price"] 
        if self.expected_price[good1] < WTP: 
            self.exchange_target = good1
            self.not_exchange_target = good2
        elif self.expected_price[good2] < self.reservation_demand[good2]["price"]: 
            self.exchange_target = good2 
            self.not_exchange_target = good1
        else:
            self.exchange_target = random.choice([good1, good2])
            self.not_exchange_target = good1 if self.exchange_target == good2 else good2

