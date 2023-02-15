import copy
import gc
import os
import time
from tkinter import *

from DataAggregator import *
from memory_profiler import memory_usage

from Model import *


class GUI():
    def __init__(self, name, run, num_agents, live_visual, plots,
                 every_t_frames_GUI = 2, every_t_frames_plots=100, 
                 mutate = True, genetic = True, agent_attributes=None, 
                 model_attributes = None):
        if live_visual:
            self.parent = Tk()
        self.name = name
        self.run = run
        self.plots = plots
        self.model = Model(self, num_agents, mutate, genetic, live_visual, plots, agent_attributes, model_attributes)
        self.dimPatch = 16
        self.live_visual = live_visual
        self.every_t_frames_GUI = every_t_frames_GUI
        self.every_t_frames_plots = every_t_frames_plots

        if self.live_visual: 
            canvasWidth = self.model.cols * self.dimPatch
            canvasHeight= self.model.rows * self.dimPatch
            self.canvas = Canvas(self.parent, width=canvasWidth, height=canvasHeight, background="white")
            self.canvas.pack()
            self.drawPatches()
            self.drawAgents()
            self.canvas.update()
            
    def drawPatches(self):
        for i in self.model.patches_dict:
            for patch in self.model.patches_dict[i].values():    
                patch.image = self.canvas.create_rectangle(
                            #left x                     
 					patch.col * self.dimPatch,
                            #top y
 					patch.row * self.dimPatch,
                            #right x
 					(patch.col + 1) * self.dimPatch,
                            #bottom y
 					(patch.row + 1) * self.dimPatch,
 					fill=self.color(patch.Q - 1, patch.good),
 					width=0) #Border width = 0
                
    def drawAgent(self, agent):
        agent.image = self.canvas.create_oval(
 			agent.col * self.dimPatch + 2,
 			agent.row * self.dimPatch + 2,
 			(agent.col + 1) * self.dimPatch - 2,
 			(agent.row + 1)* self.dimPatch - 2,
 			fill='red',
 			width=0
		)

    def drawAgents(self):
        for agent in self.model.agent_dict.values(): 
            self.drawAgent(agent)

    def moveAgents(self):   
        for agent in self.model.agent_dict.values():
            self.canvas.move(agent.image, 
 			agent.dx * self.dimPatch,
 			agent.dy * self.dimPatch)
            color, outline = self.agentColor(agent)
            self.canvas.itemconfig(agent.image,
                                   fill = color,
                                   outline = outline, 
                                   width = 2)
    
    def agentColor(self, agent):
        if agent.basic:
            color = "red"
        if agent.arbitrageur:
            color = "green"
        outline = "black" if agent.herder else color
        return color, outline
    
    def updatePatches(self):
        for i in self.model.patches_dict:
            for patch in self.model.patches_dict[i].values():    
                self.canvas.itemconfig(patch.image, fill=self.color(patch.Q, 
                                                                    patch.good))
    def color(self, q, good):
        rgb = (255 - 3 * q,255 - 10 * q,255 - 51*q) if good == "sugar" else (30 - 3 * q, 50 - 5 * q ,255 - 35*q)
        color = '#'
        for v in rgb:
            hx = hex(v)[2:]
            while len(hx) < 2: 
                hx = '0' + hx
            color += hx
        return color

agent_attributes = []#"water", "sugar", "wealth", "basic",
                      #  "herder", "arbitrageur"]
model_attributes = ["population", "total_exchanges", "total_agents_created", "total_avg_price", "runtime", "water_avg_price", "sugar_avg_price",
                      #"num_basicherders", "num_arbitrageurherders", "num_basicbasics", "num_arbitrageurbasics", 
                               "bb_res_demand", "bh_res_demand", "ab_res_demand", "ah_res_demand"]


# parent = Tk()
# parent.title = "Sugarscape"
# name = "Sugarscape"
# run = 1
# num_agents = 2000
# periods = 1000
# y = GUI(name, run, num_agents, live_visual = False, plots = True,
#          every_t_frames_GUI = 5, every_t_frames_plots= 100,
#           agent_attributes=agent_attributes, model_attributes=model_attributes)
# y.model.runModel(periods)
# parent.quit()




runs = 5
data_agg = DataAggregator(agent_attributes, model_attributes)
for mutate in [True]:
    for genetic in [True]:#(True, False):
        name = "sugarscape" 
        data_agg.prepSetting()
        print("mutate", "genetic", sep = "\t")
        print(mutate, genetic, sep = "\t")
        print("trial", "agents", "periods", "time", sep = "\t")
        gc.set_threshold(0)
        for run in range(runs):
            mem_usage = memory_usage(-1, interval=1)#, timeout=1)
            print(run, "mem:", str(int(mem_usage[0]))  + " MB", sep = "\t")
            data_agg.prepRun(name, str(run))
            # parent.title"Sugarscape"
            num_agents = 2000
            periods = 10000
            start = time.time()
            y = GUI(name + str(run), run, num_agents, live_visual = False, plots = False, mutate = mutate, genetic = genetic,
                    agent_attributes = agent_attributes, 
                    model_attributes = model_attributes)
            y.model.runModel(periods)
            # print(dict(y.model.data_dict))
            data_agg.saveRun(name, str(run), y.model.data_dict)
            # run_data = copy.copy(y.model.data_dict)
            del y.model.data_dict
            # final_num_agents = len(y.model.agent_dict)
            if y.live_visual:
                y.parent.quit()
                y.parent.destroy()
            end = time.time()
            elapse = end - start
            print("runtime:", int(elapse), sep = "\t")

            # gc.collect()
            # del run_data
        data_agg.saveDistributionByPeriodWithParquet(name, runs)
        data_agg.plotDistributionByPeriod(name, runs)
        data_agg.remove_shelves()
        data_agg.remove_parquet()


# if __name__ == "__main__":
#     parent.mainloop()