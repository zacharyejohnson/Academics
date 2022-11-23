from Agent import Agent 
import random
import numpy as np 

class Herder(Agent): 
    def __init__(self, model, row, col, ID, hasParent, **kwargs):
        super().__init__(model, row, col, ID, hasParent, **kwargs)
        self.wealthiest = self
        self.color = "lime"
    
    # the main tactic employed by herders is the herding
    # of traits seen in more wealthy trading partners 
    def trade(self): 
        super().trade()
        def herd_traits(partner): 
            if self.model.genetic:
                    for attr, val in partner.copy_attributes.items():
                        if random.random() < self.model.cross_over_rate:
                            setattr(self, attr, val)
            else: 
                    for attr, val in partner.copy_attributes.items():
                        setattr(self, attr, val)

        if self.partner != None: 
            if self.partner.wealth() > self.top_wealth:
                herd_traits(self.partner)
                self.wealthiest = self.partner
                self.top_wealth = self.partner.wealth()
    def update_params(self):
        super().update_params()
        if self.wealthiest != self: 
            self.top_wealth *= .99
