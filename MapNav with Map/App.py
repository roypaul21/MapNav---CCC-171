import pygame
import pickle
import csv
from tkinter import *
from AStarSearch import *
from Settings import *
from Grid import Grid



class App:
    def __init__(self):
        self.start = None
        self.goal = None
        self.ready = False
        self.searched = False
        self.grid = Grid(ROW_NUM, COL_NUM)
        self.path = []
        pygame.init()
        # Set the HEIGHT and WIDTH of the self.screen
        self.window_size = [int(10 * COL_NUM + 95), int(15 * ROW_NUM + 20)]
        self.screen = pygame.display.set_mode(self.window_size)
        # Set title of self.screen
        pygame.display.set_caption("Simple AI MapNav")
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('MapNav', True, BLUE, BLACK)
        textRect = text.get_rect()
        textRect.center = (200, 630)
        self.screen.blit(text, textRect)

    def run(self):
        # Loop until the user clicks the close button.
        done = False
        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ready = True


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT\
                        and self.get_cell(pygame.mouse.get_pos())[0] < ROW_NUM\
                        and self.get_cell(pygame.mouse.get_pos())[1] < COL_NUM:
                    if not self.start:
                        cell = self.get_cell(pygame.mouse.get_pos())
                        if not self.grid.is_obstacle(cell):
                            self.start = (cell)
                            self.grid.set_color(self.start, GREEN)
                    elif not self.goal:
                        cell = self.get_cell(pygame.mouse.get_pos())
                        if not self.grid.is_obstacle(cell):
                            self.goal = cell
                            self.grid.set_color(self.goal, RED)
                    elif not self.ready:
                        cell = self.get_cell(pygame.mouse.get_pos())
                        self.grid.set_color(cell, BLACK)
                        self.grid.set_obstacle(cell)
            # Set the screen background
            self.screen.fill(BLACK)

            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Simple MapNav', True, BLUE, BLACK)
            textRect = text.get_rect()
            textRect.center = (650,630)
            self.screen.blit(text, textRect)

            self.button("Clear", (self.window_size[0] - 400) / 2, self.window_size[1] - 100,
                        100, 50, GREY, WHITE, self.clean)
            self.button("Map", (self.window_size[0] + 200) / 2, self.window_size[1] - 100,
                        100, 50, GREY, WHITE, self.draw_maze)

            self.button("Distance", (self.window_size[0] - 120) / 2, self.window_size[1] - 100,
                        120, 50, GREY, WHITE, self.distance_path)

            # if obstacle, goal and starting point all set, find the shortest path through a* search
            if self.ready and not self.searched:
                self.path = a_star_search_visualize(self, self.grid, self.start, self.goal)
                self.searched = True

            for item in self.path:
                if item != self.start and item != self.goal:
                    self.grid.set_color(item, BLACK)
            self.draw_graph(FAST)

        pygame.quit()
        quit()

    def distance_path(self):

        window = Tk()
        window.title("MapNav")
        window.geometry(f'{550}x{100}+{700}+{466}')
        window.resizable(False, False)
        count_path = pickle.load(open("PathCount.dat", "rb"))
        dis = pickle.load(open("destination.dat", "rb"))
        window.overrideredirect(True)
        print(count_path)
        print(dis)

        def exit():
            window.destroy()

        Label(window, text=str(count_path) + " Meters From " + str(dis[0]) + " To " + str(dis[1]), bg="white", fg="black", font=("none 16 bold")).place(x=0, y=0)
        Button(window, text="OK", width=8, bg="light gray", command=exit).place(x=100, y=50)


        window.configure(background="white")

        window.mainloop()

    def draw_maze(self):

        window = Tk()
        window.title("MapNav")
        window.geometry(f'{400}x{150}+{460}+{280}')
        window.resizable(False, False)
        window.configure(background="white")

        def submit():
            from_where = variable.get()
            to_where = variable2.get()

            save_data = [from_where,to_where]
            pickle.dump(save_data, open("destination.dat", "wb"))

            window.destroy()



        destination = ["Select From","Entrance","EXIT","Administration","GYM","Clinic","CCS","CSM","COET",
                        "CON","CBAA","CASS","IDS","Complex","Libray","DHS","MICel","KASAMA"]
        variable = StringVar()
        variable.set(destination[0])

        destination2 = ["Select To","Entrance","EXIT","Administration","GYM","Clinic","CCS","CSM","COET",
                        "CON","CBAA","CASS","IDS","Complex","Libray","DHS","MICel","KASAMA"]
        variable2 = StringVar()
        variable2.set(destination2[0])

        Label(window, text="Choose Destination", bg="white", fg="black", font=("none 13 bold")) .place(x=120,y=20)

        Label(window, text="FROM:", bg="white", fg='GREEN', font=("none 11 bold")).place(x=55, y=50)
        Label(window, text="TO:", bg="white", fg='RED', font=("none 11 bold")).place(x=250, y=50)

        from_1= OptionMenu(window, variable, *destination)
        from_1.place(x=55,y=70)
        to_1 = OptionMenu(window, variable2, *destination2)
        to_1.place(x=250, y=70)
        Button(window, text="Submit", width=8, command=submit) .place(x=163,y=110)

        window.mainloop()

        dis = pickle.load(open("destination.dat", "rb"))

        from_where = dis[0]
        to_where = dis[1]


        self.clean()
        for i in range(ROW_NUM):

            with open('coordinates.csv') as f:
                reader = csv.DictReader(f, delimiter=',')

                for row in reader:
                    name = row['Name']
                    coor_x = row['x_coor']
                    coor_y = row['y_coor']

                    if from_where in name:
                        from_x = int(coor_x)
                        from_y = int(coor_y)
                        self.start = (from_x, from_y)
                        self.grid.set_color(self.start, GREEN)

                    if to_where in name:
                        to_x = int(coor_x)
                        to_y = int(coor_y)

                        # Where to
                        self.goal = (to_x, to_y)
                        self.grid.set_color(self.goal, RED)

                        self.grid.set_obstacle((i, 0))
                        self.grid.set_obstacle((i, COL_NUM - 1))



            self.grid.set_obstacle((i, 0))

            self.grid.set_obstacle((i, COL_NUM - 13))
            for j in range(5):
                for n in range(16):
                    self.grid.set_cass((1 + j, 20 + n))

            for j in range(6):
                for n in range(14):
                    self.grid.set_ced((10 + j, 1 + n))

            for j in range(4):
                for n in range(16):
                    self.grid.set_con((1 + j, 50 + n))

            if i < 5:
               self.grid.set_obstacle((i, 40))

            for j in range(4):
                self.grid.set_obstacle((9 + j, 38))

            for j in range(2):
                self.grid.set_obstacle((6 + j, 38))

            x = [1,2,3,4,5,6,7,8,9,10]
            for j in x:
                self.grid.set_obstacle((14 + j, 38))

            for j in range(22):
                for n in range(12):
                    self.grid.set_obstacle((27 + j, 38 + n))

            for j in range(5):
                for n in range(3):
                    self.grid.set_building((25 + j, 88 + n))

            for j in range(2):
                for n in range(16):
                    self.grid.set_obstacle((16 + j, 91 + n))

            #Gym
            for j in range(5):
                for n in range(4):
                    self.grid.set_obstacle((8 + j, 89 + n))

            for j in range(7):
                for n in range(12):
                    self.grid.set_building((8 + j, 95 + n))

            #CON
            for j in range(5):
                for n in range(10):
                    self.grid.set_obstacle((0 + j, 40 + n))

            for j in range(5):
                for n in range(22):
                    self.grid.set_obstacle((0 + j, 65 + n))

            for j in range(3):
                for n in range(4):
                    self.grid.set_obstacle((3 + j, 89 + n))

            for j in range(3):
                for n in range(3):
                    self.grid.set_obstacle((3 + j, 94 + n))

            for j in range(5):
                for n in range(9):
                    self.grid.set_obstacle((1 + j, 99 + n))

            x = [1, 2, 3, 4,5,6,7,8,9,10,11,12]
            for j in x:
                self.grid.set_obstacle((33 + j, 11))

            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
            y = [1, 2]
            for j in x:
                for n in y:
                    self.grid.set_obstacle((32 + j, 31+n))

            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]
            for j in x:
                self.grid.set_obstacle((32 + j, 9))

            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11  ]
            for j in x:
                self.grid.set_obstacle((34 + j, 35))

            #admin building
            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13,14]
            y = [1, 2, 3, 4,5,6]
            for j in x:
                for n in y:
                    self.grid.set_building((32 + j, n))

        for i in range(COL_NUM):
            self.grid.set_obstacle((0, i))
            self.grid.set_obstacle((ROW_NUM - 1, i))

            for j in range(5):
                for n in range(13):
                    self.grid.set_building((26+j, 8+ n))


            for j in range(9):
                for n in range(32):
                    self.grid.set_obstacle((16 + j,4+ n))

            for j in range(9):
                for n in range(21):
                    self.grid.set_obstacle((1 + j, n))

            for j in range(7):
                for n in range(21):
                    self.grid.set_obstacle((6 + j,15 + n))

            for j in range(2):
                for n in range(21):
                    self.grid.set_obstacle((14 + j,15 + n))

            for j in range(9):
                for n in range(3):
                    self.grid.set_obstacle((16 + j, n))

            for j in range(5):
                for n in range(14):
                    self.grid.set_building((26 + j,22+ n))

            if i < 36:
                self.grid.set_obstacle((ROW_NUM - 3, i))
            if i < 36:
                self.grid.set_obstacle((ROW_NUM - 2, i))

            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            for j in x:
                self.grid.set_obstacle((ROW_NUM - 17, 10 + j))

            x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14]
            for j in x:
                self.grid.set_obstacle((ROW_NUM - 17, 21 + j))


            for j in range(50):
                for n in range(10):
                    self.grid.set_obstacle((ROW_NUM - 23 + n, 38 + j))

            #med Building
            for j in range(7):
                for n in range(5):
                    self.grid.set_med((ROW_NUM - 23 + n, 38 + j))

            for j in range(7):
                for n in range(5):
                    self.grid.set_building((ROW_NUM - 10 + n, 38 + j))

            for j in range(5):
                for n in range(4):
                    self.grid.set_building((ROW_NUM -16   + n, 38 + j))


            for j in range(12):
                for n in range(7):
                    self.grid.set_micel((ROW_NUM - 23 + n, 48 + j))

            #css
            for j in range(15):
                for n in range(8):
                    self.grid.set_ccs((ROW_NUM - 23 + n, 66 + j))



            #CSM Builing
            for j in range(30):
                for n in range(10):
                    self.grid.set_building((ROW_NUM - 35 + n, 38 + j))

            for j in range(4):
                for n in range(10):
                    self.grid.set_con((ROW_NUM - 35 + n, 69 + j))

            for j in range(17):
                for n in range(10):
                    self.grid.set_csm((ROW_NUM - 35 + n, 74 + j))

            #CBAA to COET Building
            for j in range(7):
                for n in range(13):
                    self.grid.set_cbaa((6+j, 40+ n))

            for j in range(7):
                for n in range(14):
                    self.grid.set_cbaa((6 + j, 54 + n))

            for j in range(7):
                for n in range(15):
                    self.grid.set_coet  ((6 + j, 72 + n))



    def get_cell(self, pos):
        # Change the x/y screen coordinates to grid coordinates
        col = pos[0] // (CELL_WIDTH + MARGIN)
        row = pos[1] // (CELL_HEIGHT + MARGIN)
        return row, col


    def draw_graph(self, speed):
        # Draw the grid
        for row in range(ROW_NUM):
            for col in range(COL_NUM):
                color = self.grid.grid_color[row][col]
                pygame.draw.rect(self.screen,
                                 color,
                                 [(MARGIN + CELL_WIDTH) * col + MARGIN,
                                  (MARGIN + CELL_HEIGHT) * row + MARGIN,
                                  CELL_WIDTH,
                                  CELL_HEIGHT])
        self.clock.tick(speed)
        # update the screen with what we've drawn.
        pygame.display.flip()

    def intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(WHITE)
            large_text = pygame.font.Font('freesansbold.ttf', LARGE_TEXT_FONT)
            text_surf, text_rect = self.text_objects("A Simple AI MapNav", large_text)
            text_rect.center = ((self.window_size[0] / 2), (self.window_size[1] / 4))
            self.screen.blit(text_surf, text_rect)
            self.button("Start!", (self.window_size[0] - 100) / 2, self.window_size[1] / 2,
                        100, 50, WHITE, BLUE, self.run)
            pygame.display.update()
            self.clock.tick(15)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()


    def clean(self):
        self.searched = False
        self.start = None
        self.goal = None
        self.ready = False
        self.grid = Grid(ROW_NUM, COL_NUM)
        self.path = []

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))

            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h))

        small_text = pygame.font.SysFont("comicsansms", SMALL_TEXT_FONT)
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(text_surf, text_rect)




if __name__ == "__main__":
    app = App()
    app.intro()