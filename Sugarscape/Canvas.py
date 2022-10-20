from tkinter import *
import pandas as pd


sugarmap = pd.read_csv('sugar-map.txt', header = None, sep = ' ')
parent = Tk()
canvas = Canvas(parent)
canvas.pack()
print(sugarmap)