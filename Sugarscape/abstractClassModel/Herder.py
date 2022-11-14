from Agent import Agent 
import random
import numpy as np 

class Herder(Agent): 
    def __init__(self, model, row, col, ID, has_parent=False, **kwargs):
        super().__init__(model, row, col, ID, has_parent, **kwargs)
        self.wealthiest = self
        self.top_wealth = self.wealth()
        self.color = "lime"
    
    # the main tactic employed by herders is the herding
    # of traits seen in more wealthy trading partners 
    def trade(self): 
        partner = super().trade()
        def herd_traits(partner): 
            if self.model.genetic:
                    for attr, val in partner.copy_attributes.items():
                        if random.random() < self.model.cross_over_rate:
                            setattr(self, attr, val)
            else: 
                    for attr, val in partner.copy_attributes.items():
                        setattr(self, attr, val)

        if partner != None: 
            if partner.wealth() > self.wealth():
                herd_traits(partner)
                self.wealthiest = partner
                self.top_wealth = partner.wealth()
            else: 
                self.top_wealth *= .99

