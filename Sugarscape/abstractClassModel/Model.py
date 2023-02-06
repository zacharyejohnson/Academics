import copy
import shelve
import time
import pandas as pd
import random
import math
from randomdict import RandomDict
from Patch import *
from BasicAgent import BasicAgent
from BasicHerder import BasicHerder
from Arbitrageur import Arbitrageur
from ArbitrageurHerder import ArbitrageurHerder
import numpy as np 
import matplotlib
import gc
from memory_profiler import memory_usage
from scipy.stats.mstats import gmean
matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt
#Model.py
class Model():
    def __init__(self, gui, num_agents, mutate, genetic, live_visual, plots, agent_attributes,
                 model_attributes):
        
        self.initial_population = num_agents
        self.mutate = mutate
        self.genetic = genetic
        self.model_attributes = model_attributes
        self.agent_attributes = agent_attributes
        self.attributes = agent_attributes + model_attributes
        self.drop_attr = ["col", "row", "patch", "id", "wealth", "top_wealth",
            "sugar", "water","target", "not_target",
            "exchange_target", "not_exchange_target", "parent", "image", "arbitrageur", "herder"]
        self.live_visual = live_visual
        self.plots = plots
        if live_visual:
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
        self.init_demand_vals = {"price": {"min": 0.5, "max": 2}, 
                                "quantity": {"min": 10, "max": 25}}
        self.total_agents_created = 0

        self.max_vision = 1

        self.max_mutate_rate = 0.5

        self.cross_over_rate = 0.5

        self.primary_breeds = {"basic", "arbitrageur"}
        self.secondary_breeds = {"basic", "herder"}
        self.breeds = self.primary_breeds.union(self.secondary_breeds)

        self.primary_breeds_probabilities = {"basic": 1, "arbitrageur": 0.5}
        self.secondary_breeds_probabilities = {"basic": 1, "herder": 0.5}

        self.sugarMap = pd.read_csv('sugar-map.txt', header = None, sep = ' ')
        for key in self.sugarMap:
            self.sugarMap[key] = self.sugarMap[key].add(1)
        self.rows, self.cols = self.sugarMap.shape
        self.initializePatches()
        self.initializeAgents()
        self.data_dict = shelve.open("shelves\\masterShelve", writeback = True)
        for attribute in self.attributes:
            self.data_dict[attribute] = shelve.open("shelves\\subshelve-"+attribute, writeback = True) 

        self.transaction_prices = {good: [] for good in self.goods}
        self.all_prices = []
        self.water_avg_price = 1
        self.sugar_avg_price = 1
        self.total_avg_price = 1
        self.total_exchanges = 0
        self.num_basicherders = 0
        self.num_basicsbasics = 0 
        self.num_arbitrageursbasics = 0
        self.num_arbitrageursherders = 0
        self.population = len(self.agent_dict)

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
            agent = BasicAgent(self, row, col, ID)
            self.agent_dict[ID] = agent
            self.patches_dict[row][col].agent = agent
        
    def chooseRandomEmptyPatch(self):
        row, col = self.empty_patches.random_key() 
        del self.empty_patches[row, col]
        return row, col
    

    def simulate_interactions(self): 
        #start = time.time()
        agent_list = list(self.agent_dict.values())
        self.growPatches()
        random.shuffle(agent_list)
        self.goods_data = {good: [] for good in self.goods}
        for agent in agent_list:
            alive = agent.check_alive()
            if alive: 
                agent.move()
                agent.harvest()
                agent.trade()
                agent.consume()
                self.agent_reproduce(agent)
                agent.update_params()
                # for good in self.goods_data: 
                #         self.goods_data[good].append(agent.goods[good])
            else: 
                if self.live_visual: 
                    self.GUI.canvas.delete(agent.image)
                continue
        self.population = len(self.agent_dict)
        self.water_avg_price = gmean(self.transaction_prices['water'])
        self.sugar_avg_price = gmean(self.transaction_prices['sugar'])
        self.total_avg_price = gmean(self.all_prices)
        # end = time.time()
        # diff = end-start
        # print(diff)
        if self.plots:
            self.plot_data_dict['runtime'].append(diff)
        # print("population: " + str(len(self.agent_dict)))

    #update plot data
    def update_plot_data(self, period): 
        self.plot_data_dict['periods'].append(period)
        self.plot_data_dict['population'].append(self.population)
        self.plot_data_dict['agents_created'].append(self.total_agents_created)
        self.plot_data_dict['total_exchanges'].append(self.total_exchanges)
        self.plot_data_dict['num_basicbasic'].append(self.num_basicsbasics)
        self.plot_data_dict['num_arbitrageurbasic'].append(self.num_arbitrageursbasics)
        self.plot_data_dict['num_basicherder'].append(self.num_basicherders)
        self.plot_data_dict['num_arbitrageurherder'].append(self.num_arbitrageursherders)

        if period > 0:
            self.water_avg_price = gmean(self.transaction_prices['water'])
            self.sugar_avg_price = gmean(self.transaction_prices['sugar'])
            self.total_avg_price = gmean(self.all_prices)
            self.plot_data_dict['average_water_price'].append(self.water_avg_price)
            self.plot_data_dict['average_sugar_price'].append(self.sugar_avg_price)
            self.plot_data_dict['all_prices'].append(self.total_avg_price)



    # choose what data to plot 
    def instatiate_plot_data(self): 
        self.plot_data_dict = {
            'periods': [],
            'population': [],
            'agents_created': [],
            'total_exchanges': [],
            'num_basicbasic': [],
            'num_arbitrageurbasic': [],
            'num_basicherder': [],
            'num_arbitrageurherder': [], 
            'average_water_price': [], 
            'average_sugar_price': [], 
            'all_prices': [], 
            'runtime':[]
        }

    def runModel(self, periods):
        if self.plots: 
            self.instatiate_plot_data()
            plt.ion()
            num_rows = int(np.ceil(np.sqrt(len(self.plot_data_dict)))) + 2
            num_cols = int(np.ceil(len(self.plot_data_dict) / num_rows)) 
            self.fig, self.axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20,20))

            
        # Update the plot at each period
        for period in range(1, periods + 1):
            # Simulate the agents interacting
            self.simulate_interactions()
            self.collectData(str(period))
            #print(period)

            # Update the data for the plots
            if self.plots: 
                self.update_plot_data(period)
                if period % self.GUI.every_t_frames_plots == 0:
                    self.plot_data(blit=True)

            if self.live_visual and period % self.GUI.every_t_frames_GUI == 0: 
                self.GUI.updatePatches()
                self.GUI.canvas.update()
            if period == periods:
                mem_usage = memory_usage(-1, interval=1)#, timeout=1)
                print(period, "end memory usage before sync//collect:", mem_usage[0], sep = "\t")
                self.data_dict.sync()
                gc.collect()
                mem_usage = memory_usage(-1, interval=1)#, timeout=1)
                print(period, "end memory usage after sync//collect:", mem_usage[0], sep = "\t")

                
        if self.plots:
            # Plot the final state of the data without blitting
            self.plot_data(blit=False)

    def plot_data(self, blit=False):
        if blit:
            # Clear the previous state of the plots
                self.fig.axes.clear()

        # Iterate over the data in the dictionary
        for i, (variable, data) in enumerate(self.plot_data_dict.items()):
            # Get the row and column for the current plot
            row = i // 2
            col = i % 2

            # Plot the data for the current variable
            self.axs[row, col].plot(self.plot_data_dict['periods'], data)
            self.axs[row, col].set_xlabel('Period')
            self.axs[row, col].set_ylabel(variable)

           

        # Redraw the plots
        self.fig.canvas.draw()

        if blit: 
            for ax in self.fig.axes: 
                self.fig.canvas.blit(ax.bbox)

                    
    # the reproduce funtion is implemented in model class to avoid circular dependencies in agent class 
    def agent_reproduce(self, agent): 
        if agent in self.agent_dict.values(): 
            can_reproduce = True
            for good in self.goods: 
                if getattr(agent, good) < agent.reproduction_criteria[good]: 
                    can_reproduce = False 
                    break
            
            if can_reproduce: 

                def child_breed(): 
                    # mutation means that agent switches breed 
                    def primary_breed(): 
                        if random.random() < agent.mutate_rate: 
                            breed = "basic" if agent.arbitrageur else "arbitrageur"
                        else: 
                            breed = "arbitrageur" if agent.arbitrageur else "basic"

                        return breed

                            
                    def secondary_breed():
                        if random.random() < agent.mutate_rate: 
                            breed = "basic" if agent.herder else "herder"
                        else: 
                            breed = "herder" if agent.herder else "basic"

                        return breed

                    return primary_breed(), secondary_breed()

                child_breed = child_breed()

                self.total_agents_created += 1
                row, col = self.chooseRandomEmptyPatch()  
                ID = self.total_agents_created
                
                if child_breed == ("basic", "basic"): 
                    self.num_basicsbasics += 1
                    self.agent_dict[ID] =  BasicAgent(model=self, row=row, col=col, ID=ID, parent=agent)
                elif child_breed == ("basic", "herder"): 
                    self.num_basicherders += 1
                    self.agent_dict[ID] =  BasicHerder(model=self, row=row, col=col, ID=ID, parent=agent)
                elif child_breed == ("arbitrageur", "basic"): 
                    self.num_arbitrageursbasics += 1
                    self.agent_dict[ID] =  Arbitrageur(model=self, row=row, col=col, ID=ID, parent=agent)
                elif child_breed == ("arbitrageur", "herder"):
                    self.num_arbitrageursherders += 1
                    self.agent_dict[ID] = ArbitrageurHerder(model=self, row=row, col=col, ID=ID, parent=agent)
                else: 
                    print("error")

                # add good quantities to new agent, deduct from parent
                # self.agent_dict[ID].goods = {}
                # for good in self.goods:
                #      agent.goods[good] -= agent.reproduction_criteria[good]
                #      self.agent_dict[ID].goods[good] = 0
                #      self.agent_dict[ID].goods[good] += agent.reproduction_criteria[good]
                self.agent_dict[ID].top_wealth = agent.get_wealth()
                self.agent_dict[ID].wealthiest = agent
                self.patches_dict[row][col].agent =  self.agent_dict[ID]
                if self.live_visual: 
                    self.GUI.draw_agent(self.agent_dict[ID])
                agent.reproduced = True

    
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
                
        collectAgentAttributes()
        collectModelAttributes()
