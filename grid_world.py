""" Grid world dimension 7x10. Origin (0,0) at upper left corner.
Start at (0,3) ; Goal at (3,7)
Cross-wind on y-axis accordind following scheme [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
Agent cannot fall over the edge, but keeps
"""

from math import inf
import tkinter as tk
from PIL import ImageTk, Image
import time

PhotoImage = ImageTk.PhotoImage
UNIT = 75  # pixels
# HEIGHT = 10  # grid height
# WIDTH = 10  # grid width
INFO_BOX = 2
WIND_BOX = 2


class Gridworld(tk.Tk):
    def __init__(self, move='cross', modus='RL'):
        super(Gridworld, self).__init__()

        # set world
        self.dim_x = 10
        self.dim_y = 7
        self.wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
        
        self.start = (0,3)
        self.goal =  (7,3)

        self.pos_x = self.start[0]
        self.pos_y = self.start[1]

        self.set_action_space(move)
        self.observation_size = (self.dim_x, self.dim_y)
        self.state = [(x,y) for x in range(self.dim_x) for y in range(self.dim_y)]
        self.state_size = len(self.state)

        self.counter = 0
        self.reward = 0
        self.rewards = 0
        self.highscore = -inf
        self.round = 0
        self.mode = modus


        # set canvas
        self.title_text = 'Windy grid world'
        self.title(self.title_text)
        self.tk_setPalette(background='white', foreground='black',
               activeBackground='red', activeForeground='blue')
        # Tkinter.Button(root, text="Press me!").pack()
        self.geometry('{0}x{1}'.format(UNIT * self.dim_x , UNIT * (self.dim_y + INFO_BOX + WIND_BOX)))
        self.ub_score, self.ub_highscore, self.ub_round = self._build_upper_box()
        self.shapes = self._load_images()
        self.canvas = self._build_canvas()
        self.lower_box, self.lb_arrows = self._build_lower_box()



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

    def _build_upper_box(self):
        """Set info box at the top"""
        # background white!
        upper_box = tk.Frame(self, width=UNIT*self.dim_x, height=2*UNIT)
        upper_box.pack()

        title_font = ("Courier", int(40))
        title_label = tk.Label(upper_box, text=self.title_text, font=title_font)
        title_label.pack()

        main_font = ("Courier", int(25))

        info_box = tk.Frame(upper_box, height=UNIT)
        info_box.pack()

        score = tk.Label(info_box, text=f'SCORE: {self.rewards} \t', font=main_font)
        score.grid(row=0,column=0)

        highscore = tk.Label(info_box, text=f'HIGHSCORE:{self.highscore} \t', font=main_font)
        highscore.grid(row=1,column=0)
        
        mode = tk.Label(info_box, text=f'MODE: {self.mode} \t', font=main_font)
        mode.grid(row=0,column=1)

        round = tk.Label(info_box, text=f'ROUND: {self.round} \t', font=main_font)
        round.grid(row=1,column=1)

        return score, highscore, round


    def update_upper_box(self):
        self.ub_score.config(text=f'SCORE: {self.rewards} \t')
        self.ub_highscore.config(text=f'HIGHSCORE:{self.highscore} \t')
        self.ub_round.config(text=f'ROUND: {self.round} \t')

    def update_lower_box(self):
        c=0
        for arrow in self.lb_arrows:
            if self.pos_x ==c:
                self.lower_box.itemconfig(arrow, fill='red')
            else:
                self.lower_box.itemconfig(arrow, fill='grey')
            c += 1


    def _draw_wind_strength(self):
        """ Wind is visualized dynamically, such that acstive pushing can be seen"""
        pass


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

        # add image to canvas
        x, y = self.state_to_coords(self.start)
        self.rectangle = canvas.create_image(x, y, image=self.shapes[0])

        x, y = self.state_to_coords(self.goal)
        self.circle = canvas.create_image(x, y, image=self.shapes[2])

        # pack all`
        # canvas.pack(padx=.5, pady=.5, anchor='center')

        # canvas.place(relx=0.5, y=2*UNIT, anchor='n')
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

    def _build_lower_box(self):

        lower_box = tk.Canvas(self, bg='white', 
                    width=self.dim_x * UNIT,
                    height=2 * UNIT)

        arrows = []
        counter=0
        for c in range(0, self.dim_x * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = UNIT/2 + c, UNIT/2, UNIT/2 + c, UNIT
            arrows.append(lower_box.create_line(x0, y0, x1, y1, fill='grey', arrow=tk.FIRST,
            arrowshape=(20,20,10), width=25))
            lower_box.create_text(x0, y0+UNIT, text=self.wind[counter], fill='black', font=("Courier", int(25)))
            counter +=1
       

        lower_box.pack()

        return lower_box, arrows
        


    def move(self, direction):
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

        return (new_pos_x, new_pos_y)
 



    def _move_agent(self, move_x, move_y):
        """ This function renders agent move on canvas"""
        move_x *= UNIT
        move_y *= UNIT
        
        self.canvas.move(self.rectangle, move_x, move_y)
        self.render()

    def get_state_idx(self, state):
        return self.state.index(state)

    def get_current_state_idx(self):
        return self.state.index((self.pos_x, self.pos_y))


    def state_to_coords(self, state):
        x, y = state
        return UNIT/2 + x * UNIT , UNIT/2 + y * UNIT
        

    def get_reward(self, state):
        if state == self.goal:
            return 1000, True
        else:
            return -1, False

    def step(self, action_idx):
        self.counter += 1
        direction = self.get_direction(action_idx)
        new_state = self.move(direction)
        reward, done = self.get_reward(new_state)
        self.rewards += reward
        self.update_upper_box()
        self.update_lower_box()
        new_state_idx = self.get_state_idx(new_state)
        return new_state_idx, reward, done

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

    def get_observation_size(self):
        return self.observation_size

    def get_state_size(self):
        return self.state_size

    def get_action_size(self):
        return self.action_size 

    def render(self):
        # time.sleep(1)
        self.update()
        # self.update_idletasks()

    def reset(self):
        self.pos_x = self.start[0]
        self.pos_y = self.start[1]

        self.update_stats()

        self.update_upper_box()

        self.render()
        x, y = self.state_to_coords(self.start)
        self.canvas.coords(self.rectangle, x, y)
        

     
    def bindings(self):
        self.bind("<Up>", lambda event: self.manual_step(0))
        self.bind("<Down>", lambda event: self.manual_step(1))
        self.bind("<Left>", lambda event: self.manual_step(2))
        self.bind("<Right>", lambda event: self.manual_step(3))
        # self.canvas.bind("<Button-1>", lambda event: self.step(3))
    
    def draw(self):
        self.canvas.move(self.rectangle, UNIT, UNIT)
        self.canvas.after(100, self.draw)

    def manual_step(self, action_idx):
        _, _, done = self.step(action_idx)
        if done:
            self.round +=1
            if self.highscore < self.rewards: self.highscore = self.rewards
            self.reset()
    
    def update_stats(self):
        self.round +=1
        if self.highscore < self.rewards: self.highscore = self.rewards
        self.rewards=0




if __name__=="__main__":
    env = Gridworld(modus='manual')
    tk.mainloop()