import pandas as pd
import random
import math
from randomdict import RandomDict

from Patch import *
from Agent import *
#Model.py
class Model():
    def __init__(self, gui, num_agents):
        self.GUI = gui
        self.initial_population = num_agents

###################### MODEL PARAMETERS ##############################
        self.goods = ["sugar"]
        self.consumption_rate = {"sugar": .5}
        self.total_agents_created = 0

        self.max_vision = 1
        self.move_dict = {
            v:{
                i:{
                    j: True for j in range(-v, v + 1) if (i ** 2 + j ** 2) <= (v ** 2) }
                for i in range(-v, v + 1)}
            for v in range(1, self.max_vision + 1)}

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
                good = "sugar"
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
            self.agent_dict[ID] = Agent(self, row, col, ID)
        
    def chooseRandomEmptyPatch(self):
        i, j = self.empty_patches.random_key() 
        return i, j

    def runModel(self, periods):
        agent_list = list(self.agent_dict.values())
        for period in range(1, periods + 1):
            self.growPatches()
            random.shuffle(agent_list)
            for agent in agent_list:
                agent.move()
            if self.GUI.live_visual:
                if period % self.GUI.every_t_frames == 0:
                    self.GUI.updatePatches()
                    #self.GUI.moveAgents()
                    #self.GUI.canvas.update()
                
    def agentMove(self, agent): 
        pass

    def findMaxEmptyPatch(self, agent, curr_i, curr_j):
        pass

    def moveToMaxEmptyPatch(self, agent, curr_i, curr_j):
        pass
    
    def agentHarvest(self, agent):    
        pass
    
    def growPatches(self):
        for row in self.patches_dict:
            for patch in self.patches_dict[row].values():
                if patch.Q < patch.maxQ:
                    patch.Q += 1