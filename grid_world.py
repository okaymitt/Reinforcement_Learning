""" Grid world dimension 7x10. Origin (0,0) at upper left corner.
Start at (0,3) ; Goal at (3,7)
Cross-wind on y-axis accordind following scheme [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
Agent cannot fall over the edge, but keeps
"""

import tkinter as tk
from PIL import ImageTk, Image

PhotoImage = ImageTk.PhotoImage
UNIT = 75  # pixels
HEIGHT = 10  # grid height
WIDTH = 10  # grid width

class Gridworld():
    def __init__(self):
        self.dim_x = 7
        self.dim_y = 10
        self.wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

        self.start = (3, 0)
        self.goal =  (3, 7)

        self.pos_x = self.start[0]
        self.pos_y = self.start[1]


    def move(self, direction):
        self.pos_x += direction[0]
        self.pos_y += direction[1]

        self.pos_x -= self.wind[self.pos_y] 

        if self.pos_x < 0:
            self.pos_x = 0
        elif self.pos_x > self.dim_x -1:
            self.pos_x = self.dim_x -1
        elif self.pos_y < 0:
            self.pos_y = 0
        elif self.pos_y > self.dim_y -1:
            self.pos_y = self.dim_y -1

    








if __name__=="__main__":
    pass