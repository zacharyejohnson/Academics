import random
import time
import numpy as np
import copy
from scipy.stats.mstats import gmean
\

class Agent(): 
    def __init__(self, model, row, col, ID, has_parent = False, **kwargs):
        self.model = model
        self.col = col
        self.row = row 
        self.id = ID
        self.patch = self.model.patches_dict[self.row][self.col]
        self.patch.agent = self 
        #agents can only move to von neumann neighbors 
        self.move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.gui = self.model.GUI
        self.consumption_rate = self.model.consumption_rate
        self.vision = random.randint(1, self.model.max_vision)
        

        # this method is common to all types of agents. They choose parameters and mutate in identical fashion
        def select_parameters(mutate = False, **mutation_kwargs):

            def set_goods(): 
                self.goods = {good:random.randint(vals["min"], vals["max"])
                                  for good, vals in self.model.goods_params.items()}

            def set_reservation_demand(): 
                    init_vals = self.model.init_demand_vals
                    min_res_q = init_vals["quantity"]["min"] 
                    max_res_q = init_vals["quantity"]["max"] 
                    min_res_p = init_vals["price"]["min"]
                    max_res_p = init_vals["price"]["max"]

                    self.reservation_demand = {good:{
                            "quantity": min_res_q + random.random() * (max_res_q - min_res_q)} for good in self.model.goods}

                    self.reservation_demand["sugar"]["price"] = np.e ** (
                        np.log(min_res_p) + random.random() * (np.log(max_res_p) - np.log(min_res_p)))

                    self.reservation_demand["water"]["price"] = 1 / self.reservation_demand["sugar"]["price"]
                    min_price_change = 1.01
                    max_price_change = 1.1
                    min_quantity_change = 1.01 
                    max_quantity_change = 1.1
                    self.quantity_change = min_quantity_change + random.random() * (max_quantity_change - min_quantity_change)
                    self.price_change = min_price_change + random.random() * (max_price_change - min_price_change)

            def set_reproduction_level(): 
                    min_reproduction_criteria, max_reproduction_criteria = {}, {}
                    #agents need between 2 and 4 times the maximum possible initial endowment to reproduce 
                    for good in self.model.goods:
                        min_reproduction_criteria[good] = self.model.goods_params[good]["max"] * 2 
                        max_reproduction_criteria[good] = 2 *  min_reproduction_criteria[good] 
                    self.reproduction_criteria = {
                        good : min_reproduction_criteria[good] +random.random() * (
                            max_reproduction_criteria[good] - min_reproduction_criteria[good])
                        for good in self.model.goods} 

            def set_child_breed_probabilities(): 
                if has_parent:
                    self.breed_probabilities = {breed: (prob + (self.min_mutate_rate + random.random() * (self.max_mutate_rate - self.min_mutate_rate)))
                                            if random.random() < self.mutate_rate else prob
                                            for breed, prob in kwargs["breed_probabilities"]}
                else: 
                    self.breed_probabilities = model.breed_probabilities

            set_child_breed_probabilities()

            def set_mutate_rate(): 
                min_rate = 0 if not mutate else\
                    mutation_kwargs["mutate_rate"] / (1 + self.mutate_rate)
                max_rate = self.model.max_mutate_rate if not mutate else\
                    mutation_kwargs["mutate_rate"] * (1 + self.mutate_rate)
                # keep a hard limit on the height of mutation rate
                self.mutate_rate = min_rate + random.random() * (max_rate - min_rate)
                if self.mutate_rate <= self.model.max_mutate_rate:
                    self.mutate_rate = self.model.max_mutate_rate

            def set_exchange_target(): 
                good1 = self.model.goods[0]
                good2 = self.model.goods[1]
                self.exchange_target = random.choice(self.model.goods)
                self.not_exchange_target = good1 if self.exchange_target == good2 else good2

            set_goods()
            set_reservation_demand()
            set_reproduction_level()
            set_mutate_rate()
            set_exchange_target()

            self.top_wealth  = self.wealth()

        if has_parent:
            ####### parameters already inerited if agent has parent ########
            for attr, val in kwargs.items():
                setattr(self, attr, val)
                
            # inherited values are mutated vals in dictionary if mutation is on
            if self.model.mutate:
                mutate()        
        
        else:
            select_parameters()

        def mutate(): 
            mutate_dict = {key: True if random.random() < self.mutate_rate else False for key in kwargs.keys()}
            # mutate select parameters
            select_parameters(mutate = True, **mutate_dict)

        def define_inheritance(): 
            # use attributes to define inheritence
            self.copy_attributes = copy.copy(vars(self))
            # redefine "good" or else values are drawn from parent for children
            self.copy_attributes["goods"] = {}
            for good in self.model.goods_params:
                # set inheritence of good as starting values for firm
                # only reproduce if you can provide new firm max starting value
                self.copy_attributes["goods"][good] = self.model.goods_params[good]["max"]
            for key in ["col", "row", "patch", "id"]:
                #, "target", "exchange_target"]:#,"reservation_demand"]:
                try:
                    del self.copy_attributes[key]
                except:
                    pass 
        define_inheritance()        
        self.reproduced = False

    def update_params(self):

        def set_target_good(): 
            good1 = random.choice(self.model.goods)
            good2 = "water" if good1 == "sugar" else "sugar"
            self.exchange_target = good1 if self.goods[good1] < self.reservation_demand[good1]["quantity"] else good2
            self.not_exchange_target = good2 if self.exchange_target == good1 else good1

        def check_reservation(): 
            for good, val in self.goods.items():
                if val < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] *= self.price_change
                    self.reservation_demand[good]["quantity"] /= self.quantity_change
                if val < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] /= self.price_change
                    self.reservation_demand[good]["quantity"] *= self.quantity_change

        set_target_good()
        check_reservation()



######### AGENT GENERAL LIVING FUNCTIONS ##############
    def consume(self):
        for good in self.goods:
                self.goods[good] -= self.consumption_rate[good]

    def die(self):
        self.model.empty_patches[self.row, self.col] = self.patch
        del self.model.agent_dict[self.id]
        self.delete_image()
        

    def harvest(self): 
        self.goods[self.patch.good] += self.patch.Q
        self.patch.Q = 0

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

    
    def wealth(self): 
            return sum(self.goods[good] / self.model.consumption_rate[good] for good in self.goods)

    def check_alive(self): 
        for good, val in self.goods.items(): 
            if val <= 0: 
                self.die()
                return False 
        return True

    def trade(self):
            
            def askToTrade(partner):
                #check if partner is looking for good agent is selling
                right_good = self.exchange_target != partner.exchange_target

                return right_good

            def bargain(partner):       
                WTP = self.reservation_demand[self.exchange_target]["price"] 
                WTA = partner.reservation_demand[self.exchange_target]["price"]
                
                # assume bargaining leads to average price...
                # maybe change to random logged distribution later
                if WTP > WTA: 
                    price, can_trade = gmean((WTA, WTP)), True
                else: 
                    price, can_trade =  None, False
                
                return can_trade, price
            
            def executeTrade(partner, price):
                target = self.exchange_target
                not_target = self.not_exchange_target
                self_res_min = self.reservation_demand[not_target]["quantity"]
                partner_res_min = partner.reservation_demand[not_target]["quantity"]
                # while the agents have at least their minimum required amount of goods and can afford to pay the price, continue trading 
                
                
                while self.goods[not_target] > self_res_min and\
                    self.goods[not_target] > price and\
                    partner.goods[not_target] > partner_res_min and\
                    partner.goods[not_target] > 1:

                    self.goods[target] += 1
                    self.goods[not_target] -= price
                    partner.goods[target] -= 1
                    partner.goods[not_target] += price

            neighbor_patches = self.neighbors()
            
            random.shuffle(neighbor_patches)
            for patch in neighbor_patches: 
                if patch.agent != None and patch.agent is not self: 
                    partner = patch.agent
                    right_good = askToTrade(partner)
                    if right_good: 
                        can_trade, price = bargain(partner)
                    
                    # check if partner has appropriate goods and WTP, WTA
                    
                        if can_trade:
                                                
                            # execute trades
                            executeTrade(partner, price)
                            # return partner top be used by herders 
                            return partner

                            break
            
            
                            

    ##################### MOVEMENT ###################################################
    #change row and col of agent and move image 
    def move(self): 
        move_patch = self.max_empty_neighbor()
        if move_patch != None: 
            self.patch.agent = None
            self.model.empty_patches[self.row, self.col] = self.patch
            self.move_image(move_patch)
            self.col = move_patch.col
            self.row = move_patch.row
            self.patch = self.model.patches_dict[self.row][self.col]
            del self.model.empty_patches[self.row, self.col]
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

        