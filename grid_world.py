""" Grid world dimension 7x10. Origin (0,0) at upper left corner.
Start at (0,3) ; Goal at (3,7)
Cross-wind on y-axis accordind following scheme [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
Agent cannot fall over the edge, but keeps
"""

import tkinter as tk
from PIL import ImageTk, Image
import time

PhotoImage = ImageTk.PhotoImage
UNIT = 75  # pixels
# HEIGHT = 10  # grid height
# WIDTH = 10  # grid width

class Gridworld(tk.Tk):
    def __init__(self, move='cross', modus='auto'):
        super(Gridworld, self).__init__()

        # set world
        self.dim_x = 10
        self.dim_y = 7
        self.wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
        
        self.start = (0,3)
        self.goal_coords =  (7, 3)

        self.pos_x = self.start[0]
        self.pos_y = self.start[1]

        self.set_action_space(move)
        self.observation_size = (self.dim_x, self.dim_y)


        # set canvas
        self.title('Windy grid world')
        self.geometry('{0}x{1}'.format(UNIT * self.dim_x, UNIT * self.dim_y))
        self.shapes = self._load_images()
        self.canvas = self._build_canvas()

        self.counter = 0
        self.rewards = []
        self.goal = []

        # set rewards
        for x in range(self.dim_x):
            for y in range(self.dim_y):
                state = (x, y)
                if state != self.goal_coords:
                    self.set_reward(state, -1)
                else:
                    self.set_reward(state, 10)

        # move agent with arrow keys, if modus is manual
        if modus == 'manual':
            self.bindings()


    
    def set_action_space(self, move):
        if move == 'cross':
            self.action_space = ['u', 'd', 'l', 'r']
        elif move == 'king':
            self.action_space = ['u', 'd', 'l', 'r',
                                'ul', 'ur', 'dl', 'dr']

        self.action_size = len(self.action_space)

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           width=self.dim_x * UNIT,
                           height=self.dim_y * UNIT)
        # create grids
        for c in range(0, self.dim_x * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = c, 0, c, self.dim_y * UNIT
            canvas.create_line(x0, y0, x1, y1, fill='black')
        for r in range(0, self.dim_y * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = 0, r, self.dim_x * UNIT, r
            line = canvas.create_line(x0, y0, x1, y1, fill='black')

        self.rewards = []
        self.goal = []
        # add image to canvas
        x, y =  UNIT/2 + self.start[0]*UNIT , UNIT/2 + self.start[1]*UNIT
        self.rectangle = canvas.create_image(x, y, image=self.shapes[0])

        # pack all`
        canvas.pack()

        return canvas

    def _load_images(self):
        path = "ch5_windy_gridworld/img/"
        rectangle = PhotoImage(
            Image.open(path + "rectangle.png").resize((40, 40)))
        triangle = PhotoImage(
            Image.open(path + "triangle.png").resize((40, 40)))
        circle = PhotoImage(
            Image.open(path + "circle.png").resize((40, 40)))

        return rectangle, triangle, circle

    def set_reward(self, state, reward):
        x, y = state
        temp = {}

        temp['rewad'] = reward

        if reward > 0:
            print(x, y)
            temp['figure'] = self.canvas.create_image( UNIT / 2 + UNIT * x,
                                                       UNIT / 2 + UNIT * y,
                                                       image=self.shapes[2])
            self.canvas.tag_raise(temp['figure'])
            self.goal.append(temp['figure'])
            temp['coords'] = self.canvas.coords(temp['figure'])
            
        elif reward < 0:
            temp['figure'] = None
            temp['coords'] = ((UNIT * x) + UNIT / 2, (UNIT * y) + UNIT / 2)

        temp['state'] = state
        self.rewards.append(temp)

    def move(self, agent,  direction):
        move_x = direction[0]
        move_y = direction[1] - self.wind[self.pos_x]

        new_pos_x = self.pos_x + direction[0]
        new_pos_y = self.pos_y + direction[1] - self.wind[self.pos_x]       

        if new_pos_x < 0:
            new_pos_x = 0
        elif new_pos_x > self.dim_x -1:
            new_pos_x = self.dim_x -1    

        if new_pos_y  < 0:
            new_pos_y  = 0
        elif new_pos_y  > self.dim_y -1:
            new_pos_y = self.dim_y -1

        move_x = new_pos_x - self.pos_x
        move_y = new_pos_y - self.pos_y

        self._move_agent(move_x, move_y)

        self.pos_x = new_pos_x
        self.pos_y = new_pos_y



    def _move_agent(self, move_x, move_y):
        """ This function renders agent move on canvas"""
        move_x *= UNIT
        move_y *= UNIT
        
        self.canvas.move(self.rectangle, move_x, move_y)
        self.render()


    def coords_to_state(self):
        pass

    def state_to_coords(self):
        pass

    def step(self, action_idx):
        self.counter += 1
        direction = self.get_direction(action_idx)
        next_coords = self.move(self.rectangle, direction)

    def get_direction(self, action_idx):
        action = self.action_space[action_idx]

        if action == 'u':
            direction = (0,-1)
        elif action == 'ur':
            direction = (1, -1)
        elif action == 'r':
            direction = (1,0)
        elif action == 'dr':
            direction = (1,1)
        elif action == 'd':
            direction = (0, 1)
        elif action == 'dl':
            direction = (-1, 1)
        elif action == 'l':
            direction = (-1, 0)
        elif action == 'ul':
            direction = (-1, 1)

        return direction 

    def render(self):
        #time.sleep(0.07)
        self.update()

    def reset(self):
        pass

     
    def bindings(self):
        self.bind("<Up>", lambda event: self.step(0))
        self.bind("<Down>", lambda event: self.step(1))
        self.bind("<Left>", lambda event: self.step(2))
        self.bind("<Right>", lambda event: self.step(3))
        self.canvas.bind("<Button-1>", lambda event: self.step(3))
    
    def draw(self):
        self.canvas.move(self.rectangle, UNIT, UNIT)
        self.canvas.after(100, self.draw)







if __name__=="__main__":
    env = Gridworld(modus='manual')
    #env.update()
    #time.sleep(5)
    #print('MOVE!')
    # env.step(3)
    # env.draw()
    
    tk.mainloop()