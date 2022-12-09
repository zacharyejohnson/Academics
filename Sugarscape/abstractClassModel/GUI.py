from tkinter import *
from Model import *
import time
from matplotlib import pyplot as plt
class GUI():
    def __init__(self, parent, num_agents, live_visual, plots, every_t_frames, mutate = True, genetic = True, agent_attributes=None, 
                 model_attributes = None):
        self.parent = parent
        self.plots = plots
        self.model = Model(self, num_agents, mutate, genetic, live_visual, plots, agent_attributes, model_attributes)
        self.dimPatch = 16
        self.live_visual = live_visual
        self.every_t_frames = every_t_frames

        

        canvasWidth = self.model.cols * self.dimPatch
        canvasHeight= self.model.rows * self.dimPatch
        self.canvas = Canvas(parent, width=canvasWidth, height=canvasHeight, background="white")
        self.canvas.pack()
        if self.live_visual:
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


parent = Tk()
parent.title = "Sugarscape"
num_agents = 750
periods = 10000
y = GUI(parent, num_agents, live_visual = True, plots = True, every_t_frames = 100)
y.model.runModel(periods)
parent.quit()




if __name__ == "__main__":
    parent.mainloop()