from tkinter import *
from Model import *
from DataAggregator import *
from memory_profiler import memory_usage
import copy
import time
import os
import gc

class GUI():
    def __init__(self, name, run, num_agents, live_visual, plots, every_t_frames_GUI = 100, every_t_frames_plots=100, 
                 mutate = False, genetic = False, agent_attributes=None, 
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
 					patch.col * self.dimPatch,
 					patch.row * self.dimPatch,
 					(patch.col + 1) * self.dimPatch,
 					(patch.row + 1) * self.dimPatch,
 					fill=self.color(patch.Q - 1, patch.good),
 					width=0 
				)

    def drawAgents(self):
        for agent in self.model.agent_dict.values(): 
            agent.image = self.canvas.create_oval(
                agent.col * self.dimPatch + 2,
                agent.row * self.dimPatch + 2,
                (agent.col + 1) * self.dimPatch - 2,
                (agent.row + 1)* self.dimPatch - 2,
                fill='red',
                width=agent.outline_width
            )

    def draw_agent(self, agent): 
            agent.image = self.canvas.create_oval(
                    agent.col * self.dimPatch + 2,
                    agent.row * self.dimPatch + 2,
                    (agent.col + 1) * self.dimPatch - 2,
                    (agent.row + 1)* self.dimPatch - 2,
                    fill=agent.color,
                    width=agent.outline_width
                )

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

agent_attributes = ["transaction_prices", "wealth"]
model_attributes = ["population", "total_agents_created", "total_exchanges", "average_price"]

parent = Tk()
parent.title = "Sugarscape"
name = "Sugarscape"
run = 1
num_agents = 2000
periods = 10000
y = GUI(name, run, num_agents, live_visual = False, plots = True,
         every_t_frames_GUI = 1, every_t_frames_plots= 100,
          agent_attributes=agent_attributes, model_attributes=model_attributes)
y.model.runModel(periods)
parent.quit()


agent_attributes = ["transaction_prices", "wealth"]
model_attributes = ["population", "total_agents_created", "total_exchanges", "average_price"]


data_agg = DataAggregator(agent_attributes, model_attributes)
for mutate in [True]:
    for genetic in [True]:#(True, False):
        name = "mutate: " + str(mutate) + " genetic: " + str(genetic)
        data_agg.prepSetting(name)
        print("mutate", "genetic", sep = "\t")
        print(mutate, genetic, sep = "\t")
        print("trial", "agents", "periods", "time", sep = "\t")
        gc.set_threshold(0)
        for run in range(10):
            mem_usage = memory_usage(-1, interval=1)#, timeout=1)
            print(run, "mem:", str(int(mem_usage[0]))  + " MB", sep = "\t")
            data_agg.prepRun(name, str(run))
            # parent.title"Sugarscape"
            num_agents = 2000
            periods = 500
            start = time.time()
            y = GUI(name, run, num_agents, live_visual = False, plots=False, mutate = mutate, genetic = genetic,
                    agent_attributes = agent_attributes, 
                    model_attributes = model_attributes)
            y.model.runModel(periods)
            # print(dict(y.model.data_dict))
            data_agg.saveRun(name, str(run), y.model.data_dict)
            # run_data = copy.copy(y.model.data_dict)
            y.model.data_dict.close()
            # final_num_agents = len(y.model.agent_dict)
            if y.live_visual:
                y.parent.quit()
                y.parent.destroy()
            end = time.time()
            elapse = end - start
            print("runtime:", int(elapse), sep = "\t")

            # gc.collect()
            # del run_data
        data_agg.saveDistributionByPeriod(name)
        data_agg.plotDistributionByPeriod(name)
        data_agg.remove_shelves()


# if __name__ == "__main__":
#     parent.mainloop()