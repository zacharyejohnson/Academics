



import copy
import random
import numpy as np
from scipy.stats.mstats import gmean
from Patch import *
#Agent.py

class Agent():
    # **inheritance are the inherited
    def __init__(self, model, row, col, ID, parent = None):
         
        def selectParameters(mutate = False, reservation_demand = True, 
                             reproduction_criteria= True,  
                             **mutate_kwargs):    
         
            # at first, you are the agent does not know any one else
            # give all agents these variables to avoid error when deleted from
            # inheritance dict
            def setReservationDemand():#price_change = True, quantity_change = True):
                ### don't mutate reservation quantity and price
                ### these are set in live time
                init_vals = self.model.max_init_demand_vals
                # min_res_q = init_vals["quantity"]["min"] 
                # max_res_q = init_vals["quantity"]["max"] 
                min_res_p = init_vals["price"]["min"]
                max_res_p = init_vals["price"]["max"]
                self.wealth_by_good = {}
                for good in self.model.goods: 
                    self.wealth_by_good[good] = (getattr(self,good) / self.model.consumption_rate[good])

                self.reservation_demand = {good:{"quantity": getattr(self, good)} for good in self.model.goods}


                self.reservation_demand["sugar"]["price"] = self.wealth_by_good["sugar"] / self.wealth_by_good["water"]
                self.reservation_demand["water"]["price"] = 1 / self.reservation_demand["sugar"]["price"]
                
                ### set rates of adjustment
                # change price (WTP//WTA) by at most 10% per period
                # if price_change: 
                ## price_change defined in kwargs if mutate
                if parent == None:
                    min_price_change = 1.01 
                    max_price_change = 1.1
                    self.price_change = np.e ** (
                        np.log(min_price_change) + random.random() * (np.log(max_price_change) - np.log(min_price_change)))
                #change reservation demand (quantity) by at most 10% per period
                #if quantity_change:
                    min_quantity_change = 1.001 
                    max_quantity_change = 1.01 
                    self.quantity_change = min_quantity_change + random.random() * (max_quantity_change - min_quantity_change)  
                else:
                    self.price_change = parent.price_change
                    self.quantity_change = parent.quantity_change


            
            def setReproductionLevel():
                min_reproduction_criteria, max_reproduction_criteria = {}, {}
                for good in self.model.goods:
                    min_reproduction_criteria[good] = self.model.goods_params[good]["max"] * 2 if not mutate else\
                        self.parent.reproduction_criteria[good] / (1 + self.mutate_rate)
                    max_reproduction_criteria[good] = 2 *  min_reproduction_criteria[good] if not mutate else\
                        self.parent.reproduction_criteria[good] * (1 + self.mutate_rate)
                self.reproduction_criteria = {
                    good :min_reproduction_criteria[good] + random.random() * (
                        max_reproduction_criteria[good] - min_reproduction_criteria[good])
                    for good in self.model.goods} 
                for good in self.model.goods: 
                    if self.reproduction_criteria[good] < self.model.goods_params[good]["max"] * 2: 
                        self.reproduction_criteria[good] = self.model.goods_params[good]["max"] * 2
                
            def setUtilityFunction(): 

                self.sugar_utility_weight = 0.5 #self.model.consumption_rate["sugar"] / sum(self.model.consumption_rate[good] for good in self.model.goods)
                self.water_utility_weight = 1 - self.sugar_utility_weight
                # self.wealth_by_good = {}
                # for good in self.model.goods: 
                #     self.wealth_by_good[good] = (getattr(self,good) / self.model.consumption_rate[good])
            
                # self.wealth = sum(self.wealth_by_good.values())
                self.MRS = self.wealth_by_good["water"] / self.wealth_by_good["sugar"]
                self.utility = (self.wealth_by_good["sugar"] ** self.sugar_utility_weight) * (self.wealth_by_good["water"] ** self.water_utility_weight)
                 
            def selectBreed():    
                if self.parent is not None:
                    # place herder first in list
                    shuffle_breeds = copy.copy(self.model.primary_breeds)
                    random.shuffle(shuffle_breeds)

                    for breed_ in ["herder"] + shuffle_breeds:
                        if random.random() < self.mutate_rate:
                            # if mutation occurs, switch breed boolean
                            select_breed = False if getattr(self, breed_) else True
                            setattr(self, breed_, select_breed)
                            
                            if select_breed == True and breed_ in shuffle_breeds:
                                shuffle_breeds.remove(breed_)
                                for not_my_breed in shuffle_breeds:
                                    setattr(self, not_my_breed, False)
                                break
                    # set breed basic if all breeds are turned to False
                    if True not in (getattr(self, brd)
                                    for brd in self.model.primary_breeds):
                        if "basic" in self.model.primary_breeds: 
                            self.setBreedBasic(herder = self.herder)
                        else: 
                            for breed in self.model.breeds: 
                                setattr(self, breed, getattr(self.parent, breed))

                # select breed randomly if agent has no parent            
                else:                            
                    # for breed_, prob in self.model.breed_probabilities.items():
                    #     if random.random() <= prob :
                    #         setattr(self, breed_, True)  
                    #     else: 
                    #         setattr(self, breed_, False)  
                    # since switcher and basic are mutually exclusive,
                    # All initial agents are basic, other breeds only 
                    # appear through mutation
                    self.setBreedBasic(herder = False)
                    
                self.selectBreedParameters(mutate, self.parent, 
                                           herding = False)


            def setMutateRate():
                if self.model.mutate:
                    min_rate = 0 if not mutate else\
                        self.parent.mutate_rate / (1 + self.parent.mutate_rate)
                    max_rate = self.model.max_mutate_rate if not mutate else\
                        self.parent.mutate_rate * (1 + self.parent.mutate_rate)
                    # keep a hard limit on the height of mutation rate
                    self.mutate_rate = min_rate + random.random() * (max_rate - min_rate)
                    if self.mutate_rate >= self.model.max_mutate_rate:
                        self.mutate_rate = self.model.max_mutate_rate
 



            ###################################################################            

            # define mutate rate first so that it effects mutation of all
            # other attributes
            
            setMutateRate() 

            
            # set value of commodity holdings, if agent has parents,
            # these values will be replaced by the max values
            setStocks()
            #if reservation_demand: 
            setReservationDemand()
            if reproduction_criteria:
                setReproductionLevel()     
            setUtilityFunction()   
            setTargets()
            self.vision = random.randint(1, self.model.max_vision)
            selectBreed()
        #######################################################################

        def setStocks():
            if self.parent == None:
                for good, vals in self.model.goods_params.items():
                    val = random.randint(vals["min"], vals["max"])
                    setattr(self, good, val)
            else:
                for good in self.model.goods:
                    setattr(self, good, self.model.goods_params[good]["max"])
                    setattr(self.parent, good, 
                            getattr(self.parent, good) - self.model.goods_params[good]["max"])
                    
            # wealth is the number of periods worth of food owned by the agent
            # assumes that one good is instantly convertable to another

            self.wealth_by_good = {good: (getattr(self, good) / self.model.consumption_rate[good]) for good in self.model.goods}
        
            self.wealth = sum(list(self.wealth_by_good.values()))

        def setTargets():
            # set exchange target randomly at first
            goods = list(self.model.goods)
            random.shuffle(goods)
            self.target = goods.pop()
            self.not_target = goods[0]
               
        def mutate():
            # select which parameters will be mutated
            mutate_dict = {key: val if random.random() < self.mutate_rate else False for key, val in inheritance.items()} 
            # mutate select parameters
            selectParameters(mutate = True, **mutate_dict)
            
        if parent != None:
            inheritance = parent.defineInheritance()
        self.parent = parent
        self.model = model
        
        if self.parent is not None:
            ####### parameters already inherited if agent has parent ########
            for attr, val in inheritance.items():
                setattr(self, attr, val)
            setStocks()
            # randomly set target, will be redifined in according to breed
            # parameters in the following period
            setTargets()
            # inherited values are mutated vals in dictionary if mutation is on
            if self.model.mutate:
                mutate()    
            else:
                self.selectBreedParameters(mutate = False,
                                           parent = self.parent,
                                           herding  = False)
        
        else:
            selectParameters()
        # allocate each .good to agent within quantity in range specified by 
        # randomly choose initial target good
        self.col = col
        self.row = row 
        self.dx = 0
        self.dy = 0
        self.id = ID
        self.reproduced = False

###############################################################################     
    def setBreedBasic(self, herder):
        if "basic" in self.model.primary_breeds: 
            self.basic = True
            self.optimizer = False 
        else: 
            self.optimizer = True 
            self.basic = False
        self.arbitrageur = False
        self.herder = herder

    def selectBreedParameters(self, mutate, parent, herding = False, 
                              partner = None):
        #inheritance = parent.defineInheritance() if parent is not None else ""
        def generateBreedParameters():
            if breed == "basic":
                goods = list(self.model.goods)
                random.shuffle(goods)
                self.target = goods.pop()
                self.not_target = goods[0]
                
            if breed == "arbitrageur":
                # track past exchange prices
                # if average prices is below price agent believes is correct,
                min_denominator = 10 if not mutate or "present_price_weight" not in inheritance else\
                    int(inheritance["present_price_weight"] / (1 + self.mutate_rate))
                max_denominator = 100 if not mutate  or "present_price_weight" not in inheritance else\
                    int(inheritance["present_price_weight"] * (1 + self.mutate_rate))
                self.present_price_weight = random.randint(
                    min_denominator, max_denominator)
                self.expected_price = self.reservation_demand["sugar"]["price"]

            if breed  == "herder":      
                self.wealthiest = parent if inheritance else self
                self.top_wealth = parent.wealth if inheritance else self.wealth

            if breed == "optimizer": 
                self.MRS = self.wealth_by_good["water"] / self.wealth_by_good["sugar"]

            # print("set attributes new:", breed)
        
        def copyPartnerParameters():
            # if copied breed and missing parameter value, draw from partner
            if getattr(self, breed):
                if breed  == "herder":  
                    if not hasattr(self, "top_wealth"):
                        self.top_wealth = partner.wealth
                        self.wealthiest = partner
                if breed == "arbitrageur":
                    if not hasattr(self, "expected_price"):                        
                        self.expected_price = partner.expected_price
                    if not hasattr(self, "present_price_weight"):                    
                        self.present_price_weight = partner.present_price_weight 

                if breed == "optimizer": 
                    if not hasattr(self, "MRS"): 
                        self.MRS = self.wealth_by_good["water"] / self.wealth_by_good["sugar"]
                    # if not
                    # self.target = partner.target
                    # self.not_target = partner.not_target
          
        for breed in self.model.breeds:
            if getattr(self, breed):
                inheritance = parent.defineInheritance() if parent else ""
                # those who change breed due to herding need only need to fill missing
                # parameter values
                if herding:
                    copyPartnerParameters()
                else:
                    generateBreedParameters()        

    def defineInheritance(self):
        # use attributes to define inheritance
        copy_attributes = copy.copy(vars(self))
        # redefine "good" or else values are drawn from parent for children

        for key in self.model.drop_attr:
            try:
                del copy_attributes[key]
            except:
                continue 
        return copy_attributes
    
    def updateParams(self, trade = False):

        for good in self.model.goods: 
                self.wealth_by_good[good] = (getattr(self,good) / self.model.consumption_rate[good])
        self.wealth = sum(list(self.wealth_by_good.values()))# / len(self.model.goods)
        

        def setTargetGood():
            if self.herder:
                if self.wealth > self.top_wealth:
                    self.wealthiest = self
                if self.wealthiest != self:
                    self.top_wealth *= .999
            # let exchange target be determined by reservation demand
            # if shortage of both goods, choose randomly
            # good1 = random.choice(self.model.goods)
            # good2 = "water" if good1 == "sugar" else "sugar"
            # if self.basic:
            #     if getattr(self,good1) < self.reservation_demand[good1]["quantity"]\
            #         and getattr(self,good2) < self.reservation_demand[good2]["quantity"]:
            #         self.target, self.not_target = good1, good2
                
            #         # in case to level of wealth falls, as it does one population 
            #         # grows, allow top_wealth to decay
            #     elif getattr(self,good1) < self.reservation_demand[good1]["quantity"]\
            #         and getattr(self,good2) > self.reservation_demand[good2]["quantity"]:
            #         self.target, self.not_target = good1, good2
            #     elif getattr(self,good2) < self.reservation_demand[good2]["quantity"]\
            #         and getattr(self,good1) > self.reservation_demand[good1]["quantity"]:
            #         self.target, self.not_target = good2, good1                
             
            if self.arbitrageur:
                # arbitrageur exchanges for the good that is cheaper than his WTP
                WTP = self.reservation_demand["sugar"]["price"]
                if self.expected_price > WTP:
                    self.target, self.not_target = "sugar", "water"  
                else: 
                    self.target, self.not_target = "water", "sugar"

            # if self.optimizer and not trade: 
            #             if self.MRS < 1: 
            #                 self.target = "water"
            #                 self.not_target = "sugar"
            #             elif self.MRS > 1: 
            #                 self.target = "sugar"
            #                 self.not_target = "water"
            #             else: 
            #                 goods = list(self.model.goods)
            #                 random.shuffle(goods)
            #                 self.target = goods.pop()
            #                 self.not_target = goods[0]
                


        def checkReservation():
            goods = list(self.model.goods)
            random.shuffle(goods)
            for i, good in enumerate(goods):
                othergood = goods.pop()
                if getattr(self, othergood) < self.reservation_demand[othergood]["quantity"]:
                    self.reservation_demand[othergood]["price"] *= self.price_change
                    self.reservation_demand[othergood]["quantity"] /= self.quantity_change
                    self.reservation_demand[good]["price"] = 1 / self.reservation_demand[othergood]["price"]

                elif getattr(self, othergood) > self.reservation_demand[othergood]["quantity"]:
                    self.reservation_demand[othergood]["price"] /= self.price_change
                    self.reservation_demand[othergood]["quantity"] *= self.quantity_change
                    self.reservation_demand[good]["price"] = 1 / self.reservation_demand[othergood]["price"]



                

            



        def checkReservationOptimizer(): 
            # optimizers choose internal valuations of each good based on their relative scarcity
            #self.reservation_demand["water"]["price"] = self.wealth_by_good["water"] / self.wealth
            #self.reservation_demand["sugar"]["price"] = self.wealth_by_good["sugar"] / self.wealth
            if self.wealth_by_good["water"] > 0 and self.wealth_by_good["sugar"] > 0: 
                self.MRS = self.wealth_by_good["water"] / self.wealth_by_good["sugar"]
                self.utility = (self.wealth_by_good["sugar"] ** self.sugar_utility_weight) * (self.wealth_by_good["water"] ** self.water_utility_weight)
            
            
        if not trade: 
            setTargetGood()

        # print(self.id)
        if self.optimizer: 
            checkReservationOptimizer()

        elif not trade: 
            checkReservation()




    def consume(self):
        for good, rate in self.model.consumption_rate.items():
            setattr(self,good, getattr(self,good) - rate)
            
            
    
    def check_alive(self):
        alive = True
        for good in self.model.goods:
            if getattr(self, good) < 0:
                alive = False 
                # self.model.dead_agent_dict[self.id] = self
                self.model.empty_patches[self.row, self.col] = self.model.patches_dict[self.row][self.col]
                if self.model.live_visual:
                    self.model.GUI.canvas.delete(self.image)
                del self.model.agent_dict[self.id]

                return alive 
        return alive 

            
    def reproduce(self):
        if self.sugar > self.reproduction_criteria["sugar"] and\
            self.water > self.reproduction_criteria["water"] and\
            self.sugar > self.model.goods_params["sugar"]["max"]*2 and\
            self.water > self.model.goods_params["water"]["max"]*2:
            # make sure inherited values are up to date

            self.model.total_agents_created += 1
            row, col = self.model.chooseRandomEmptyPatch()  
            ID = self.model.total_agents_created
            self.model.agent_dict[ID] =  Agent(self.model, row=row, col=col, 
                                               ID=ID, parent = self)


            self.model.patches_dict[row][col].agent =  self.model.agent_dict[ID]
            if self.model.live_visual:
                self.model.GUI.drawAgent(self.model.agent_dict[ID])
            self.reproduced = True

    def getPatchUtility(self, patch): 
        if patch.good == "sugar": 
            new_utility = ((self.wealth_by_good["sugar"] + (patch.Q / self.model.consumption_rate["sugar"]))  ** self.sugar_utility_weight) * (self.wealth_by_good["water"] ** self.water_utility_weight)
        elif patch.good == "water": 
            new_utility = (self.wealth_by_good["sugar"]  ** self.sugar_utility_weight) * ((self.wealth_by_good["water"] + (patch.Q / self.model.consumption_rate["water"])) ** self.water_utility_weight)
        else: 
            new_utility = 0

        return new_utility



######################## move method and functions ############################
    def move(self):  
        def findMaxEmptyPatch(curr_row, curr_col):
            # dict to save empty patch with max q for each good for basics, utility gain for optimizers 

            max_patch = {good:{"U":0,
                                "patch":None}
                            for good in self.model.goods}

            
            patch_moves = [(curr_row + dy, curr_col + dx)  
                           for dy in self.model.nav_dict[self.vision] if 0 <= curr_row + dy < 50
                           for dx in self.model.nav_dict[self.vision][dy] if 0 <= curr_col + dx < 50]
            
            # shuffle patches so not movement biased in one direction
            random.shuffle(patch_moves)
            near_empty_patch = False #{good: False for good in self.good}
            empty_patches = []
            for coords in patch_moves:   
                if coords in self.model.empty_patches.keys:
                    row, col = coords[0], coords[1]
                    empty_patch = self.model.patches_dict[row][col]
                    empty_patches.append(empty_patch)
                    if self.optimizer: 
                        patch_q = self.getPatchUtility(empty_patch)
                    else: 
                        patch_q = empty_patch.Q
                    patch_good = empty_patch.good
                    try: 
                        if patch_q > max_patch[patch_good]["U"]:
                            # only mark near empty patch if Q > 0
                            near_empty_patch = True
                            max_patch[patch_good]["patch"] = empty_patch
                            max_patch[patch_good]["U"] = patch_q
                    except: 
                        
                        print(getattr(self, "sugar"), getattr(self, "water"))
            return max_patch, near_empty_patch, empty_patches    

        def moveToMaxEmptyPatch(curr_row, curr_col, 
                                max_patch, near_empty_patch,
                                target, not_target, empty_patches):
            
            def basicMove(max_patch):
                max_q = max(max_patch[good]["U"] for good in max_patch )
                # include both max water and max sugar patch if moth have max_q
                max_patches = [good for good in max_patch if max_patch[good]["U"] == max_q]
                #randomly select max water or max sugar patch
                max_good = random.choice(max_patches) 
                target_patch = max_patch[max_good]["patch"]
                return target_patch
            
            def chooseTargetOrAlternate(max_patch, target, not_target, empty_patches):
                if type(max_patch[target]["patch"]) is Patch:
                    target_patch = max_patch[target]["patch"]
                    return target_patch
                # use elif with return within the if statement, that way
                # an error is thrown if target == not_target
                elif type(max_patch[not_target]["patch"]) is Patch:
                    # choose patch that moves agent closest to target 
                    # commodity
                    max_val = float("-inf")
                    min_val = float("inf")
                    for patch in empty_patches:
                        coord_sum = patch.col + patch.row 
                        if target == "sugar":
                            if coord_sum < min_val:
                                max_val = coord_sum
                                target_patch = patch
                        elif target == "water":
                            if coord_sum > max_val:
                                min_val = coord_sum
                                target_patch = patch
                                                
                    return target_patch
            
            ###################################################################  
            
    
            if near_empty_patch:
                if self.basic or self.optimizer and not self.arbitrageur:
                    target_patch = basicMove(max_patch)
                else:
                    target_patch = chooseTargetOrAlternate(max_patch, target, not_target, empty_patches)
                # track relative position to move image
                if target_patch is not None: 
                    self.dx, self.dy = target_patch.col - curr_col, target_patch.row - curr_row
                # set new coordinates
                    self.row, self.col =  target_patch.row, target_patch.col 
                # register agent to patch
                    self.model.patches_dict[self.row][self.col].agent = self
                # set agent at old patch to none
                    self.model.patches_dict[curr_row][curr_col].agent = None
                # register old patch to empty_patches
                    self.model.empty_patches[curr_row, curr_col] = self.model.patches_dict[curr_row][curr_col]
                # remove agent's current position from emtpy_patches
                    del self.model.empty_patches[self.row, self.col]
            else:
                self.dx = 0
                self.dy = 0
    ###############################################################################

        # save agent coords to track agent movement, changes in (not) empty patches
        curr_row, curr_col = self.row, self.col
        max_patch, near_empty_patch, empty_patches = findMaxEmptyPatch(curr_row, curr_col)
        random.shuffle(empty_patches)
        
        # if near_empty_patch:
        moveToMaxEmptyPatch(curr_row, curr_col, max_patch, 
             near_empty_patch, self.target, self.not_target, empty_patches)


    
    def harvest(self):    
        agent_patch = self.model.patches_dict[self.row][self.col]
        setattr(self, agent_patch.good, getattr(self, agent_patch.good) + agent_patch.Q)
        agent_patch.Q = 0 

    def paretoImproving(self, price, target): 
        new_wealth = {"water": 0, "sugar": 0}
        pareto_improvement = False
        # if target == "water": 
        #     if price >= 1: 
        #         new_wealth["water"] = self.wealth_by_good["water"] + (price / 0.5)
        #         new_wealth["sugar"] = self.wealth_by_good["sugar"] - (1 / 0.5)
        #     elif price < 1: 
        #         new_wealth["water"] = self.wealth_by_good["water"] + (1 / 0.5)
        #         new_wealth["sugar"] = self.wealth_by_good["sugar"] - ((1/price) / 0.5)
            
        # elif target == "sugar": 
        #     if price >= 1: 
        #         new_wealth["water"] = self.wealth_by_good["water"] - (price / 0.5)
        #         new_wealth["sugar"] = self.wealth_by_good["sugar"] + (1 / 0.5)
        #     elif price < 1: 
        #         new_wealth["water"] = self.wealth_by_good["water"] - (1 / 0.5)
        #         new_wealth["sugar"] = self.wealth_by_good["sugar"] + ((1/price) / 0.5)
        # else: 
        #     print(target, self, price)
        new_wealth[self.target] = self.wealth_by_good[self.target] + (1 / 0.5)
        new_wealth[self.not_target] = self.wealth_by_good[self.not_target] - (price / 0.5)

         
        if new_wealth["water"] > 0 and new_wealth["sugar"] > 0: 
            new_utility = (new_wealth["sugar"] ** self.sugar_utility_weight) * (new_wealth["water"] ** self.water_utility_weight)
            if new_utility > self.utility: 
                pareto_improvement = True 

        return pareto_improvement
        
    def trade(self):
        
        def askToTrade(patch):
            partner = patch.agent
            #check if partner is looking for good agent is selling
            if not self.optimizer and not partner.optimizer: 
                right_good = self.target != partner.target
            elif self.optimizer and partner.optimizer: 
                right_good = self.MRS != partner.MRS
            elif self.optimizer and not partner.optimizer: 
                # partners relative wealth is higher than the price their partner is charging 
                if self.MRS > partner.reservation_demand["sugar"]["price"]: 
                    right_good = partner.target == "sugar"
                elif self.MRS < partner.reservation_demand["water"]["price"]: 
                    right_good = partner.target == "water"
                else: 
                    right_good = False
            elif not self.optimizer and partner.optimizer: 
                if partner.MRS > self.reservation_demand["sugar"]["price"]: 
                    right_good = self.target == "sugar"
                elif partner.MRS < self.reservation_demand["water"]["price"]: 
                    right_good = self.target == "water"
                else: 
                    right_good = False
                

            return partner, right_good

        def bargain(partner):
            can_trade = False
            price = None
            if not self.optimizer and not partner.optimizer:        
                WTP = self.reservation_demand[self.target]["price"] 
                WTA = partner.reservation_demand[self.target]["price"]

                # assume bargaining leads to average price...
                # maybe change to random logged distribution later
                price, can_trade = (gmean((WTA, WTP)), True) if WTP > WTA else (None, False)
            elif partner.optimizer and self.optimizer: 
                    # partner values water more than self 
                    if self.MRS > partner.MRS: 
                        self.target = "sugar"
                        self.not_target = "water"
                        partner.target = "water"
                        partner.not_target = "sugar"
                        price = np.sqrt(self.MRS * partner.MRS)
                        if getattr(partner, "sugar") > 1 and getattr(self, "water") > price: 
                            can_trade = True
                    # partner values sugar more than self 
                    elif self.MRS < partner.MRS: 
                        self.target = "water"
                        self.not_target = "sugar"
                        partner.target = "sugar"
                        partner.not_target = "water"
                        price = np.sqrt(self.MRS * partner.MRS)
                        if getattr(partner, "water") > 1 and getattr(self, "sugar") > price:
                            can_trade = True
                    elif self.MRS == partner.MRS: 
                        can_trade = False
                        price = None
                    else: 
                        price, can_trade = None, False 
                        print(self.MRS, partner.MRS)
            elif self.optimizer and not partner.optimizer: 
                    if self.MRS > partner.reservation_demand["sugar"]["price"]: 
                        self.target = "sugar"
                        self.not_target = "water"
                        price = np.sqrt(self.MRS * partner.reservation_demand["sugar"]["price"])
                        can_trade = self.target != partner.target
                    elif self.MRS < partner.reservation_demand["water"]["price"]: 
                        self.target = "water"
                        self.not_target = "sugar"
                        price = np.sqrt(self.MRS * partner.reservation_demand["water"]["price"])
                        can_trade = self.target != partner.target 
                    else: 
                        can_trade = False
                        price = None
            elif not self.optimizer and partner.optimizer: 
                    if partner.MRS > self.reservation_demand["sugar"]["price"]: 
                        partner.target = "sugar"
                        partner.not_target = "water"
                        price = np.sqrt(partner.MRS * self.reservation_demand["sugar"]["price"])
                        can_trade = partner.target != self.target
                    elif partner.MRS < self.reservation_demand["water"]["price"]: 
                        partner.target = "water"
                        partner.not_target = "sugar"
                        price = np.sqrt(partner.MRS* self.reservation_demand["water"]["price"])
                        can_trade = partner.target != self.target
                    else: 
                        can_trade = False
                        price = None


            return price, can_trade
                

        def executeTrade(partner, price):
            self_res_min = self.reservation_demand[self.not_target]["quantity"]
            partner_res_min = partner.reservation_demand[self.target]["quantity"]
            #   optimizers must trade iteratively for now, the number of tradees could be precalculated later on. 
            if not self.optimizer and not partner.optimizer: 
                # calculate how many trades each agent would make to arrive at their 
                # reservation demand for the good they are giving away
            
                self_excess_demand = getattr(self, self.not_target) - self_res_min
                partner_excess_demand = getattr(partner, self.target) - partner_res_min
                self_max_trades = np.floor(self_excess_demand / price)
                partner_max_trades = np.floor(partner_excess_demand)

                # number of trades is determined by which agent has to stop trading first 
                num_trades = min(self_max_trades, partner_max_trades)
                if num_trades > 1 and self_excess_demand > price  and partner_excess_demand > 1: 
                    
            
                    # adjust values of goods for agents based on how many trades were made 
                    setattr(self, self.not_target, (getattr(self, self.not_target) - (num_trades * price)))
                    setattr(self, self.target, (getattr(self, self.target) + num_trades))
                    setattr(partner, self.target, (getattr(partner, self.target) - num_trades))
                    setattr(partner, self.not_target, (getattr(partner, self.not_target) + (num_trades * price)))

                    transaction_price = price if self.target == "sugar" else 1 / price
                    self.model.transaction_prices[self.target].append(transaction_price)
                    self.model.transaction_weights[self.target].append(num_trades)
                    self.model.all_prices.append(transaction_price)
                    self.model.all_prices_weights.append(num_trades)
                    self.model.total_exchanges += num_trades
                    if self.arbitrageur:
                            self.expected_price =  (self.expected_price * (
                                self.present_price_weight) + num_trades * transaction_price) / (self.present_price_weight + num_trades)
                            
            elif self.optimizer and partner.optimizer: 

                if self.MRS > partner.MRS: # self is relatively richer in water than partner 

                    while (self.MRS > partner.MRS and self.paretoImproving(price, "water") and partner.paretoImproving(1, "sugar")):
                            
                            setattr(self, self.target, getattr(self, self.target) + 1)
                            setattr(self, self.not_target, getattr(self, self.not_target) - price)
                            setattr(partner, self.target, getattr(partner, self.target) - 1)
                            setattr(partner, self.not_target, getattr(partner, self.not_target) + price)
                            
                            # save price of sugar or implied price of sugar for every exchange
                            transaction_price = price if self.target == "sugar" else 1 / price
                            self.model.transaction_prices[self.target].append(transaction_price)
                            self.model.transaction_weights[self.target].append(1)
                            self.model.all_prices.append(transaction_price)
                            self.model.all_prices_weights.append(1)
                            self.model.total_exchanges += 1
                            self.updateParams(trade=True)
                            partner.updateParams(trade=True)

                            price = np.sqrt(self.MRS * partner.MRS)
                            if self.arbitrageur:
                                self.expected_price = (self.expected_price * (
                                    self.present_price_weight) + transaction_price) / self.present_price_weight
                                
                elif self.MRS < partner.MRS: 
                        
                        while (self.MRS < partner.MRS and self.paretoImproving(price, "sugar") and partner.paretoImproving(1, "water")): 
                    
                            setattr(self, self.target, getattr(self, self.target) + 1)
                            setattr(self, self.not_target, getattr(self, self.not_target) - price)
                            setattr(partner, self.target, getattr(partner, self.target) - 1)
                            setattr(partner, self.not_target, getattr(partner, self.not_target) + price)
                            
                            # save price of sugar or implied price of sugar for every exchange
                            transaction_price = price if self.target == "sugar" else 1 / price
                            self.model.transaction_prices[self.target].append(transaction_price)
                            self.model.transaction_weights[self.target].append(1)
                            self.model.all_prices.append(transaction_price)
                            self.model.all_prices_weights.append(1)
                            self.model.total_exchanges += 1
                            self.updateParams(trade=True)
                            partner.updateParams(trade=True)
                            # self.MRS = self.wealth_by_good["water"] / self.wealth_by_good["sugar"]
                            # partner.MRS = partner.wealth_by_good["water"] / partner.wealth_by_good["sugar"]
                            price = np.sqrt(self.MRS * partner.MRS)
                            if self.arbitrageur:
                                self.expected_price = (self.expected_price * (
                                    self.present_price_weight) + transaction_price) / self.present_price_weight
                                
                                
            elif self.optimizer and not partner.optimizer:
                if self.MRS > price: 
                    while (self.MRS > price and getattr(partner, "water") > partner_res_min + 1 and self.paretoImproving(1, "sugar")):
                            
                            setattr(self, self.target, getattr(self, self.target) + 1)
                            setattr(self, self.not_target, getattr(self, self.not_target) - price)
                            setattr(partner,self.target, getattr(partner, self.target) - 1)
                            setattr(partner, self.not_target, getattr(partner, self.not_target) + price)
                            
                            # save price of sugar or implied price of sugar for every exchange
                            transaction_price = price if self.target == "sugar" else 1 / price
                            self.model.transaction_prices[self.target].append(transaction_price)
                            self.model.transaction_weights[self.target].append(1)
                            self.model.all_prices.append(transaction_price)
                            self.model.all_prices_weights.append(1)
                            self.model.total_exchanges += 1
                            self.updateParams(trade=True)
                            price = np.sqrt(self.MRS * partner.reservation_demand["sugar"]["price"])
                            if self.arbitrageur:
                                self.expected_price = (self.expected_price * (
                                    self.present_price_weight) + transaction_price) / self.present_price_weight
                elif self.MRS < price:  
                        
                        while (self.MRS < price and getattr(partner, self.target) > partner_res_min + 1 and self.paretoImproving(1, "water")): 
                    
                            setattr(self, self.target, getattr(self, self.target) + 1)
                            setattr(self, self.not_target, getattr(self, self.not_target) - price)
                            setattr(partner,self.target, getattr(partner, self.target) - 1)
                            setattr(partner, self.not_target, getattr(partner, self.not_target) + price)
                            
                            # save price of sugar or implied price of sugar for every exchange
                            transaction_price = price if self.target == "sugar" else 1 / price
                            self.model.transaction_prices[self.target].append(transaction_price)
                            self.model.transaction_weights[self.target].append(1)
                            self.model.all_prices.append(transaction_price)
                            self.model.all_prices_weights.append(1)
                            self.model.total_exchanges += 1
                            self.updateParams(trade=True)
                            price = np.sqrt(self.MRS * partner.reservation_demand["water"]["price"])
                            if self.arbitrageur:
                                self.expected_price = (self.expected_price * (
                                    self.present_price_weight) + transaction_price) / self.present_price_weight
                                
               

            elif not self.optimizer and partner.optimizer:
                if partner.MRS > price: 
                    while (partner.MRS > price and getattr(self, partner.target) > self_res_min + price and partner.paretoImproving(1, "sugar")):
                            
                            setattr(self, self.target, getattr(self, self.target) + 1)
                            setattr(self, self.not_target, getattr(self, self.not_target) - price)
                            setattr(partner,self.target, getattr(partner, self.target) - 1)
                            setattr(partner, self.not_target, getattr(partner, self.not_target) + price)
                            
                            # save price of sugar or implied price of sugar for every exchange
                            transaction_price = price if self.target == "sugar" else 1 / price
                            self.model.transaction_prices[self.target].append(transaction_price)
                            self.model.transaction_weights[self.target].append(1)
                            self.model.all_prices.append(transaction_price)
                            self.model.all_prices_weights.append(1)
                            self.model.total_exchanges += 1
                            partner.updateParams(trade=True)
                            price = np.sqrt(partner.MRS * self.reservation_demand["sugar"]["price"])
                            if self.arbitrageur:
                                self.expected_price = (self.expected_price * (
                                    self.present_price_weight) + transaction_price) / self.present_price_weight
                elif partner.MRS < price:  
                        
                        while (partner.MRS < price and getattr(self, partner.target) >  self_res_min + 1 and partner.paretoImproving(1, "water")): 
                    
                            setattr(self, self.target, getattr(self, self.target) + 1)
                            setattr(self, self.not_target, getattr(self, self.not_target) - price)
                            setattr(partner,self.target, getattr(partner, self.target) - 1)
                            setattr(partner, self.not_target, getattr(partner, self.not_target) + price)
                            
                            # save price of sugar or implied price of sugar for every exchange
                            transaction_price = price if self.target == "sugar" else 1 / price
                            self.model.transaction_prices[self.target].append(transaction_price)
                            self.model.transaction_weights[self.target].append(1)
                            self.model.all_prices.append(transaction_price)
                            self.model.all_prices_weights.append(1)
                            self.model.total_exchanges += 1
                            partner.updateParams(trade=True)
                            price = np.sqrt(partner.MRS * self.reservation_demand["water"]["price"])
                            if self.arbitrageur:
                                self.expected_price = (self.expected_price * (
                                    self.present_price_weight) + transaction_price) / self.present_price_weight

                                   
        def herdTraits(agent, partner):
            def turn_off_other_primary_breeds(agent, breed, have_attr):
                if attr in self.model.primary_breeds:
                    # if breed changed, set other values false
                    if have_attr == True:
                        for brd in self.model.primary_breeds:
                            if brd != breed: 
                                setattr(agent, brd, False)
            # agent will copy partner traits. Sometimes, agent is self, 
            # sometimes not, so we call agent.selectBreedParameters at end
            if agent.herder:
                if agent.top_wealth < partner.wealth:
                    copy_attributes = partner.defineInheritance()
                    if agent.model.genetic:
                        for attr, val in copy_attributes.items():
                            if random.random() <= agent.model.cross_over_rate:
                                setattr(agent, attr, val)
                                # if attr is a primary breed, other breeds 
                                # will be switched off
                                turn_off_other_primary_breeds(agent, attr, val)
                        
                        # set basic True if all primary breeds switched to false
                        # due to genetic algorithm
                        if True not in (getattr(agent, breed)
                                        for breed in self.model.primary_breeds):
                            agent.setBreedBasic(herder = agent.herder)
                        agent.selectBreedParameters(mutate = False, parent = None, 
                                                   herding = True, partner = partner)
          
                    else: 
                        for attr, val in copy_attributes.items():
                            setattr(agent, attr, val)             

    ###############################################################################            

        # find trading partner
        neighbor_patches = [(self.row + i, self.col + j)
                        for i in self.model.nav_dict[1] if 0 <= self.row + i < 50
                        for j in self.model.nav_dict[1][i] if 0 <= self.col + j < 50 ]
        random.shuffle(neighbor_patches)
        for coords in neighbor_patches:
            if coords not in self.model.empty_patches.keys:
                row, col = coords[0], coords[1]
                target_patch = self.model.patches_dict[row][col]
                # if partner found on patch, ask to trade
                partner, right_good = askToTrade(target_patch)
                if right_good: 
                    price, can_trade = bargain(partner)
                else:
                    price, can_trade = None, False 
                # check if partner has appropriate goods and WTP, WTA
                if can_trade:
                                        
                    # execute trades
                    executeTrade(partner, price)
                    if self.herder:
                        if self.top_wealth <  partner.wealth:
                            herdTraits(self, partner)
                    elif partner.herder:
                        if partner.top_wealth < self.wealth:    
                            herdTraits(partner, self)
                    
                    #  genetic?
                    # only trade with one partner per agent search
                    # agents can be selected by more than one partner
                    # if not self.optimizer: 
                    # break
