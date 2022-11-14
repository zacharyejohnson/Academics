import pandas as pd
import random
import math
from randomdict import RandomDict
from Patch import *
from BasicAgent import BasicAgent
from Herder import Herder
import numpy as np 
#Model.py
class Model():
    def __init__(self, gui, num_agents, mutate, genetic, live_visual, agent_attributes,
                 model_attributes):
        self.GUI = gui
        self.initial_population = num_agents
        self.mutate = mutate
        self.genetic = genetic
        self.model_attributes = model_attributes
        self.live_visual = live_visual

###################### MODEL PARAMETERS ##############################
        # goods to be included in model 
        self.goods = ["sugar", "water"]
        # initial distribution of wealth 
        self.init_good_ranges = {"min": 5, "max": 25}

        self.goods_params = {good:{"min":5,
                                   "max":25} for good in self.goods}
        # rates of good consumption 
        self.consumption_rate = {good : .1 for good in self.goods}
        # initial rates of demand 
        self.init_demand_vals = {"price": {"min": 0.5, "max": 2.0}, 
                                "quantity": {"min": 10, "max": 25}}
        self.total_agents_created = 0

        self.max_vision = 1

        self.max_mutate_rate = 0.5

        self.cross_over_rate = 0.5

        self.primary_breeds = {"basic"}
        self.secondary_breeds = {"herder"}
        self.breeds = self.primary_breeds.union(self.secondary_breeds)

        self.breed_probabilities = {"basic": 1, "herder": .50}

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
            del self.empty_patches[row, col]
            #all agents are initially basic 
            agent = BasicAgent(self, row, col, ID)
            self.agent_dict[ID] = agent
            self.patches_dict[row][col].agent = agent
        
    def chooseRandomEmptyPatch(self):
        i, j = self.empty_patches.random_key() 
        return i, j

    def runModel(self, periods):
        for period in range(1, periods + 1):
            agent_list = list(self.agent_dict.values())
            self.growPatches()
            random.shuffle(agent_list)
            for agent in agent_list:
                agent.update_params()
            for agent in agent_list:
                agent.move()
                agent.harvest()
                agent.consume()
                agent.trade()
                self.agent_reproduce(agent)
            if self.GUI.live_visual:
                if period % self.GUI.every_t_frames == 0:
                    self.GUI.updatePatches()
                    self.GUI.canvas.update()

    # the reproduce funtion is implemented in model class to avoid circular dependencies in agent class 
    def agent_reproduce(self, agent): 
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
            del self.empty_patches[row, col]
            ID = self.total_agents_created

            if child_breed == "basic": 
                self.agent_dict[ID] =  BasicAgent(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
            elif child_breed == "herder": 
                self.agent_dict[ID] =  Herder(row=row, col=col, ID=ID, hasParent = True,  **agent.copy_attributes)
            else: 
                print("error choosing child breed")
            
            # add good quantities to new agent, deduct from parent
            self.agent_dict[ID].goods = {}
            for good in agent.goods:
                agent.goods[good] -= agent.reproduction_criteria[good]
                self.agent_dict[ID].goods[good] = agent.reproduction_criteria[good]
            self.patches_dict[row][col].agent =  self.agent_dict[ID]
            self.GUI.draw_agent(self.agent_dict[ID])
            self.reproduced = True

    
    def growPatches(self):
        for row in self.patches_dict:
            for patch in self.patches_dict[row].values():
                if patch.Q < patch.maxQ:
                    patch.Q += 1