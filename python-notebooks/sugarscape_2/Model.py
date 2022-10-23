import pandas as pd 
import numpy as np 


class Model(): 
   def __init__(self, gui, num_agents):
        self.GUI = gui
        self.initial_population = num_agents
        self.total_agents_created = 0
        