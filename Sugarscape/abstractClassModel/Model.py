import copy
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
        self.live_visual = live_visual
        self.plots = plots
        if self.live_visual: 
            self.GUI = gui

###################### MODEL PARAMETERS ##############################
        # goods to be included in model 
        self.goods = ["sugar", "water"]
        # initial distribution of wealth 
        self.init_good_ranges = {"min": 5, "max": 25}

        self.goods_params = {good:{"min":5,
                                   "max":25} for good in self.goods}
        # rates of good consumption 
        self.consumption_rate = {good : 0.5 for good in self.goods}
        # initial rates of demand 
        self.init_demand_vals = {"price": {"min": 0.5, "max": 2.0}, 
                                "quantity": {"min": 10, "max": 25}}
        self.total_agents_created = 0

        self.max_vision = 1

        self.max_mutate_rate = 0.5

        self.cross_over_rate = 0.5

        self.primary_breeds = {"basic", "arbitrageur"}
        self.secondary_breeds = {"herder", "basic"}
        self.breeds = self.primary_breeds.union(self.secondary_breeds)

        self.primary_breeds_probabilities = {"basic": 1, "arbitrageur": 0.5}
        self.secondary_breeds_probabilities = {"basic": 1, "herder": 0.5}

        self.transaction_prices = {good:[] for good in self.goods}
        self.average_price = {good: np.nan for good in self.goods}
        self.total_exchanges = 0

        self.sugarMap = pd.read_csv('sugar-map.txt', header = None, sep = ' ')
        for key in self.sugarMap:
            self.sugarMap[key] = self.sugarMap[key].add(1)
        self.rows, self.cols = self.sugarMap.shape
        self.initializePatches()
        self.initializeAgents()

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

    def runModel(self, periods):
        population_data = []
        agents_created = []
        total_exchanges = []
        period_list = []
        
        for period in range(0, periods + 1):
            population_data.append(len(self.agent_dict))
            agents_created.append(self.total_agents_created)
            total_exchanges.append(self.total_exchanges)
            period_list.append(period)
            if self.plots and period % self.GUI.every_t_frames == 0:
                if period == 0: 
                    plt.ion()
                    fig, axs = plt.subplots(3, figsize = (15,5))
                    axs[0].plot(period_list, population_data)
                    axs[1].plot(period_list, agents_created)
                    axs[2].plot(period_list, total_exchanges)
                    # ax.plot(period_list, self.total_agents_created)
                else: 
                    # line2.set_ydata(self.total_agents_created)
                    axs[0].plot(period_list, population_data)
                    axs[1].plot(period_list, agents_created)
                    axs[2].plot(period_list, total_exchanges)
                    plt.draw()
                    plt.pause(0.0001)
                    
                

                

            start = time.time()
            agent_list = list(self.agent_dict.values())
            self.growPatches()
            random.shuffle(agent_list)
            for agent in agent_list:
            #     agent.update_params()
            # for agent in agent_list:
                alive = agent.check_alive()
                if alive: 
                    agent.move()
                    agent.harvest()
                    agent.trade()
                    agent.consume()
                    self.agent_reproduce(agent)
                    agent.update_params()
                else: 
                    if self.live_visual: 
                        self.GUI.canvas.delete(agent.image)
                    continue
            if self.live_visual:
                if period % self.GUI.every_t_frames == 0:
                    self.GUI.updatePatches()
                    self.GUI.canvas.update()


            end = time.time()
            diff = end-start
            print(diff)
            print("population: " + str(len(self.agent_dict)))
                    

    # the reproduce funtion is implemented in model class to avoid circular dependencies in agent class 
    def agent_reproduce(self, agent): 
        if agent in self.agent_dict.values(): 
            can_reproduce = True
            for good in agent.goods: 
                if agent.goods[good] < agent.reproduction_criteria[good]: 
                    can_reproduce = False 
                    break
            
            if can_reproduce: 

                def child_breed(): 
                    primary_breed = random.choices(list(self.primary_breeds_probabilities.keys()), 
                                            weights=list(self.primary_breeds_probabilities.values()), k=1)[0]
                    secondary_breed = random.choices(list(self.secondary_breeds_probabilities.keys()), 
                                            weights=list(self.secondary_breeds_probabilities.values()), k=1)[0]
                    return primary_breed, secondary_breed

                child_breed = child_breed()

                self.total_agents_created += 1
                row, col = self.chooseRandomEmptyPatch()  
                ID = self.total_agents_created
                
                if child_breed == ("basic", "basic"): 
                    self.agent_dict[ID] =  BasicAgent(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
                elif child_breed == ("basic", "herder"): 
                    self.agent_dict[ID] =  BasicHerder(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
                elif child_breed == ("arbitrageur", "basic"): 
                    self.agent_dict[ID] =  Arbitrageur(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
                elif child_breed == ("arbitrageur", "herder"):
                    self.agent_dict[ID] = ArbitrageurHerder(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
                else: 
                    print("error")
                    

                # add good quantities to new agent, deduct from parent
                self.agent_dict[ID].goods = {}
                for good in self.goods:
                    agent.goods[good] -= agent.reproduction_criteria[good]
                    self.agent_dict[ID].goods[good] = 0
                    self.agent_dict[ID].goods[good] += agent.reproduction_criteria[good]
                self.patches_dict[row][col].agent =  self.agent_dict[ID]
                if self.live_visual: 
                    self.GUI.draw_agent(self.agent_dict[ID])
                agent.reproduced = True

    
    def growPatches(self):
        for row in self.patches_dict:
            for patch in self.patches_dict[row].values():
                if patch.Q < patch.maxQ:
                    patch.Q += 1