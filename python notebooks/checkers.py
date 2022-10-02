import tkinter as tk 
from tkinter import *
import numpy as np 
import time
from Patch import *
from Agent import *

class Checkers(): 
    def __init__(self, name, dimPatch, cols, rows):
        self.parent = Tk()
        self.name = name
        self.dimPatch = dimPatch
        self.cols = cols
        self.rows = rows
        self.color_dict = {0: "white", 1: "grey"}
        self.patches_dict = self.create_patches()
        canvasWidth = self.cols * self.dimPatch
        canvasHeight = self.rows * self.dimPatch

        self.canvas = Canvas(self.parent, width = canvasWidth, height = canvasHeight, background = "white", name = self.name)
        self.canvas.pack()

        self.agents_dict = self.checkers_agents()


        self.draw_patches()
        self.draw_agents(self.agents_dict)
        self.canvas.update()

    def play(self): 

        agents_dict = self.agents_dict
        turn = 'black' 
        while len(agents_dict[turn]) > 0:
            avaiable_agents = agents_dict[turn]
            skip = False
            # first, check for skips
            for agent in avaiable_agents:
                agent_moves = agent.get_moves()
                if len(agent_moves) > 0:
                    print(agent_moves)
                    skips = [ele for ele in agent_moves if ele in [(2, 2), (2, -2), (-2, 2), (-2, -2)]]
                    if len(skips) > 0: 
                        skip = True
                        move = agent_moves[agent_moves.index(skips[0])]
                        agent.move(move[0], move[1])
                        break

            if not skip: 
                for agent in avaiable_agents:
                    agent_moves = agent.get_moves()
                    if len(agent_moves) > 0:
                        agent.move(agent_moves[0][0], agent_moves[0][1])
                
            self.canvas.delete("all")
            self.draw_patches()
            self.draw_agents(self.agents_dict)
            self.canvas.update()

            if turn == 'red': 
                turn = 'black'
            else: turn = 'red'

            print(f"{turn}'s turn")

            time.sleep(.5)

    def draw_agents(self, agents_dict):
        for color in agents_dict.keys():
            for agent in agents_dict[color]: 
                agent.draw()
        print("agents drawn")

    def create_patches(self): 
        patches_dict = {}
        for i in range(self.rows): 
            patches_dict[i] = {}
            for j in range(self.cols):
                patches_dict[i][j] = Patch(self, i, j)
        return patches_dict
        print("patches created")

    def draw_patches(self): 
        patches_dict = self.patches_dict
        for row in patches_dict.keys(): 
            for col, patch in patches_dict[row].items(): 
                patch.image = self.canvas.create_rectangle(
                    col * self.dimPatch,
                    patch.row * self.dimPatch, 
                    (patch.col + 1) * self.dimPatch, 
                    (patch.row + 1) * self.dimPatch, 
                    fill = patch.color 
                )
        print("patches drawn")

    def checkers_agents(self): 
        startpos = 1
        agents_dict = {'red':[], 'black':[]}

        for i in range(0,3):
                for j in range(startpos,self.rows,2):
                    agents_dict["red"].append(Agent(self, i, j, 'red'))

                if startpos == 0: 
                    startpos = 1
                else: 
                    startpos = 0

        for i in range(self.cols - 3, self.cols):
            for j in range(startpos,self.rows,2):
                agents_dict["black"].append(Agent(self, i, j, 'black'))
            
            if startpos == 0: 
                startpos = 1
            else: 
                startpos = 0

        return agents_dict
        print("checkers created")

    
class Patch(): 
    def __init__(self, gui, row, col): 
        self.gui = gui
        self.row = row
        self.col = col
        self.agent = None
        self.color = self.gui.color_dict[self.set_color()]
        self.occupied = False
    
    def set_color(self):
        row, col = self.row, self.col
        row_remainder = row % 2
        col_remainder = col % 2
        total_remainder = row_remainder + col_remainder
        total_remainder = total_remainder % 2
        return total_remainder

class Agent(): 
    def __init__(self, gui, row, col, color): 
        self.gui = gui
        self.row = row
        self.col = col
        self.patch = self.gui.patches_dict[row][col]
        self.patch.agent = self
        self.patch.occupied = True
        self.color = color
        self.king = False
        self.move_directions = {'red': [(1, 1),(1, -1)], 'black': [(-1, 1), (-1, -1)] }

# recursive moving: if a skip happens, check to see if more skips are avaliable and keep skipping until you can't
    def move(self, dX, dY):
        self.patch.occupied = False
        if (2 == np.abs(dX)):
            self.skip(dX, dY)
            moves = self.get_moves()
            skips = [ele for ele in moves if ele in [(2, 2), (2, -2), (-2, 2), (-2, -2)]]
            if len(skips) > 0: 
                move = moves[moves.index(skips[0])]
                self.move(move[0], move[1])
            
        if(1 == np.abs(dX)): 
            self.row += dY
            self.col += dX
            self.gui.patches_dict[self.row][self.col].agent = self
            self.gui.patches_dict[self.row][self.col].occupied = True

        print("agent moved")

    def skip(self, dX, dY): 
        skipped_agent = self.gui.patches_dict[self.row+dY/2][self.col+dX/2].agent
        if skipped_agent in self.gui.agents_dict[skipped_agent.color]:
            self.gui.agents_dict[skipped_agent.color].remove(skipped_agent)
        self.gui.patches_dict[self.row+dY/2][self.col+dX/2].occupied = False
        self.row += dY
        self.col += dX
        self.gui.patches_dict[self.row][self.col].agent = self
        self.gui.patches_dict[self.row][self.col].occupied = True

    
    def get_moves(self):
        move_directions = self.move_directions
        moves = []
        for dX, dY in move_directions[self.color]:
            if self.valid_move(dX, dY):  
                    moves.append((dX, dY))
            elif self.skippable(dX, dY):
                moves.append((2*dX, 2*dY))
        print(moves)
        return moves
        
    
    def skippable(self, dX, dY): 
        patches_dict = self.gui.patches_dict
        if self.valid_patch(dX, dY):
            if (patches_dict[self.row + dY][self.col + dX].occupied == True and patches_dict[self.row + dY][self.col + dX].agent.color != self.color\
                and not patches_dict[self.row + 2*dY][self.col + 2*dX].occupied):
                return True
                print("skippable piece identified")
            else: 
                return False
        else:
             return False


    def draw(self): 
        self.image = self.gui.canvas.create_oval(self.col * self.gui.dimPatch, 
                                    self.row * self.gui.dimPatch, 
                                    (self.col + 1) * self.gui.dimPatch, 
                                    (self.row + 1) * self.gui.dimPatch, 
                                    fill = self.color, width = 0)

    # def move_diagonal(self):
    #     moves = self.get_moves()
    #     if(len(moves) > 0):
    #         move = moves[np.random.randint(0, len(moves))]
    #         self.move(move[0], move[1])

    def valid_patch(self, dX, dY):
        if(self.row + dY > 0 and self.row + dY < self.gui.rows - 1) and (self.col + dX > 0 and self.col + dX < self.gui.cols - 1): 
            return True
        else: 
            return False

    def valid_move(self, dX, dY): 
        if(self.valid_patch(dX, dY) and not self.gui.patches_dict[self.row + dY][self.col + dX].occupied): 
            return True
            print("valid move identified")
        else: 
            return False

          
gui = Checkers("tk Checkers", 50, 8, 8)
gui.play()
