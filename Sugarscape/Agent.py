import random
from tkinter import * 
import numpy as np
import random
from scipy.stats.mstats import gmean
import copy

class Agent():
    def __init__(self, model, row, col, ID, has_parent = False, **kwargs):
        self.model = model
        self.col = col
        self.row = row 
        self.id = ID
        self.image = None
        self.patch = self.model.patches_dict[self.row][self.col]
        self.patch.agent = self 
        #agents can only move to von neumann neighbors 
        self.move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.gui = self.model.GUI
        self.consumption_rate = self.model.consumption_rate
        

        def select_parameters(mutate = False, good = True, wealth = True, reservation_demand = True, 
                             reproduction_criteria= True, breed = True, 
                             exchange_target = True, 
                             vision = True, mutate_rate = True,
                             **mutate_kwargs): 

            def set_breed_parameters(breed_): 
                if self.breed[breed_]: 
                    if breed_ == "basic":
                        self.target = "sugar"
                        self.not_target = "water"
                        self.color = "red"
                    if breed_ == "switcher":
                        switch_min = 100 
                        switch_max = 1000 
                        self.switch_rate = random.randint(switch_min, switch_max) 
                        self.periods_to_switch = self.switch_rate
                        # start switcher with random target
                        goods = list(self.goods.keys())
                        num_goods = len(goods)
                        target_index = random.randint(0, num_goods-1)
                        self.target = goods[target_index]
                        self. target = goods[0]
                        self.color = "orange"

                    if breed_ == "arbitrageur":
              
                        # track past exchange prices
                        # if average prices is below price agent believes is correct,
                        min_denominator = 10 
                        max_denominator = 100 
                        self.present_price_weight = random.randint(min_denominator, max_denominator)
                        self.expected_price = self.reservation_demand["sugar"]["price"]
                        targets = copy.copy(self.model.goods)
                        random.shuffle(targets)
                        self.target = targets.pop()
                        self.not_target = targets[0]
                        self.color = "green"
                    if breed_  == "herder":        
                        self.wealthiest = self
                        self.top_wealth = self.wealth
                        self.color = "blue"
    
            def set_init_goods():
                min = self.model.init_good_ranges["min"]
                max = self.model.init_good_ranges["max"]
                goods = {good: random.randrange(min, max) for good in self.model.goods}
                return goods

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
                min_price_change = 1.01
                max_price_change = 1.1
                min_quantity_change = 1.01 
                max_quantity_change = 1.1
                self.quantity_change = min_quantity_change + random.random() * (max_quantity_change - min_quantity_change)
                self.price_change = min_price_change + random.random() * (max_price_change - min_price_change)

            def set_reproduction_level(): 
                min_reproduction_criteria, max_reproduction_criteria = {}, {}
                for good in self.model.goods:
                    min_reproduction_criteria[good] = self.model.goods_params[good]["max"] * 2 
                    max_reproduction_criteria[good] = 2 *  min_reproduction_criteria[good] 
                self.reproduction_criteria = {
                    good :min_reproduction_criteria[good] +random.random() * (
                        max_reproduction_criteria[good] - min_reproduction_criteria[good])
                    for good in self.model.goods} 

            if good: 
                self.goods = set_init_goods()

            if wealth: 
                self.wealth = sum(self.goods[good] / self.model.consumption_rate[good]
                                         for good in self.goods)
            if reservation_demand: 
                set_reservation_demand()

            if reproduction_criteria: 
                set_reproduction_level()

            if breed:
                self.breed = {breed:True if 0 < random.random() <= prob  else False 
                              for breed, prob in self.model.breed_probabilities.items()}
                self.breed["switcher"] = False if self.breed["basic"] else True
                for breed_ in self.model.breeds:
                    set_breed_parameters(breed_) 
            if exchange_target:
                #set exchange target randomly at first
                self.exchange_target = random.choice(self.model.goods)
            if mutate_rate and self.model.mutate:
                min_rate = 0 
                max_rate = self.model.max_mutate_rate 
                
                self.mutate_rate = min_rate + random.random() * (max_rate - min_rate)
                if self.mutate_rate <= self.model.max_mutate_rate:
                    self.mutate_rate = self.model.max_mutate_rate
            if vision:
                    self.vision = random.randint(1, self.model.max_vision )

        def define_inheritence():
            # use attributes to define inheritence
            self.copy_attributes = copy.copy(vars(self))
            # redefine "good" or else values are drawn from parent for children
            self.copy_attributes["good"] = {}
            for good in self.model.goods_params:
                # set inheritence of good as starting values for firm
                # only reproduce if you can provide new firm max starting value
                self.copy_attributes["good"][good] = self.model.goods_params[good]["max"]
            for key in ["col", "row", "dx", "dy", "id", "good", "wealth"]:
                #, "target", "exchange_target"]:#,"reservation_demand"]:
                try:
                    del self.copy_attributes[key]
                except:
                    pass 
        def mutate():
            mutate_dict = {key: True if random.random() < self.mutate_rate else False for key in kwargs.keys()}
            # mutate select parameters
            select_parameters(mutate = True, **mutate_dict)
            
        self.model = model
        
        if has_parent:
            ####### parameters already inerited if agent has parent ########
            for attr, val in kwargs.items():
                # print(attr, val, sep = "\n")
                setattr(self, attr, val)
                
            # inherited values are mutated vals in dictionary if mutation is on
            if self.model.mutate:
                mutate()
                print("Mutated")        
        
        else:
            select_parameters()
        # allocate each .good to agent within quantity in range specified by 
        # randomly choose initial target good
        define_inheritence()        
        self.reproduced = False

    # finds the von neumann neighbor with highest q increase and moves to it to consume 
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


    def max_empty_neighbor_utility(self): 
        max_u = 0
        max_empty_neighbor_utility = None
        random.shuffle(self.move_directions)
        for dy, dx in self.move_directions: 
            if self.valid_move(dx, dy):
                patch = self.model.patches_dict[self.row + dy][self.col + dx]
                hypothetical_goods  = self.goods
                hypothetical_goods[patch.good] += patch.Q
                hypothetical_utility = np.prod(list(hypothetical_goods.values()))
                if hypothetical_utility > max_u: 
                    max_u = hypothetical_utility
                    max_empty_neighbor_utility = patch
        return max_empty_neighbor_utility

    def utility(self): 
        return np.prod(list(self.goods.values()))

    def harvest(self): 
        agent_patch = self.model.patches_dict[self.row][self.col]
        self.goods[agent_patch.good] += agent_patch.Q
        agent_patch.Q = 0

    def consume(self):
        dead = False 
        for good in self.goods:
            if not dead: 
                self.goods[good] -= self.consumption_rate[good]
                if self.goods[good] <= 0: 
                    self.die()
                    dead = True
            else: 
                break
            
    def die(self):
        self.delete_image()
        del self.model.agent_dict[self.id]

    def update_params(self): 
        def set_target_good(): 
            self.wealth = sum(self.goods[good] / self.model.consumption_rate[good] for good in self.goods)
            good1 = random.choice(self.model.goods)
            good2 = "water" if good1 == "sugar" else "sugar"
            self.exchange_target = good1 if self.goods[good1] < self.reservation_demand[good1]["quantity"] else good2
            self.not_exchange_target = good2 if self.exchange_target == good1 else good1
        def checkReservation():
            for good, val in self.goods.items():
                if val < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] *= self.price_change
                    self.reservation_demand[good]["quantity"] /= self.quantity_change
                if val < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] /= self.price_change
                    self.reservation_demand[good]["quantity"] *= self.quantity_change
        checkReservation()
        set_target_good()

    def reproduce(self): 
        can_reproduce = True
        for good in self.goods: 
            if self.goods[good] < self.reproduction_criteria[good]: 
                can_reproduce = False 
                break
        
        if can_reproduce: 
            print("reproducing")
            self.model.total_agents_created += 1
            row, col = self.model.chooseRandomEmptyPatch()  
            ID = self.model.total_agents_created
            self.model.agent_dict[ID] =  Agent(row=row, col=col, ID=ID, hasParent = True,  **self.copy_attributes)
            # add good quantities to new agent, deduct from parent
            self.model.agent_dict[ID].goods = {}
            for good in self.goods:
                self.goods[good] -= self.reproduction_criteria[good]
                self.model.agent_dict[ID].goods[good] = self.reproduction_criteria[good]
            self.model.patches_dict[row][col].agent =  self.model.agent_dict[ID]
            self.gui.draw_agent(self.model.agent_dict[ID])
            
            

            self.reproduced = True


    def trade(self):
        
        def askToTrade(patch):
            partner = patch.agent
            #check if partner is looking for good agent is selling
            right_good = self.exchange_target == partner.exchange_target

            return partner, right_good

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
            self_res_min = self.reservation_demand[self.not_exchange_target]["quantity"]
            partner_res_min = self.reservation_demand[self.not_exchange_target]["quantity"]
            while self.goods[self.not_exchange_target] > self_res_min and\
                self.goods[self.not_exchange_target] > price and\
                partner.goods[self.not_exchange_target] > partner_res_min and\
                partner.goods[self.not_exchange_target] > 1:
                
                self.goods[self.exchange_target] += 1
                self.goods[self.not_exchange_target] -= price
                partner.goods[self.exchange_target] -= 1
                partner.goods[self.not_exchange_target] += price

        neighbor_patches = self.neighbors()
        
        random.shuffle(neighbor_patches)
        for patch in neighbor_patches: 
            if patch.agent != None: 
                partner, right_good = askToTrade(patch)
                if right_good: 
                    can_trade, price = bargain(partner)
                
                # check if partner has appropriate goods and WTP, WTA
                
                    if can_trade == True:
                                            
                        # execute trades
                        executeTrade(partner, price)
                        

##################### MOVEMENT ###################################################
 #change row and col of agent and move image 
    def move(self): 
        move_patch = self.max_empty_neighbor()
        if move_patch != None: 
            self.patch.agent = None
            self.move_image(move_patch)
            self.col = move_patch.col
            self.row = move_patch.row
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



        






        