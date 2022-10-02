class Patch(): 
    def __init__(self, gui, row, col): 
        self.gui = gui
        self.row = row
        self.col = col
        self.color = self.gui.color_dict[self.set_color()] 
    

    def set_color(self):
        row, col = self.row, self.col
        row_remainder = row % 2
        col_remainder = col % 2
        total_remainder = row_remainder + col_remainder
        total_remainder = total_remainder % 2
        return total_remainder