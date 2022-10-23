from tkinter import * 
import pandas as pd
import numpy as np 


class GUI(): 
    def __init__(self, parent, num_agents): 
        self.parent = parent 
        self.initial_population = num_agents

        