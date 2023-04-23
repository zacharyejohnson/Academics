import copy
import shelve
import time
import pandas as pd
import random
import math
from randomdict import RandomDict
from Patch import *
import numpy as np 
import matplotlib
import gc
from Agent import Agent
from memory_profiler import memory_usage
from scipy.stats.mstats import gmean
matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt
import cython
#from DataCollector import DataCollector
#Model.py
class Model():
    def __init__(self, gui, num_agents, mutate, genetic, live_visual, plots, agent_attributes,
                 model_attributes, primary_breeds = ["basic", "optimizer", "arbitrageur"]):
        
        self.initial_population = num_agents
        self.mutate = mutate
        self.genetic = genetic
        self.model_attributes = model_attributes
        self.agent_attributes = agent_attributes
        self.attributes = agent_attributes + model_attributes
        self.primary_breeds = primary_breeds
        self.drop_attr = ["col", "row", "dx", "dy", "id", "wealth", "top_wealth",
             "sugar", "water","target", "not_target", 
             "exchange_target", "not_exchange_target", "parent", "MRS", "wealth_by_good", "sugar_utility_weight", "water_utility_weight"]#, "price_change", "quantity_change"]#, "image"]
        #  "exchange_target", "not_exchange_target", "parent", "image", "arbitrageur", "herder"]
        self.live_visual = live_visual
        if live_visual:
            self.drop_attr.append("image")


        # clean up model attributes to ensure only pulling attributes for agent types in the current run 
        if "num_optimizers" in self.attributes and "optimizer" not in self.primary_breeds: 
             self.model_attributes.remove("num_optimizers")
             self.attributes.remove("num_optimizers")

        for breed in ["basic", "optimizer", "arbitrageur"]:
            if breed not in self.primary_breeds: 
                for attr in self.attributes: 
                    if breed in attr: 
                        self.model_attributes.remove(attr)
                        self.attributes.remove(attr)



        self.plots = plots
        
        self.GUI = gui

###################### MODEL PARAMETERS ##############################
        # goods to be included in model 
        self.goods = ["sugar", "water"]
        # initial distribution of wealth 
        self.init_good_ranges = {"min": 10, "max": 25}

        self.goods_params = {good:{"min":10,
                                   "max":25} for good in self.goods}
        # rates of good consumption 
        self.consumption_rate = {good : 0.5 for good in self.goods}
        # initial rates of demand 
        self.max_init_demand_vals = {"price": {"min": 0.5, "max": 2}, 
                                "quantity": {"min": 10, "max": 25}}
        # closest utility exponents for goods can be to 0 or 1 
        self.utility_bound = 0.1

        self.total_agents_created = 0

        self.max_vision = 1

        self.max_mutate_rate = 0.5

        self.cross_over_rate = 0.5

        
        self.secondary_breeds = ["herder"]
        
        self.breeds = self.primary_breeds + self.secondary_breeds

        if "basic" in primary_breeds: 
            self.breed_probabilities = {"basic":1, # if you are not a basic, you are a switcher
                                    "herder":0,
                                    "arbitrageur":0, 
                                    "optimizer": 0}
        else: 
            self.breed_probabilities = {"basic":0, # if you are not a basic, you are a switcher
                                    "herder":0,
                                    "arbitrageur":0, 
                                    "optimizer": 1}

        self.nav_dict = {
            v:{
                i:{
                    j: True for j in range(-v, v + 1) if 0 < (i ** 2 + j ** 2) <= (v ** 2)}
                for i in range(-v, v + 1)}
            for v in range(1, self.max_vision + 1)}

        self.sugarMap = pd.read_csv('sugar-map.txt', header = None, sep = ' ')
        for key in self.sugarMap:
            self.sugarMap[key] = self.sugarMap[key].add(1)
        self.rows, self.cols = self.sugarMap.shape
        self.initializePatches()
        self.initializeAgents()
        self.data_dict = {}#shelve.open("shelves\\masterShelve", writeback = True)
        for attribute in self.attributes:
            self.data_dict[attribute] = {}#shelve.open("shelves\\subshelve-"+attribute, writeback = True) 

        self.transaction_prices = {good: [1] for good in self.goods}
        self.transaction_weights = {good: [1] for good in self.goods}
        self.all_prices = [1]
        self.all_prices_weights = [1]
        self.water_avg_price = 1
        self.sugar_avg_price = 1
        self.total_avg_price = 1
        self.total_exchanges = 0
        self.total_variance = 0
        self.water_variance = 0 
        self.sugar_variance = 0 
        self.population = len(self.agent_dict)
        self.basicbasic_res_demand = 1
        self.basicherder_res_demand = 1
        self.arbitrageurbasic_res_demand = 1
        self.arbitrageurherder_res_demand = 1
        self.optimizer_MRS = 1 
        self.agent_wealth = 0
        self.runtime = 0

    def initializePatches(self):
        self.patches_dict = {i:{j:0}
                           for i in range(self.rows) for j in range(self.cols)}
        for i in range(self.rows):
            for j in range(self.cols):
                good = "sugar" if i+j < self.cols else "water"
                self.patches_dict[i][j] = Patch(self,  i , j, 
                                              self.sugarMap[i][j], good)
        self.empty_patches = RandomDict({
            (i,j):self.patches_dict[i][j]
            for i in range(self.rows) for j in range(self.cols)})
                
        
    def initializeAgents(self):
        self.agent_dict = {}
        for i in range(self.initial_population):
            self.total_agents_created += 1
            ID = self.total_agents_created
            row, col = self.chooseRandomEmptyPatch()  
            #all agents are initially basic 
            agent = Agent(self, row, col, ID)
            self.agent_dict[ID] = agent
            self.patches_dict[row][col].agent = agent
        
    def chooseRandomEmptyPatch(self):
        row, col = self.empty_patches.random_key() 
        del self.empty_patches[row, col]
        return row, col
    

    def simulate_interactions(self, period): 
        agent_list = list(self.agent_dict.values())
        random.shuffle(agent_list)
        if self.model_attributes != []: # and self.plots: 
            self.num_basicherders = 0
            self.num_arbitrageurherders = 0
            self.num_basicbasics = 0 
            self.num_arbitrageurbasics = 0
            self.num_optimizers = 0 
            basicbasic_res_demand = []
            basicherder_res_demand = []
            arbitrageurbasic_res_demand = []
            arbitrageurherder_res_demand = []
            optimizer_MRS = []
        # temp_dict={}
        # for attribute in self.agent_attributes:
        #     temp_dict[attribute] = []
        self.temp_wealth = 0
        self.temp_wealth += self.agent_wealth
        self.temp_pop = 0 
        self.temp_pop += self.population
        self.agent_wealth = 0
        self.consumption = 0
        for agent in agent_list:
                if agent.check_alive(): 
                    agent.move()
                    # if agent.sugar < -.5 or agent.water < -.5: 
                    #     print("MOVE", agent.sugar, agent.water, agent.basic, agent.herder, agent.arbitrageur)
                    #     continue
                    agent.harvest()
                    if agent.sugar < -.5 or agent.water < -.5: 
                        print("HARVEST", agent.sugar, agent.water, agent.basic, agent.herder, agent.arbitrageur)
                        del self.agent_dict[agent.id]
                        self.empty_patches[agent.row, agent.col] = self.patches_dict[agent.row][agent.col]
                        continue
                    agent.trade()
                    if agent.sugar < -.5 or agent.water < -.5: 
                        print("TRADE", agent.sugar, agent.water, agent.basic, agent.herder, agent.arbitrageur)
                        continue
                    
                    agent.consume()
                    if agent.sugar < -.5 or agent.water < -.5: 
                        print("CONSUME", agent.sugar, agent.water, agent.basic, agent.herder, agent.arbitrageur)
                        continue


                    agent.reproduce()
                    if agent.sugar < -.5 or agent.water < -.5: 
                        print("REPRODUCE", agent.sugar, agent.water, agent.basic, agent.herder, agent.arbitrageur)
                        continue
                    agent.updateParams()
                    if agent.sugar < -.5 or agent.water < -.5: 
                        print("UPDATEPARAMS", agent.sugar, agent.water, agent.basic, agent.herder, agent.arbitrageur)
                        continue
                    if agent in self.agent_dict.values(): 
                        self.agent_wealth += agent.wealth
                        self.consumption += 1
                        



        

                # #agent statistics tracking 
                if self.model_attributes != []: # and self.plots:
                    if not agent.herder and not agent.arbitrageur and not agent.optimizer: 
                        self.num_basicbasics += 1
                        basicbasic_res_demand.append(agent.reservation_demand["sugar"]["price"])
                    elif agent.herder and not agent.arbitrageur and not agent.optimizer: 
                        self.num_basicherders += 1
                        basicherder_res_demand.append(agent.reservation_demand["sugar"]["price"])
                    elif not agent.herder and agent.arbitrageur and not agent.optimizer: 
                        self.num_arbitrageurbasics += 1
                        arbitrageurbasic_res_demand.append(agent.reservation_demand["sugar"]["price"])
                    elif agent.herder and agent.arbitrageur and not agent.optimizer: 
                        self.num_arbitrageurherders += 1
                        arbitrageurherder_res_demand.append(agent.reservation_demand["sugar"]["price"])
                    elif agent.optimizer: 
                        self.num_optimizers += 1
                        optimizer_MRS.append(agent.MRS)

        if self.model_attributes != []: # and self.plots:
            if len(basicbasic_res_demand) > 0:
                self.basicbasic_res_demand = gmean(basicbasic_res_demand)
            if len(basicherder_res_demand) > 0:
                self.basicherder_res_demand = gmean(basicherder_res_demand)
            if len(arbitrageurbasic_res_demand) > 0:
                self.arbitrageurbasic_res_demand = gmean(arbitrageurbasic_res_demand)
            if len(arbitrageurherder_res_demand) > 0:
               self.arbitrageurherder_res_demand = gmean(arbitrageurherder_res_demand)
            if len(optimizer_MRS) > 0:
               self.optimizer_MRS = gmean(optimizer_MRS)
        # for attribute, val in temp_dict.items():
        #         self.data_dict[attribute].__setitem__(str(period), np.mean(val)

    def runModel(self, periods):           
        # Update the plot at each period
        for period in range(1, periods + 1):
            # Simulate the agents interacting
            start1 = time.time()
            self.growPatches()
            self.simulate_interactions(period)
            setattr(self, "population", len(self.agent_dict))
            setattr(self, "wealth_per_capita", self.agent_wealth / self.population)
            setattr(self, "savings", self.agent_wealth / self.population - self.temp_wealth / self.temp_pop)
            setattr(self, "tech_eff_capital", (self.savings +  self.consumption) / self.population)

            if period > 1: 
                avg_water = gmean(self.transaction_prices['water'], weights=self.transaction_weights['water'])
                avg_sugar = gmean(self.transaction_prices['sugar'], weights=self.transaction_weights['sugar'])
                avg_total = gmean(self.all_prices, weights=self.all_prices_weights)
                setattr(self, "water_avg_price", avg_water)
                setattr(self, "sugar_avg_price", avg_sugar)
                setattr(self, "total_avg_price", avg_total)
                # setattr(self, "total_variance", np.std(self.all_prices))
                # setattr(self, "water_variance", np.std(self.transaction_prices['water']))
                # setattr(self, "sugar_variance", np.std(self.transaction_prices['sugar']))

            self.collectData(str(period))
            end1 = time.time()
            self.runtime = end1-start1
            if period % 10 == 0: 
                print(period, self.runtime)


            if self.live_visual and period % self.GUI.every_t_frames_GUI == 0: 
                self.GUI.updatePatches()
                self.GUI.moveAgents()
                self.GUI.canvas.update()
            if period == periods:
                mem_usage = memory_usage(-1, interval=1)#, timeout=1)
                print(period, "end memory usage before sync//collect:", mem_usage[0], sep = "\t")
                gc.collect()
                mem_usage = memory_usage(-1, interval=1)#, timeout=1)
                print(period, "end memory usage after sync//collect:", mem_usage[0], sep = "\t")

                
        if self.plots:
            self.plot_data()

    def plot_data(self):

        num_rows = int((len(self.data_dict) / 2)) -4
        num_cols = 2
        self.fig, self.axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20,30))


        # Iterate over the data in the dictionary
        j = 0 
        for i, (variable, data) in enumerate(self.data_dict.items()):
            
            if "num" in variable: 
                #plot proportions of each agent over time in final plot 
                self.axs[num_rows - 1, 1].plot(np.array(list(data.values())) / np.array(list(self.data_dict["population"].values())), label = variable[4:]) # get rid of "num_"
                self.axs[num_rows - 1, 1].set_ylabel("Population\nShare")
                self.axs[num_rows - 1, 1].legend(fontsize=7, loc=2)
                j += 1
            elif "price" in variable:
                self.axs[num_rows - 1, 0].plot(data.values(), label = variable[:9]) # get rid of "_avg_price"... etc 
                self.axs[num_rows - 1, 0].set_ylabel("Prices")
                self.axs[num_rows - 1, 0].legend(fontsize=7, loc=2)
                j += 1
                self.axs[num_rows - 2, 0].plot(np.diff(list(data.values())), label = variable[:9])
                self.axs[num_rows - 2, 0].set_ylabel("Price\nVariance")
                self.axs[num_rows - 2, 0].legend(fontsize=7)
            elif "res_demand" in variable:
                self.axs[num_rows - 2, 1].plot(data.values(), label = variable[:2])
                self.axs[num_rows - 2, 1].set_ylabel("Reservation\nDemands")
                self.axs[num_rows - 2, 1].legend(fontsize=7, loc=2)
                j += 1

            else: 
            


                # Get the row and column for the current plot
                row = (i-j) // 2
                col = (i-j) % 2
                print(variable)
                # Plot the data for the current variable
                self.axs[row, col].plot(data.values())
                self.axs[row, col].set_xlabel('Period')
                self.axs[row, col].set_ylabel(variable.replace("_", "\n"))
            

        # Redraw the plots
        self.fig.canvas.draw()
        plt.show()



                    
    # the reproduce funtion is implemented in model class to avoid circular dependencies in agent class 
    # def agent_reproduce(self, agent): 
    #     if agent in self.agent_dict.values(): 
    #         can_reproduce = True
    #         for good in self.goods: 
    #             if getattr(agent, good) < agent.reproduction_criteria[good]: 
    #                 can_reproduce = False 
    #                 break
            
    #         if can_reproduce: 

    #             def child_breed(): 
    #                 # mutation means that agent switches breed 
    #                 def primary_breed(): 
    #                     if random.random() < agent.mutate_rate: 
    #                         breed = "basic" if agent.arbitrageur else "arbitrageur"
    #                     else: 
    #                         breed = "arbitrageur" if agent.arbitrageur else "basic"

    #                     return breed

                            
    #                 def secondary_breed():
    #                     if random.random() < agent.mutate_rate: 
    #                         breed = "basic" if agent.herder == True else "herder"
    #                     else: 
    #                         breed = "herder" if agent.herder == True else "basic"

    #                     return breed

    #                 return primary_breed(), secondary_breed()

    #             child_breed = child_breed()

    #             self.total_agents_created += 1
    #             row, col = self.chooseRandomEmptyPatch()  
    #             ID = self.total_agents_created
                
    #             if child_breed == ("basic", "basic"): 
    #                 self.num_basicsbasics += 1
    #                 self.agent_dict[ID] =  BasicAgent(model=self, row=row, col=col, ID=ID, parent=agent)
    #             elif child_breed == ("basic", "herder"): 
    #                 self.num_basicherders += 1
    #                 self.agent_dict[ID] =  BasicHerder(model=self, row=row, col=col, ID=ID, parent=agent)
    #             elif child_breed == ("arbitrageur", "basic"): 
    #                 self.num_arbitrageursbasics += 1
    #                 self.agent_dict[ID] =  Arbitrageur(model=self, row=row, col=col, ID=ID, parent=agent)
    #             elif child_breed == ("arbitrageur", "herder"):
    #                 self.num_arbitrageursherders += 1
    #                 self.agent_dict[ID] = ArbitrageurHerder(model=self, row=row, col=col, ID=ID, parent=agent)
    #             else: 
    #                 print("error")

    #             # add good quantities to new agent, deduct from parent
    #             # self.agent_dict[ID].goods = {}
    #             # for good in self.goods:
    #             #      agent.goods[good] -= agent.reproduction_criteria[good]
    #             #      self.agent_dict[ID].goods[good] = 0
    #             #      self.agent_dict[ID].goods[good] += agent.reproduction_criteria[good]
    #             self.agent_dict[ID].top_wealth = agent.get_wealth()
    #             self.agent_dict[ID].wealthiest = agent
    #             self.patches_dict[row][col].agent =  self.agent_dict[ID]
    #             if self.live_visual: 
    #                 self.GUI.draw_agent(self.agent_dict[ID])
    #             agent.reproduced = True

    
    def growPatches(self):
        for row in self.patches_dict:
            for patch in self.patches_dict[row].values():
                if patch.Q < patch.maxQ:
                    patch.Q += 1


    def collectData(self, period):
        
        def collectAgentAttributes():
            temp_dict={}
            for attribute in self.agent_attributes:
                temp_dict[attribute] = []
            for ID, agent in self.agent_dict.items():
                for attribute in self.agent_attributes:
                    temp_dict[attribute].append(getattr(agent, attribute)) 
            
            for attribute, val in temp_dict.items():
                self.data_dict[attribute][period] = np.mean(val)

        def collectModelAttributes():
            for attribute in self.model_attributes:
                self.data_dict[attribute][period] = getattr(self, attribute)
                
        #collectAgentAttributes()
        collectModelAttributes()
