import copy
from Agent import Agent
import random
import numpy as np 
from scipy.stats import gmean

class Arbitrageur(Agent): 
    def __init__(self, model, row, col, ID, parent):
        super().__init__(model, row, col, ID, parent)
        self.color = "magenta"
        self.arbitrageur = True
        self.herder = False 
        # is this a good range for arb vision? 
        #self.arbitrageur_vision = random.randint(50, 1000)

    def select_breed_parameters(self, mutate, parent, herding = False, partner = None): 
            # no herding is done
            def  generate_breed_parameters(): 
                inheritance = parent.define_inheritance()
                min_denominator = 10 if not mutate or "present_price_weight" not in inheritance else\
                        int(inheritance["present_price_weight"] / (1 + self.mutate_rate))
                max_denominator = 100 if not mutate  or "present_price_weight" not in inheritance else\
                    int(inheritance["present_price_weight"] * (1 + self.mutate_rate))
                self.present_price_weight = random.randint(
                    min_denominator, max_denominator)
                self.expected_price = self.reservation_demand["sugar"]["price"]

            if not herding: 
                   generate_breed_parameters()





    def decrease_count(self): 
        self.model.num_arbitrageursbasics -= 1
    
        
    def update_params(self):
        super().update_params()
        #arbitrageur exchanges for the good that is cheaper than his WTP
        WTP = self.reservation_demand["sugar"]["price"] 
        if self.expected_price > WTP:
                    self.exchange_target, self.not_exchange_target = "sugar", "water"  
        else: 
                    self.exchange_target, self.not_exchange_target = "water", "sugar"

    # def trade(self):
    #     super().trade()
        # arbitrageur uses n prevous prices to determine a goods expected price once they have made enough trades, 
        # otherwise expected price is just set at the reservation demand of the agent 
        # if len(self.agent_transaction_prices) > self.arbitrageur_vision:
        #     self.expected_price = gmean(self.agent_transaction_prices[:self.arbitrageur_vision])

    

    
        


