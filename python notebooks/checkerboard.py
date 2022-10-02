import tkinter as tk

SIZE = 30

board_length = 8
board_width = 8

root = tk.Tk()

canvas = tk.Canvas(root)
canvas.pack()

color = 'white'

for y in range(board_length):

    for x in range(board_width):
        x1 = x*SIZE
        y1 = y*SIZE
        x2 = x1 + SIZE
        y2 = y1 + SIZE
        canvas.create_rectangle((x1, y1, x2, y2), fill=color)
        if color == 'white':
            color = 'black'
        else:    
            color = 'white'

    if color == 'white':
        color = 'black'
    else:    
        color = 'white'

root.mainloop()        