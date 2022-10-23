import numpy as np 
import pandas as pd 

class Agent(): 
    def __init__(self, model, row, col, ID):  
        self.model = model
        self.row = row
        self.col = col
        self.ID = ID