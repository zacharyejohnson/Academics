import copy
import time
import pandas as pd
import random
import math
from randomdict import RandomDict
from Patch import *
from BasicAgent import BasicAgent
from Herder import Herder
from Arbitrageur import Arbitrageur
import numpy as np 
#Model.py
class Model():
    def __init__(self, gui, num_agents, mutate, genetic, live_visual, agent_attributes,
                 model_attributes):
        
        self.initial_population = num_agents
        self.mutate = mutate
        self.genetic = genetic
        self.model_attributes = model_attributes
        self.live_visual = live_visual
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
        self.consumption_rate = {good : .5 for good in self.goods}
        # initial rates of demand 
        self.init_demand_vals = {"price": {"min": 0.5, "max": 2.0}, 
                                "quantity": {"min": 10, "max": 25}}
        self.total_agents_created = 0

        self.max_vision = 1

        self.max_mutate_rate = 0.5

        self.cross_over_rate = 0.5

        self.primary_breeds = {"basic", "arbitrageur"}
        self.secondary_breeds = {"herder"}
        self.breeds = self.primary_breeds.union(self.secondary_breeds)

        self.breed_probabilities = {"basic": 1, "herder": .50, "arbitrageur": .50}

        self.transaction_prices = []
        self.average_price = np.nan
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
        
        for period in range(1, periods + 1):
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
                    breed = random.choices(list(self.breed_probabilities.keys()), 
                                            weights=list(self.breed_probabilities.values()), k=1)
                    return breed[0]

                child_breed = child_breed()

                self.total_agents_created += 1
                row, col = self.chooseRandomEmptyPatch()  
                ID = self.total_agents_created

                if child_breed == "basic": 
                    self.agent_dict[ID] =  BasicAgent(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
                elif child_breed == "herder": 
                    self.agent_dict[ID] =  Herder(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
                elif child_breed == "arbitrageur": 
                    self.agent_dict[ID] =  Arbitrageur(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
                else: 
                    print("error choosing child breed")

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