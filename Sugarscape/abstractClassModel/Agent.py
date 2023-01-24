import random
import time
import numpy as np
import copy
from scipy.stats.mstats import gmean

class Agent(): 
    def __init__(self, model, row, col, ID, parent):
        self.model = model
        self.col = col
        self.row = row 
        self.id = ID
        self.patch = self.model.patches_dict[self.row][self.col]
        self.patch.agent = self 
        self.parent = parent
        #agents can only move to von neumann neighbors 
        self.move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.live_visual = self.model.live_visual
        self.outline_width = 0
        if self.live_visual:
            self.gui = self.model.GUI
        self.consumption_rate = self.model.consumption_rate
        self.vision = random.randint(1, self.model.max_vision)

        # this method is common to all types of agents. They choose parameters and mutate in identical fashion
        def select_parameters(mutate = False, reservation_demand = True, 
                             reproduction_criteria= True,  
                             **mutate_kwargs):

            def set_stocks():
                if self.parent == None:
                    for good, vals in self.model.goods_params.items():
                        val = random.randint(vals["min"], vals["max"])
                        setattr(self, good, val)
                else:
                    for good in self.model.goods:
                        setattr(self, good, self.model.goods_params[good]["max"])
                        setattr(self.parent, good, 
                                getattr(self.parent,good) - self.model.goods_params[good]["max"])


            def set_reservation_demand(): 
                init_vals = self.model.init_demand_vals
                min_res_q = init_vals["quantity"]["min"] 
                max_res_q = init_vals["quantity"]["max"] 
                min_res_p = init_vals["price"]["min"]
                max_res_p = init_vals["price"]["max"]

                self.reservation_demand = {good:{
                    "quantity": min_res_q + random.random()
                    * (max_res_q - min_res_q)}
                    for good in self.model.goods}
                
                self.reservation_demand["sugar"]["price"] = np.e ** (
                    np.log(min_res_p) + random.random() * (np.log(max_res_p) - np.log(min_res_p)))

                self.reservation_demand["water"]["price"] = 1 / self.reservation_demand["sugar"]["price"]

                      ### set rates of adjustment
                # change price (WTP//WTA) by at most 10% per period
                # if price_change: 
                ## price_change defined in kwargs if mutate
                min_price_change = 1.01 if not mutate else\
                    self.parent.price_change / (1 + self.mutate_rate)
                max_price_change = 1.1 if not mutate else\
                    self.parent.price_change * (1 + self.mutate_rate)
                self.price_change =  min_price_change + random.random() * (max_price_change - min_price_change)
                
                # change reservation demand (quantity) by at most 10% per period
                # if quantity_change:
                min_quantity_change = 1.001 if not mutate else\
                    self.parent.quantity_change / (1 + self.mutate_rate)
                max_quantity_change = 1.01 if not mutate else\
                    self.parent.quantity_change * (1 + self.mutate_rate)
                    
                self.quantity_change = min_quantity_change + random.random() * (max_quantity_change - min_quantity_change)

            def set_reproduction_level(): 
                    min_reproduction_criteria, max_reproduction_criteria = {}, {}
                    for good in self.model.goods:
                        min_reproduction_criteria[good] = self.model.goods_params[good]["max"] * 2 if not mutate else\
                            self.parent.reproduction_criteria[good] / (1 + self.mutate_rate)
                        max_reproduction_criteria[good] = 2 *  min_reproduction_criteria[good] if not mutate else\
                            self.parent.reproduction_criteria[good] * (1 + self.mutate_rate)
                    self.reproduction_criteria = {
                        good :min_reproduction_criteria[good] +random.random() * (
                            max_reproduction_criteria[good] - min_reproduction_criteria[good])
                        for good in self.model.goods} 

            def set_child_breed_probabilities(): 
                if self.parent is not None:
                    self.primary_breeds_probabilities = {breed: (prob + (random.random() * (self.mutate_rate)))
                                            if random.random() < self.mutate_rate else prob
                                            for breed, prob in inheritance["primary_breeds_probabilities"].items()}
                    self.secondary_breeds_probabilities = {breed: (prob + (random.random() * (self.mutate_rate)))
                                            if random.random() < self.mutate_rate else prob
                                            for breed, prob in inheritance["secondary_breeds_probabilities"].items()}
                else: 
                    self.primary_breeds_probabilities = model.primary_breeds_probabilities
                    self.secondary_breeds_probabilities = model.secondary_breeds_probabilities

            def set_mutate_rate(): 
                min_rate = 0 if not mutate else\
                    self.parent.mutate_rate / (1 + self.parent.mutate_rate)
                max_rate = self.model.max_mutate_rate if not mutate else\
                    self.parent.mutate_rate * (1 + self.parent.mutate_rate)
                # keep a hard limit on the height of mutation rate
                self.mutate_rate = min_rate + random.random() * (max_rate - min_rate)
                if self.mutate_rate >= self.model.max_mutate_rate:
                    self.mutate_rate = self.model.max_mutate_rate

            def set_exchange_target(): 
                good1 = self.model.goods[0]
                good2 = self.model.goods[1]
                self.exchange_target = random.choice(self.model.goods)
                self.not_exchange_target = good1 if self.exchange_target == good2 else good2

            # set and mutate, or not, based on mutation_kwargs
            
            set_stocks()
            self.top_wealth  = self.get_wealth()
            self.wealth = self.get_wealth()
            
            if reservation_demand: 
                set_reservation_demand()

            if reproduction_criteria:     
                set_reproduction_level()

            set_mutate_rate()

            set_child_breed_probabilities()

            set_exchange_target()

            self.select_breed_parameters(mutate, self.parent, herding = False)

        def mutate(): 
            mutate_dict = {key: val if random.random() < self.mutate_rate else False for key, val in inheritance.items()} 
            # mutate select parameters
            select_parameters(mutate = True, **mutate_dict)

        if parent is not None: 
            self.wealthiest = parent
            self.top_wealth = parent.get_wealth()
            inheritance = parent.define_inheritance()
            for attr, val in inheritance.items():
                setattr(self, attr, val)
            
            # inherited values are mutated vals in dictionary if mutation is on
            if self.model.mutate:
                mutate()    
            else:
                self.select_breed_parameters(mutate = False, parent = self.parent, herding = False)
        
        else:
            select_parameters()


        self.reproduced = False
        self.transaction_prices = []
        
        self.agent_transaction_prices = []

    def select_breed_parameters(self, mutate, parent, herding = False, partner = None):
        pass

    def define_inheritance(self):
            # use attributes to define inheritance
            copy_attributes = copy.copy(vars(self))
            # redefine "good" or else values are drawn from parent for children
            for key in self.model.drop_attr:
                try:
                    del copy_attributes[key]
                except:
                    continue 
            return copy_attributes

    def update_params(self):

        def set_target_good(): 
            good1 = random.choice(self.model.goods)
            good2 = "water" if good1 == "sugar" else "sugar"
            if getattr(self,good1) < self.reservation_demand[good1]["quantity"]\
                and getattr(self,good2) < self.reservation_demand[good2]["quantity"]:
                self.exchange_target, self.not_exchange_target = good1, good2
            elif getattr(self,good1) < self.reservation_demand[good1]["quantity"]\
                and getattr(self,good2) > self.reservation_demand[good2]["quantity"]:
                self.exchange_target, self.not_exchange_target = good1, good2
            elif getattr(self,good2) < self.reservation_demand[good2]["quantity"]\
                and getattr(self,good1) > self.reservation_demand[good1]["quantity"]:
                self.exchange_target, self.not_exchange_target = good2, good1 
            else: 
                self.exchange_target, self.not_exchange_target = good2, good1


        def check_reservation(): 
            # Rules simulating the law of demand

            for good in self.model.goods:
                if getattr(self, good) < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] *= self.price_change
                    self.reservation_demand[good]["quantity"] /= self.quantity_change
                if getattr(self, good) < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] /= self.price_change
                    self.reservation_demand[good]["quantity"] *= self.quantity_change
                    
        self.wealth = self.get_wealth()
            ### !!!! For loop should be rewritten if number of goods > 2 !!!!
            #goods = self.model.goods
            #for good in self.model.goods:
                # adjust_other_price = False
                # # Make a list of the good not selected, select index 0 and name other_good
                # other_good = [good_ for good_ in goods if good_ != good][0]
                # # excess demand for good
                # if getattr(self, good) < self.reservation_demand[good]["quantity"]:
                #     self.reservation_demand[good]["price"] *= self.price_change
                #     self.reservation_demand[good]["quantity"] /= self.quantity_change
                #     adjust_other_price = True
                # # excess supply of good
                # elif getattr(self, good) > self.reservation_demand[good]["quantity"]:
                #     self.reservation_demand[good]["price"] /= self.price_change
                #     self.reservation_demand[good]["quantity"] *= self.quantity_change
                #     adjust_other_price = True
                # if adjust_other_price == True:
                #     self.reservation_demand[other_good]["price"] = 1 / self.reservation_demand[good]["price"]



                # if self.goods["water"] < self.reservation_demand["water"]["quantity"]:
                #     self.reservation_demand["water"]["quantity"] /= self.quantity_change
                # # excess supply of good
                # if self.goods["water"] > self.reservation_demand["water"]["quantity"]:
                #     self.reservation_demand["water"]["quantity"] *= self.quantity_change

                # self.reservation_demand["water"]["price"] = 1 / self.reservation_demand["sugar"]["price"]

        set_target_good()
        check_reservation()



######### AGENT GENERAL LIVING FUNCTIONS ##############
    def consume(self):
        for good, rate in self.model.consumption_rate.items():
            setattr(self,good, getattr(self,good) - rate)

    def harvest(self): 
        agent_patch = self.model.patches_dict[self.row][self.col]
        setattr(self, agent_patch.good, getattr(self, agent_patch.good) + agent_patch.Q)
        agent_patch.Q = 0 

    # def reproduce(self): 
    #     can_reproduce = True
    #     for good in self.goods: 
    #         if self.goods[good] < self.reproduction_criteria[good]: 
    #             can_reproduce = False 
    #             break
        
    #     if can_reproduce: 

    #         def child_breed(): 
    #             breed = random.choice(self.model.breed_probabilities.keys(), 
    #                                     weights=self.model.breed_probabilities.values())
    #             return breed

    #         child_breed = child_breed()

    #         print("reproducing")
    #         self.model.total_agents_created += 1
    #         row, col = self.model.chooseRandomEmptyPatch()  
    #         ID = self.model.total_agents_created

    #         if child_breed == "basic": 
    #             self.model.agent_dict[ID] =  BasicAgent(row=row, col=col, ID=ID, hasParent = True,  **self.copy_attributes)
    #         elif child_breed == "herder": 
    #             self.model.agent_dict[ID] =  Herder(row=row, col=col, ID=ID, hasParent = True,  **self.copy_attributes)
    #         # add good quantities to new agent, deduct from parent
    #         self.model.agent_dict[ID].goods = {}
    #         for good in self.goods:
    #             self.goods[good] -= self.reproduction_criteria[good]
    #             self.model.agent_dict[ID].goods[good] = self.reproduction_criteria[good]
    #         self.model.patches_dict[row][col].agent =  self.model.agent_dict[ID]
    #         self.gui.draw_agent(self.model.agent_dict[ID])
    #         self.reproduced = True

    
    def get_wealth(self): 
        return sum(getattr(self, good) / self.model.consumption_rate[good]
                                     for good in self.model.goods)

    def check_alive(self): 
        alive = True
        for good in self.model.goods:
            if getattr(self, good) < 0:
                # self.model.dead_agent_dict[self.id] = self
                self.model.empty_patches[self.row, self.col] = self.model.patches_dict[self.row][self.col]
                if self.model.live_visual:
                    self.model.GUI.canvas.delete(self.image)
                del self.model.agent_dict[self.id]
                self.patch.agent = None
                self.patch = None
                alive =  False
                self.decrease_count()
                break
        return alive
    
    def decrease_count(self): 
         # decrease population of specific agent within each class
         pass

    def trade(self):
            
            def askToTrade(partner):
                #check if partner is looking for good agent is selling
                if (self.exchange_target != partner.exchange_target): 
                    return True
                else: 
                    return False

            def bargain(partner):       
                WTP = self.reservation_demand[self.exchange_target]["price"] 
                WTA = partner.reservation_demand[self.exchange_target]["price"]
                
                # assume bargaining leads to average price...
                # maybe change to random logged distribution later
                if WTP > WTA: 
                    price, can_trade = gmean((WTA, WTP)), True
                else: 
                    price, can_trade =  None, False
                
                return price, can_trade
            
            def executeTrade(partner, price):
                    
                self_res_min = self.reservation_demand[self.not_exchange_target]["quantity"]
                partner_res_min = partner.reservation_demand[self.exchange_target]["quantity"]

                if self.exchange_target == "sugar": 
                        true_price = price
                else: 
                        true_price = 1/price

                while (getattr(self, self.not_exchange_target) > self_res_min > price) and\
                        (getattr(partner, self.exchange_target) > partner_res_min > 1):
                    
                    setattr(self, self.exchange_target, getattr(self, self.exchange_target) + 1)
                    setattr(self, self.not_exchange_target, getattr(self, self.not_exchange_target) - price)
                    setattr(partner,self.exchange_target, getattr(partner, self.exchange_target) - 1)
                    setattr(partner, self.not_exchange_target, getattr(partner, self.not_exchange_target) + price)

                    self.model.transaction_prices[self.exchange_target].append(true_price)

                    self.model.all_prices.append(true_price)
                    self.model.total_exchanges += 1
                    self.agent_transaction_prices.append(true_price)

                    if self.arbitrageur: 
                        self.expected_price = (self.expected_price * (
                                self.present_price_weight) + true_price) / self.present_price_weight

            def herd_traits(agent, partner):
                if agent.top_wealth < partner.get_wealth():
                    copy_attributes = partner.define_inheritance()
                    if agent.model.genetic:
                        for attr, val in copy_attributes.items():
                            if random.random() <= agent.model.cross_over_rate:
                                setattr(agent, attr, val)
                        
                        agent.select_breed_parameters(mutate = False, parent = None, 
                                                herding = True, partner = partner)
        
                    else: 
                        for attr, val in copy_attributes.items():
                            setattr(agent, attr, val) 
            neighbor_patches = self.neighbors()
            
            random.shuffle(neighbor_patches)
            self.partner = None
            for patch in neighbor_patches: 
                if patch.agent != None and patch.agent != self: 
                    self.partner = patch.agent
                    self.partner.partner = self
                    right_good = askToTrade(self.partner)
                    if right_good: 
                        price, can_trade = bargain(self.partner)
                    else: 
                        price, can_trade = None, False
                    if can_trade: 
                        executeTrade(self.partner, price)
                        if self.herder: 
                            if self.top_wealth < self.partner.get_wealth(): 
                                herd_traits(self, self.partner)
                            # if partner is a herder, they can reverse herd 
                        elif self.partner.herder and self.partner.top_wealth < self.get_wealth(): 
                                herd_traits(self.partner, self)
                        #print(price)
                        break
               
            
                            

    ##################### MOVEMENT ###################################################
    #change row and col of agent and move image 
    def move(self): 
        move_patch = self.max_empty_neighbor()
        if move_patch != None: 
            self.patch.agent = None
            self.model.empty_patches[self.row, self.col] = self.patch
            if self.live_visual:
                self.move_image(move_patch)
            self.col = move_patch.col
            self.row = move_patch.row
            del self.model.empty_patches[self.row, self.col]
            self.patch = self.model.patches_dict[self.row][self.col]
            self.patch.agent = self

    # move image of agent to desired row, col
    def move_image(self, patch):
                self.gui.canvas.move(self.image, 
                                (patch.col - self.col) * self.gui.dimPatch,
                                (patch.row - self.row) * self.gui.dimPatch)

    def delete_image(self): 
        self.gui.canvas.delete(self.image)

    #checks if identified patch is a real patch, i.e. is not out of bounds of the map
    def valid_patch(self, dx, dy):
        if(self.row + dy >= 0 and self.row + dy <= self.model.rows-1) and (self.col + dx >= 0 and self.col + dx <= self.model.cols-1): 
            return True
        else: 
            return False

    #checks if a patch can be moved to, i.e. no agent is already occupying the patch 
    def valid_move(self, dx, dy): 
        if(self.valid_patch(dx, dy) and self.model.patches_dict[self.row + dy][self.col + dx].agent == None): 
            return True
        else: 
            return False 

    def max_empty_neighbor(self): 
        max_q = 0
        max_empty_neighbor = None
        random.shuffle(self.move_directions)
        for dy, dx in self.move_directions: 
            if self.valid_move(dx, dy):
                patch = self.model.patches_dict[self.row + dy][self.col + dx]
                if patch.Q > max_q: 
                    max_q = patch.Q
                    max_empty_neighbor = patch
        return max_empty_neighbor

    # return von neumann neighbors
    def neighbors(self): 
        neighbors = []
        for dy, dx in self.move_directions: 
            if self.valid_patch(dx, dy):
                patch = self.model.patches_dict[self.row + dy][self.col + dx]
                neighbors.append(patch)

        return neighbors

        