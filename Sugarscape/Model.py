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
import numbers 
import plotly.graph_objects as go

class Model:
    def __init__(self, gui, num_agents, mutate, genetic, live_visual, plots, agent_attributes,
                 model_attributes, primary_breeds):
        """
        Initializes the model for the Sugarscape simulation.

        Args:
            gui: Reference to the GUI object for visual representation.
            num_agents (int): The initial number of agents in the simulation.
            mutate (bool): Flag indicating if agents can mutate.
            genetic (bool): Flag indicating if genetic algorithms are used.
            live_visual (bool): Flag for enabling live visualization.
            plots (bool): Flag for enabling plotting of results.
            agent_attributes (list): List of attributes to track for each agent.
            model_attributes (list): List of attributes to track for the model.
            primary_breeds (list): List of primary breeds in the simulation.
        """

        # Basic model parameters
        self.initial_population = num_agents
        self.mutate = mutate
        self.genetic = genetic
        self.live_visual = live_visual
        self.plots = plots
        self.GUI = gui

        # Attributes and breeds setup
        self.model_attributes = model_attributes
        self.agent_attributes = agent_attributes
        self.attributes = agent_attributes + model_attributes
        self.primary_breeds = primary_breeds
        self.secondary_breeds = ["herder"]
        self.breeds = self.primary_breeds + self.secondary_breeds

        # goods to be included in model 
        self.goods = ["sugar", "water"]

        # initial distribution of wealth 
        self.init_good_ranges = {"min": 10, "max": 25}

        # initial ranges for basic res ratios
        self.init_res_ratio_ranges = {"min": 0.5, "max": 2}

        # initial bounds for goods endowment for first generation of agents 
        self.goods_params = {good:{"min":10,
                                   "max":25} for good in self.goods}

        # rates of good consumption 
        self.consumption_rate = {"water" : 1.5, 
                                 "sugar": 1.5}

        # initial range of reproduction ratio
        self.init_reproduction_ratio_ranges = {good: {"min": 1.2, 
                                                      "max": 5} for good in self.goods}
        
        # tracker for total agents created
        self.total_agents_created = 0

        # maximum allowable agent vision (set at 1 for this project)
        self.max_vision = 1

        # maximum allowable mutate rate for an agent
        self.max_mutate_rate = 0.5

        # herding crossover rate
        self.cross_over_rate = 0.5

        # attributes not to be included in inheritance
        self.drop_attr = ["col", "row", "dx", "dy", "id", "wealth", "top_wealth",
             "sugar", "water", "vision", "model", "parent", "MRS", "wealth_by_good",
               "initial_goods", "wealthiest", "reproduction_criteria", 
               "period_savings", "period_consumption", "period_income", "num_alive_children"]
        
        # map representing vision of agents on the Sugarscape
        self.nav_dict = {
            v:{
                i:{
                    j: True for j in range(-v, v + 1) if 0 < (i ** 2 + j ** 2) <= (v ** 2)}
                for i in range(-v, v + 1)}
            for v in range(1, self.max_vision + 1)}

        # initialization of model environment - growing the Sugarscape
        self.sugarMap = pd.read_csv('sugar-map.txt', header = None, sep = ' ')
        for key in self.sugarMap:
            self.sugarMap[key] = self.sugarMap[key].add(1)

        # number of rows, cols
        self.rows, self.cols = self.sugarMap.shape

        # populate the sugarscape with patches (goods) and agents
        self.initializePatches()
        self.initializeAgents()

        # create data dict to store data for each run - reinitialized every run
        self.data_dict = {}#shelve.open("shelves\\masterShelve", writeback = True)
        for attribute in self.attributes:
            self.data_dict[attribute] = {}#shelve.open("shelves\\subshelve-"+attribute, writeback = True) 


        # initialization of variables used for tracking model attributes
        self.transaction_prices = {good: [1] for good in self.goods}
        self.transaction_weights = {good: [1] for good in self.goods}
        self.all_prices = [1]
        self.all_prices_weights = [1]
        self.water_avg_price = 1
        self.sugar_avg_price = 1
        self.total_avg_price = 1
        self.total_exchanges = 0
        self.price_variance = 0
        self.preference_variance = 0 
        self.population = len(self.agent_dict) 
        self.optimizer_MRS = 1 
        self.agent_wealth = 0
        self.runtime = 0
        self.avg_mutation_rate = 0
        self.real_income_per_capital = 0
        self.income=0
        self.savings=0
        self.basic_wealth_per_capita = 0 
        self.optimizer_wealth_per_capita = 0 
        self.mutate_rate = 0
        self.price_change = 0 
        self.reservation_ratio = 1
        self.basic_mutatable_vars = ["reproduction_criteria", "reproduction_ratio"]
        

    def initializePatches(self):
        """
        Initializes the patches in the simulation grid.
        """
        self.patches_dict = {i: {j: 0 for j in range(self.cols)} for i in range(self.rows)}
        for i in range(self.rows):
            for j in range(self.cols):
                good = "sugar" if i + j < self.cols else "water"
                self.patches_dict[i][j] = Patch(self, i, j, self.sugarMap[i][j], good)

        self.empty_patches = RandomDict({
            (i, j): self.patches_dict[i][j]
            for i in range(self.rows) for j in range(self.cols)
        })

    def initializeAgents(self):
        """
        Initializes agents and places them randomly on empty patches.
        """
        self.agent_dict = {}
        for i in range(self.initial_population):
            self.total_agents_created += 1
            ID = self.total_agents_created
            row, col = self.chooseRandomEmptyPatch()
            agent = Agent(self, row, col, ID)
            self.agent_dict[ID] = agent
            self.patches_dict[row][col].agent = agent

    def chooseRandomEmptyPatch(self):
        """
        Selects a random empty patch from the grid.

        Returns:
            Tuple (row, col): Coordinates of the chosen empty patch.
        """
        row, col = self.empty_patches.random_key()
        del self.empty_patches[row, col]
        return row, col

    def chooseNearestEmptyPatch(self, agent):
        """
        Chooses the nearest empty patch to the given agent.

        Args:
            agent (Agent): The agent for which to find the nearest empty patch.

        Returns:
            Tuple (row, col): Coordinates of the nearest empty patch, or (None, None) if none found.
        """
        row, col = agent.row, agent.col
        neighbor_patches = [
            (agent.row + i, agent.col + j)
            for i in self.nav_dict[1] if 0 <= row + i < 50
            for j in self.nav_dict[1][i] if 0 <= col + j < 50
        ]

        if len(neighbor_patches) > 0:
            choice = random.choice(neighbor_patches)
            del self.empty_patches[choice]
            return choice
        else:
            return None, None



    def simulate_interactions(self, period): 
        agent_list = list(self.agent_dict.values())
        random.shuffle(agent_list)
        if self.model_attributes != []: # and self.plots: 
            self.num_herders = 0
            self.num_optimizers = 0 
            self.num_basics = 0
            self.num_wealth_herders = 0 
            self.num_progenycount_herders = 0 

            self.all_prices = []
     
            self.mutate_rate_list = []
            self.price_change_list = []
            self.reservation_ratio_list = []
            for attr in self.basic_mutatable_vars: 
                # if not isinstance(getattr(agent_list[0], attr), dict):
                #         setattr(self, attr + "_list", [])
                # else: 
                    for key in getattr(agent_list[0], attr).keys(): 
                        setattr(self, attr + "_" +  key + "_list", [])

        self.agent_wealth = 0
        self.consumption = 0
        self.savings = 0 
        self.income = 0 
        self.basic_wealth = 0 
        self.optimizer_wealth = 0 
        self.herder_wealth_per_capita = 0 
        self.wealth_herder_wealth_per_capita = 0 
        self.progenycount_herder_wealth_per_capita = 0 
        
        for agent in agent_list:
                    
                    temp_wealth = 0 
                    temp_wealth += agent.wealth

                    agent.move()
                    agent.harvest()
                    agent.trade()
                    agent.consume()
                    agent.check_alive()
                    agent.reproduce()
                    agent.updateParams()

                    if agent.id in self.agent_dict.keys(): 
                        agent.period_savings = agent.wealth - temp_wealth
                        agent.period_income = agent.period_consumption + agent.period_savings

                # #agent statistics tracking 
                    if self.model_attributes != []: 
                        if agent.herder: 
                            self.num_herders += 1
                            self.herder_wealth_per_capita += agent.wealth
                            if agent.herding_metric == "wealth": 
                                self.num_wealth_herders += 1
                                self.wealth_herder_wealth_per_capita += agent.wealth
                            else: 
                                self.num_progenycount_herders += 1
                                self.progenycount_herder_wealth_per_capita += agent.wealth

                        if agent.basic: 
                            self.basic_wealth += agent.wealth
                            self.num_basics += 1
                            
                        if agent.optimizer: 
                            self.optimizer_wealth += agent.wealth
                            self.num_optimizers += 1
                        self.reservation_ratio_list.append(agent.reservation_ratio)
                        self.mutate_rate_list.append(agent.mutate_rate)
                        self.price_change_list.append(agent.price_change)
                        for attr in self.basic_mutatable_vars:
                            #if hasattr(agent, attr): 
                                # if not isinstance(getattr(agent, attr), dict): 
                                #     getattr(self, attr+"_list").append(getattr(agent, attr))
                                # else: 
                                    for key in getattr(agent, attr).keys(): 
                                        getattr(self, attr + "_" + key + "_list").append(getattr(agent, attr)[key])

        for agent in self.agent_dict.values():
            self.agent_wealth += agent.wealth
            self.consumption += agent.period_consumption
            self.savings += agent.period_savings 
            self.income += agent.period_income 

        if self.model_attributes != []: # and self.plots:
            #print(self.reservation_ratio_list)
            #self.reservation_ratio = gmean(self.reservation_ratio_list)
            for attr in ["reservation_ratio", "mutate_rate", "price_change", "reproduction_ratio", "reproduction_criteria"]: 
                    
                    if not isinstance(getattr(agent, attr), dict): 
                        #if period == 1:
                            #print(attr + "\n\n\n" , getattr(self, attr+"_list"))
                        if attr in ["reservation_ratio", "price_change"]: 
                            setattr(self, attr, gmean(getattr(self, attr+"_list")))
                        else: 
                            if len(getattr(self, attr+"_list")) > 0: 
                                setattr(self, attr, np.average(getattr(self, attr+"_list")))
                    else: 
                        for key in getattr(agent, attr).keys(): 
                            if len(getattr(self, attr+"_"+key+"_list")) > 0: 
                                setattr(self, attr + "_" + key, np.average(getattr(self, attr+"_"+key+"_list")))

            self.preference_variance = np.std(self.reservation_ratio_list)

    def runModel(self, periods):           
        # Update the plot at each period
        for period in range(1, periods + 1):
            
            self.cw = self.consumption_rate["water"]
            self.cs = self.consumption_rate["sugar"]
            # Simulate the agents interacting
            start1 = time.time()
            self.growPatches()
            setattr(self, "population", len(self.agent_dict))
            if self.population == 0:
                 break 

            self.simulate_interactions(period)
            
            setattr(self, "wealth_per_capita", self.agent_wealth / self.population)

            setattr(self, "real_income_per_capital", self.income / self.population)

            if self.num_wealth_herders > 0: 

                self.wealth_herder_wealth_per_capita /= self.num_wealth_herders

            if self.num_progenycount_herders > 0: 

                self.progenycount_herder_wealth_per_capita /= self.num_progenycount_herders

            if self.num_basics > 0: 
                setattr(self, "basic_wealth_per_capita", getattr(self, "basic_wealth") / self.num_basics)
            if self.num_optimizers > 0: 
                setattr(self, "optimizer_wealth_per_capita", getattr(self, "optimizer_wealth") / self.num_optimizers)
            if self.num_herders > 0: 
                self.herder_wealth_per_capita /= self.num_herders

            if period > 1: 
               
                if len(self.all_prices) > 0: 
                    avg_total = gmean(self.all_prices)
                    setattr(self, "price_variance", np.std(self.all_prices))
                else: 
                    avg_total = 1

                    self.price_variance = 0 
              
                setattr(self, "total_avg_price", avg_total)

            if period == 1:
                print("mutate rate: " + str(self.mutate_rate))
                print("reservation_ratio: " + str(self.reservation_ratio))
                
            end1 = time.time()
            self.runtime = end1-start1
            self.GUI.data_agg.collectData(self, self.GUI.run, period)
            self.collectData(period)
            
            
            if period % 1000 == 0: 
                print(period, self.runtime)
                gc.collect()

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

        num_rows = int((len(self.data_dict) / 2))
        num_cols = 2
        fig = go.Figure()


        # Iterate over the data in the dictionary
        j = 0 
        for i, (variable, data) in enumerate(self.data_dict.items()):
            
            # if "num" in variable: 
            #     #plot proportions of each agent over time in final plot 
            #     self.axs[num_rows - 1, 1].plot(np.array(list(data.values())) / np.array(list(self.data_dict["population"].values())), label = variable[4:]) # get rid of "num_"
            #     self.axs[num_rows - 1, 1].set_ylabel("Population\nShare")
            #     self.axs[num_rows - 1, 1].legend(fontsize=5, loc=4)
            #     j += 1
            # elif "_price" in variable and "hueristic" not in variable:
            #     self.axs[num_rows - 1, 0].plot(data.values(), label = variable[:9], linewidth=0.1) # get rid of "_avg_price"... etc 
            #     self.axs[num_rows - 1, 0].set_ylabel("Prices")
            #     self.axs[num_rows - 1, 0].legend(fontsize=7, loc=2)
                
                
            # elif "res_demand" in variable:
            #     self.axs[num_rows - 2, 1].plot(data.values(), label = variable)
            #     self.axs[num_rows - 2, 1].set_ylabel("Reservation\nDemands")
            #     self.axs[num_rows - 2, 1].legend(fontsize=7, loc=2)
            #     j += 1

            # else: 
            
            fig.add_trace(
                go.Scatter(x = list(self.data_dict["total_exchanges"]),
                           y = list(data.values()),
                           name = variable,
                           visible = False,
                           line = dict(color="black")
                )
            )

        buttons = [{"label": variable, "method": "update", "args": [{"visible": [key == variable for key in self.data_dict.keys()]},
                                                           {"title": variable, "annotations": []}]}
           for variable in self.data_dict.keys()]

        fig.update_layout(
            updatemenus=[
                dict(
                    active=0, 
                    buttons = buttons)
                    

            ]
        )

        fig.update_layout(title_text = "Plots")
        fig.show()

                # Get the row and column for the current plot
                # row = (i-j) // 2
                # col = (i-j) % 2
                # #print(variable)
                # # Plot the data for the current variable
                # self.axs[row, col].plot(data.values())
                # self.axs[row, col].set_xlabel('Period')
                # self.axs[row, col].set_ylabel(variable.replace("_", "\n"))
            

        # Redraw the plots
        # self.fig.canvas.draw()
        # plt.show()

    
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
