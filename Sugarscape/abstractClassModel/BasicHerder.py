from BasicAgent import BasicAgent
import random
import numpy as np 

class BasicHerder(BasicAgent): 
    def __init__(self, model, row, col, ID, parent):
        super().__init__(model, row, col, ID, parent)
        self.wealthiest = self
        self.outline_width = 2
        self.herder = True
        self.arbitrageur = False

    def select_breed_parameters(self, mutate, parent, herding = False, partner = None):
        def generate_breed_parameters(): 
            inheritance = parent.define_inheritance() if parent is not None else None

            #herder attributes
            self.wealthiest = parent if inheritance is not None else self
            self.top_wealth = parent.get_wealth() if inheritance is not None else self.get_wealth()

        def copy_partner_parameters(): 
            if not hasattr(self, "top_wealth"):
                self.top_wealth = partner.get_wealth()
                self.wealthiest = partner

        if herding: 
             copy_partner_parameters()
        else: 
             generate_breed_parameters()

    
    def decrease_count(self): 
        self.model.num_basicherders -= 1

    def update_params(self):
        super().update_params()
        if self.wealth > self.top_wealth:
                    self.wealthiest = self
        if self.wealthiest != self:
                    self.top_wealth *= .999
