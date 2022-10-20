import tkinter as tk 
from tkinter import *
import numpy as np 
import time
from colorama import Fore, Back, Style

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

        #end game once all agents in red or black set have been eliminated 
        while len(agents_dict[turn]) > 0:
            avaiable_agents = agents_dict[turn]
            skip = False
            moves_dict = {}
            # first, check for skips, and if there are skips the agent will always chose to skip
            for agent in avaiable_agents:
                agent_moves = agent.get_moves()
                if len(agent_moves) > 0: 
                        moves_dict[agent] = agent_moves
                # identify skips and execute
                skips = [ele for ele in agent_moves if ele in [(2, 2), (2, -2), (-2, 2), (-2, -2)]]
                if len(skips) > 0: 
                    skip = True
                    move = agent_moves[agent_moves.index(skips[0])]
                    #send skip to move funtion, which will execute multiple skips if avaliable
                    agent.move(move[0], move[1])
                    #break once move has been done
                    break

            if not skip: 
                agents = list (moves_dict.keys())
                if len(agents) > 0:
                    #choose random agent and move
                    rand_agent_ind = np.random.randint(0, len(agents))
                    agent = agents[rand_agent_ind]
                    rand_move_index = np.random.randint(0, len(moves_dict[agent]))
                    agent.move(moves_dict[agent][rand_move_index][0], moves_dict[agent][rand_move_index][1])
                    
            if turn == 'red': 
                turn = 'black'
            else: turn = 'red'

            print(f"{turn}'s turn")

            #pause between turns for a bit
            time.sleep(.4)

        # print out winner message once loop is done executing
        if turn == 'black': 
            print(Fore.RED + Style.BRIGHT + 'RED WINS!')
        else: 
            print(Fore.BLACK + Style.BRIGHT + 'BLACK WINS!')

        time.sleep(2)


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

    def checkers_agents(self): 
        startpos = 1
        # the checkers are best represented as a set
        agents_dict = {'red': set(), 'black': set()}

        for i in range(0,3):
                for j in range(startpos,self.rows,2):
                    agents_dict["red"].add(Agent(self, i, j, 'red'))

                if startpos == 0: 
                    startpos = 1
                else: 
                    startpos = 0

        for i in range(self.cols - 3, self.cols):
            for j in range(startpos,self.rows,2):
                agents_dict["black"].add(Agent(self, i, j, 'black'))
            
            if startpos == 0: 
                startpos = 1
            else: 
                startpos = 0

        return agents_dict

class Patch(): 
    def __init__(self, gui, row, col): 
        self.gui = gui
        self.row = row
        self.col = col
        self.agent = None
        self.color = self.gui.color_dict[self.set_color()]
    
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
        self.color = color
        self.king = False
        self.move_directions = {'red': [(1, 1), (1, -1)], 'black': [(-1, 1), (-1, -1)], 'king':[(1, 1), (1, -1), (-1, 1), (-1, -1)]}
        self.pdict = self.gui.patches_dict

# recursive moving: if a skip happens, check to see if more skips are avaliable and keep skipping until you can't
    def move(self, dX, dY):
        pdict = self.pdict
        self.patch = pdict[self.row][self.col]
        self.patch.agent = None
        #if the intended move is a skip, execute skip mechanics
        if (4 == np.abs(dY) + np.abs(dX)):
            row_0 = self.row 
            col_0 = self.col
            row_1 = self.row + dY
            col_1 = self.col + dX
            if(self.valid_move(dX, dY)):
                skip_patch = pdict[(row_0 + row_1) / 2][(col_0 + col_1) / 2]
                self.row += dY
                self.col += dX
                self.move_image(dX, dY)
                skipped_agent = skip_patch.agent
                if skipped_agent != None: 
                    skipped_agent.delete_image()
                    self.gui.agents_dict[skipped_agent.color].remove(skipped_agent)
                time.sleep(0.4)
                skip_patch.agent = None
                self.patch = pdict[self.row][self.col]
                self.patch.agent = self
                skips = [ele for ele in self.get_moves() if ele in [(2, 2), (2, -2), (-2, 2), (-2, -2)]]
                if len(skips) > 0:
                    rand_skip = np.random.randint(0, len(skips)) 
                    move = skips[rand_skip]
                    self.move(move[0], move[1])
                    time.sleep(.4)

        elif(2 == np.abs(dY) + np.abs(dX)): 
            self.row += dY
            self.col += dX
            self.move_image(dX, dY)

            self.patch = pdict[self.row][self.col]
            self.patch.agent = self

        # piece is a king if it reaches the end of the board
        if((self.row == 0 and self.color == 'black') or (self.row == self.gui.rows-1 and self.color == 'red')): 
            self.king = True
    
    def get_moves(self):
        move_directions = self.move_directions
        moves = []
        if self.king: 
            for dY, dX in move_directions['king']:
                if self.valid_move(dX, dY):  
                    moves.append((dX, dY))
                elif self.skippable(dX, dY):
                    moves.append((2*dX, 2*dY))

        else: 
            for dY, dX in move_directions[self.color]:
                if self.valid_move(dX, dY):  
                    moves.append((dX, dY))
                elif self.skippable(dX, dY):
                    moves.append((2*dX, 2*dY))
        print(moves)
        return moves
    
    def skippable(self, dX, dY): 
        if self.valid_patch(dX, dY):
            pdict = self.gui.patches_dict
            skip_patch = pdict[self.row + dY][self.col + dX]
            if self.valid_move(2*dX, 2*dY):
                landing_patch = pdict[self.row + 2*dY][self.col + 2*dX]
                if ((skip_patch.agent != None) and (skip_patch.agent.color != self.color) and (landing_patch.agent == None)):
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

    def move_image(self, dX, dY):
            self.gui.canvas.move(self.image, 
                                dX * self.gui.dimPatch,
                                dY * self.gui.dimPatch)
            self.gui.canvas.update()

    def delete_image(self): 
        self.gui.canvas.delete(self.image)
        self.gui.canvas.update()


    def valid_patch(self, dX, dY):
        if(self.row + dY >= 0 and self.row + dY < self.gui.rows) and (self.col + dX >= 0 and self.col + dX < self.gui.cols): 
            return True
        else: 
            return False

    def valid_move(self, dX, dY): 
        if(self.valid_patch(dX, dY) and self.gui.patches_dict[self.row + dY][self.col + dX].agent == None): 
            return True
            print("valid move identified")
        else: 
            return False

gui = Checkers("tk Checkers", 50, 8, 8)
gui.play()
