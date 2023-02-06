from Arbitrageur import Arbitrageur
from Agent import Agent
import random

class ArbitrageurHerder(Arbitrageur): 
    def __init__(self, model, row, col, ID, parent):
        super().__init__(model, row, col, ID, parent)
        self.outline_width = 2
        self.wealthiest = self
        self.herder = True
        self.arbitraguer = True

    def select_breed_parameters(self, mutate, parent, herding, partner):
        super().select_breed_parameters(mutate, parent, herding, partner)
        def generate_breed_parameters(): 
            inheritance = parent.define_inheritance() if parent is not None else None
            #herder attributes
            self.wealthiest = parent if inheritance is not None else self
            self.top_wealth = parent.get_wealth() if inheritance is not None else self.get_wealth()

        def copy_partner_parameters(): 
            if not hasattr(self, "top_wealth"):
                self.top_wealth = partner.get_wealth()
                self.wealthiest = partner
            if not hasattr(self, "expected_price"):                        
                        self.expected_price = partner.expected_price
            if not hasattr(self, "present_price_weight"):                    
                        self.present_price_weight = partner.present_price_weight 

        if herding: 
             copy_partner_parameters()
        else: 
             generate_breed_parameters()

    def decrease_count(self): 
        self.model.num_arbitrageursherders -= 1
                

    def update_params(self):
        super().update_params()

        if self.get_wealth() != self.top_wealth: 
            self.wealthiest = self
        if self.wealthiest != self: 
             self.top_wealth *= .999
