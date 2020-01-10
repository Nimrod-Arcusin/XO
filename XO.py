import random as rnd
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import time


class XO:
    # for the AI
    vow = 5
    vol = -2
    vof = 1
    vxw = 2
    vxl = -2
    vxf = -1
    number_of_train_runs = 100
    how_to_train_x = 'rnd'  # super, ai, com, rnd
    how_to_train_o = 'rnd'

    def __init__(self, what_to_play, player):
        self.board = ['  11 ', '  12 ', '  13 ', '  21 ', '  22 ', '  23 ', '  31 ', '  32 ', '  33 ']
        self.newboard = ['  11 ', '  12 ', '  13 ', '  21 ', '  22 ', '  23 ', '  31 ', '  32 ', '  33 ']
        self.option = [11, 12, 13, 21, 22, 23, 31, 32, 33]
        self.left = [11, 12, 13, 21, 22, 23, 31, 32, 33]
        self.xturn = True
        self.what_to_play = what_to_play   # gui, console, train
        self.com_think_time = 0.5
        self.player = player  # ai, com, rnd, super, p

        self.action = ""
        self.file = open("AI", 'r')
        self.games = self.file.readlines()
        self.file.close()

        if self.what_to_play == 'gui':
            self.init_gui()
            self.g.mainloop()
        elif self.what_to_play == 'console':
            self.main()
        elif self.what_to_play == 'train':
            self.train()

    def init_gui(self):
        self.g = tk.Tk()
        self.g.title('XO made by Nimrod Arcusin')
        self.b1 = tk.Button(self.g, command=self.b1p)
        self.b1.grid(row=0, column=0, sticky=N + S + E + W)
        self.b2 = tk.Button(self.g, command=self.b2p)
        self.b2.grid(row=0, column=1, sticky=N + S + E + W)
        self.b3 = tk.Button(self.g, command=self.b3p)
        self.b3.grid(row=0, column=2, sticky=N + S + E + W)
        self.b4 = tk.Button(self.g, command=self.b4p)
        self.b4.grid(row=1, column=0, sticky=N + S + E + W)
        self.b5 = tk.Button(self.g, command=self.b5p)
        self.b5.grid(row=1, column=1, sticky=N + S + E + W)
        self.b6 = tk.Button(self.g, command=self.b6p)
        self.b6.grid(row=1, column=2, sticky=N + S + E + W)
        self.b7 = tk.Button(self.g, command=self.b7p)
        self.b7.grid(row=2, column=0, sticky=N + S + E + W)
        self.b8 = tk.Button(self.g, command=self.b8p)
        self.b8.grid(row=2, column=1, sticky=N + S + E + W)
        self.b9 = tk.Button(self.g, command=self.b9p)
        self.b9.grid(row=2, column=2, sticky=N + S + E + W)
        self.bb = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9]
        self.N_photo = PhotoImage(file=r"N.png")
        self.X_photo = PhotoImage(file=r"X.png")
        self.O_photo = PhotoImage(file=r"O.png")
        self.N_photo = self.N_photo.subsample(2, 2)
        self.X_photo = self.X_photo.subsample(2, 2)
        self.O_photo = self.O_photo.subsample(2, 2)
        # N_photo = N_photo.zoom(2, 2)
        # X_photo = X_photo.zoom(2, 2)
        # O_photo = O_photo.zoom(2, 2)
        self.g.resizable(False, False)
        self.paint()

    @classmethod
    def outside_train(cls, how_to_train_x, how_to_train_o):
        XO.how_to_train_x = how_to_train_x
        XO.how_to_train_o = how_to_train_o
        cls('train', '')

    def print_board(self):
        print(self.board[0], '| ', self.board[1], '| ', self.board[2])
        print('-----------------------')
        print(self.board[3], '| ', self.board[4], '| ', self.board[5])
        print('-----------------------')
        print(self.board[6], '| ', self.board[7], '| ', self.board[8])

    def place(self, xy):
        count = 0
        xy = int(xy)
        for o in self.option:
            if o is xy:
                break
            count += 1
        if self.xturn:
            self.board[count] = ['X']
        else:
            self.board[count] = ['O']
        self.left.remove(xy)
        self.action = self.action + str(xy) + ' '
        self.xturn = not self.xturn

    def play(self):
        xy = input('move: ')
        while xy not in str(self.left) or xy.__len__() is not 2:
            print('not valid')
            xy = input('move: ')
        xy = int(xy)
        self.place(xy)

    def check_lines(self):
        if self.board[0] == self.board[1] and self.board[0] == self.board[2]:  # 012
            return 0
        if self.board[3] == self.board[4] and self.board[3] == self.board[5]:  # 345
            return 3
        if self.board[6] == self.board[7] and self.board[6] == self.board[8]:  # 678
            return 6
        return 'N'

    def check_rows(self):
        if self.board[0] == self.board[3] and self.board[0] == self.board[6]:  # 036
            return 0
        if self.board[1] == self.board[4] and self.board[1] == self.board[7]:  # 147
            return 1
        if self.board[2] == self.board[5] and self.board[2] == self.board[8]:  # 258
            return 2
        return 'N'

    def check_diagonal(self):
        if self.board[0] == self.board[4] and self.board[0] == self.board[8]:  # 048
            return 0
        if self.board[2] == self.board[4] and self.board[2] == self.board[6]:  # 246
            return 2
        return 'N'

    def check_full(self):
        for b in self.board:
            if b != ['X'] and b != ['O']:
                return 'N'
        return 'F'

    def check_empty(self):
        for b in self.board:
            if b == ['X'] or b == ['O']:
                return 'N'
        return 'E'

    def check_win(self):
        c = self.check_lines()
        if c == 'N':
            c = self.check_rows()
            if c == 'N':
                c = self.check_diagonal()
                if c == 'N':
                    return self.check_full()
                else:
                    return self.board[c]
            else:
                return self.board[c]
        else:
            return self.board[c]
        return self.check_full()

    def c_line_win(self):
        player = ['O']
        enemy = ['X']
        if self.xturn:
            player = ['X']
            enemy = ['O']
        # first line
        if self.board[0] == self.board[1] and self.board[0] == player and self.board[2] != enemy:  # 12-
            return 13
        if self.board[0] == self.board[2] and self.board[0] == player and self.board[1] != enemy:  # 1-3
            return 12
        if self.board[1] == self.board[2] and self.board[1] == player and self.board[0] != enemy:  # -23
            return 11
        # second line
        if self.board[3] == self.board[4] and self.board[3] == player and self.board[5] != enemy:  # 45-
            return 23
        if self.board[3] == self.board[5] and self.board[3] == player and self.board[4] != enemy:  # 4-6
            return 22
        if self.board[4] == self.board[5] and self.board[4] == player and self.board[3] != enemy:  # -56
            return 21
        # third line
        if self.board[6] == self.board[7] and self.board[6] == player and self.board[8] != enemy:  # 78-
            return 33
        if self.board[6] == self.board[8] and self.board[6] == player and self.board[7] != enemy:  # 7-9
            return 32
        if self.board[7] == self.board[8] and self.board[7] == player and self.board[6] != enemy:  # -89
            return 31
        return 'N'

    def c_row_win(self):
        player = ['O']
        enemy = ['X']
        if self.xturn:
            player = ['X']
            enemy = ['O']
        # first row
        if self.board[0] == self.board[3] and self.board[0] == player and self.board[6] != enemy:  # 14-
            return 31
        if self.board[0] == self.board[6] and self.board[0] == player and self.board[3] != enemy:  # 1-7
            return 21
        if self.board[3] == self.board[6] and self.board[3] == player and self.board[0] != enemy:  # -47
            return 11
        # second row
        if self.board[1] == self.board[4] and self.board[1] == player and self.board[7] != enemy:  # 25-
            return 32
        if self.board[1] == self.board[7] and self.board[1] == player and self.board[4] != enemy:  # 2-8
            return 22
        if self.board[4] == self.board[7] and self.board[4] == player and self.board[1] != enemy:  # -58
            return 12
        # third row
        if self.board[2] == self.board[5] and self.board[2] == player and self.board[8] != enemy:  # 36-
            return 33
        if self.board[2] == self.board[8] and self.board[2] == player and self.board[5] != enemy:  # 3-9
            return 23
        if self.board[5] == self.board[8] and self.board[5] == player and self.board[2] != enemy:  # -69
            return 13
        return 'N'

    def c_diagonal_win(self):
        player = ['O']
        enemy = ['X']
        if self.xturn:
            player = ['X']
            enemy = ['O']
        # \ line
        if self.board[0] == self.board[4] and self.board[0] == player and self.board[8] != enemy:  # 15-
            return 33
        if self.board[0] == self.board[8] and self.board[0] == player and self.board[4] != enemy:  # 1-9
            return 22
        if self.board[4] == self.board[8] and self.board[4] == player and self.board[0] != enemy:  # -59
            return 11
        # / line
        if self.board[2] == self.board[4] and self.board[2] == player and self.board[6] != enemy:  # 35-
            return 31
        if self.board[2] == self.board[6] and self.board[2] == player and self.board[4] != enemy:  # 3-7
            return 22
        if self.board[4] == self.board[6] and self.board[4] == player and self.board[2] != enemy:  # -57
            return 13
        return 'N'

    def c_line_lose(self):
        player = ['O']
        enemy = ['X']
        if self.xturn:
            player = ['X']
            enemy = ['O']
        # im lazy that's way i only switch between player and enemy
        tmp = player
        player = enemy
        enemy = tmp
        # first line
        if self.board[0] == self.board[1] and self.board[0] == player and self.board[2] != enemy:  # 12-
            return 13
        if self.board[0] == self.board[2] and self.board[0] == player and self.board[1] != enemy:  # 1-3
            return 12
        if self.board[1] == self.board[2] and self.board[1] == player and self.board[0] != enemy:  # -23
            return 11
        # second line
        if self.board[3] == self.board[4] and self.board[3] == player and self.board[5] != enemy:  # 45-
            return 23
        if self.board[3] == self.board[5] and self.board[3] == player and self.board[4] != enemy:  # 4-6
            return 22
        if self.board[4] == self.board[5] and self.board[4] == player and self.board[3] != enemy:  # -56
            return 21
        # third line
        if self.board[6] == self.board[7] and self.board[6] == player and self.board[8] != enemy:  # 78-
            return 33
        if self.board[6] == self.board[8] and self.board[6] == player and self.board[7] != enemy:  # 7-9
            return 32
        if self.board[7] == self.board[8] and self.board[7] == player and self.board[6] != enemy:  # -89
            return 31
        return 'N'

    def c_row_lose(self):
        player = ['O']
        enemy = ['X']
        if self.xturn:
            player = ['X']
            enemy = ['O']
        # im lazy that's way i only switch between player and enemy
        tmp = player
        player = enemy
        enemy = tmp
        # first row
        if self.board[0] == self.board[3] and self.board[0] == player and self.board[6] != enemy:  # 14-
            return 31
        if self.board[0] == self.board[6] and self.board[0] == player and self.board[3] != enemy:  # 1-7
            return 21
        if self.board[3] == self.board[6] and self.board[3] == player and self.board[0] != enemy:  # -47
            return 11
        # second row
        if self.board[1] == self.board[4] and self.board[1] == player and self.board[7] != enemy:  # 25-
            return 32
        if self.board[1] == self.board[7] and self.board[1] == player and self.board[4] != enemy:  # 2-8
            return 22
        if self.board[4] == self.board[7] and self.board[4] == player and self.board[1] != enemy:  # -58
            return 12
        # third row
        if self.board[2] == self.board[5] and self.board[2] == player and self.board[8] != enemy:  # 36-
            return 33
        if self.board[2] == self.board[8] and self.board[2] == player and self.board[5] != enemy:  # 3-9
            return 23
        if self.board[5] == self.board[8] and self.board[5] == player and self.board[2] != enemy:  # -69
            return 13
        return 'N'

    def c_diagonal_lose(self):
        player = ['O']
        enemy = ['X']
        if self.xturn:
            player = ['X']
            enemy = ['O']
        # im lazy that's way i only switch between player and enemy
        tmp = player
        player = enemy
        enemy = tmp
        # \ line
        if self.board[0] == self.board[4] and self.board[0] == player and self.board[8] != enemy:  # 15-
            return 33
        if self.board[0] == self.board[8] and self.board[0] == player and self.board[4] != enemy:  # 1-9
            return 22
        if self.board[4] == self.board[8] and self.board[4] == player and self.board[0] != enemy:  # -59
            return 11
        # / line
        if self.board[2] == self.board[4] and self.board[2] == player and self.board[6] != enemy:  # 35-
            return 31
        if self.board[2] == self.board[6] and self.board[2] == player and self.board[4] != enemy:  # 3-7
            return 22
        if self.board[4] == self.board[6] and self.board[4] == player and self.board[2] != enemy:  # -57
            return 13
        return 'N'

    def rnd_play(self):
        xy = rnd.choice(self.left)
        print('rnd')
        self.place(xy)

    def com_play(self):
        xy = self.c_line_win()
        if xy == 'N':
            xy = self.c_row_win()
            if xy == 'N':
                xy = self.c_diagonal_win()
                if xy == 'N':
                    xy = self.c_line_lose()
                    if xy == 'N':
                        xy = self.c_row_lose()
                        if xy == 'N':
                            xy = self.c_diagonal_lose()
                            if xy == 'N':
                                xy = rnd.choice(self.left)
                                print('rnd')
        self.place(xy)

    def AI_play(self):
        if self.check_empty() == 'E':
            self.rnd_play()
        else:
            needed_games = []
            statistic = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in self.games:
                if str(i).startswith(self.action):
                    needed_games.append(str(i).replace(self.action, '').replace('\n', ''))
            if self.xturn:
                for i in needed_games:
                    if str(i).endswith('X'):
                        val = (str(i).count('X')) * self.vxw
                        if str(i).startswith('11'):
                            statistic[0] += val
                        elif str(i).startswith('12'):
                            statistic[1] += val
                        elif str(i).startswith('13'):
                            statistic[2] += val
                        elif str(i).startswith('21'):
                            statistic[3] += val
                        elif str(i).startswith('22'):
                            statistic[4] += val
                        elif str(i).startswith('23'):
                            statistic[5] += val
                        elif str(i).startswith('31'):
                            statistic[6] += val
                        elif str(i).startswith('32'):
                            statistic[7] += val
                        elif str(i).startswith('33'):
                            statistic[8] += val
                    elif str(i).endswith('O'):
                        val = str(i).count('O') * self.vxl
                        if str(i).startswith('11'):
                            statistic[0] += val
                        elif str(i).startswith('12'):
                            statistic[1] += val
                        elif str(i).startswith('13'):
                            statistic[2] += val
                        elif str(i).startswith('21'):
                            statistic[3] += val
                        elif str(i).startswith('22'):
                            statistic[4] += val
                        elif str(i).startswith('23'):
                            statistic[5] += val
                        elif str(i).startswith('31'):
                            statistic[6] += val
                        elif str(i).startswith('32'):
                            statistic[7] += val
                        elif str(i).startswith('33'):
                            statistic[8] += val
                    elif str(i).endswith('F'):
                        val = str(i).count('F') * self.vxf
                        if str(i).startswith('11'):
                            statistic[0] += val
                        elif str(i).startswith('12'):
                            statistic[1] += val
                        elif str(i).startswith('13'):
                            statistic[2] += val
                        elif str(i).startswith('21'):
                            statistic[3] += val
                        elif str(i).startswith('22'):
                            statistic[4] += val
                        elif str(i).startswith('23'):
                            statistic[5] += val
                        elif str(i).startswith('31'):
                            statistic[6] += val
                        elif str(i).startswith('32'):
                            statistic[7] += val
                        elif str(i).startswith('33'):
                            statistic[8] += val
            else:
                for i in needed_games:
                    if str(i).endswith('O'):
                        val = (str(i).count('O')) * self.vow
                        if str(i).startswith('11'):
                            statistic[0] += val
                        if str(i).startswith('12'):
                            statistic[1] += val
                        if str(i).startswith('13'):
                            statistic[2] += val
                        if str(i).startswith('21'):
                            statistic[3] += val
                        if str(i).startswith('22'):
                            statistic[4] += val
                        if str(i).startswith('23'):
                            statistic[5] += val
                        if str(i).startswith('31'):
                            statistic[6] += val
                        if str(i).startswith('32'):
                            statistic[7] += val
                        if str(i).startswith('33'):
                            statistic[8] += val
                    elif str(i).endswith('X'):
                        val = str(i).count('X') * self.vol
                        if str(i).startswith('11'):
                            statistic[0] += val
                        if str(i).startswith('12'):
                            statistic[1] += val
                        if str(i).startswith('13'):
                            statistic[2] += val
                        if str(i).startswith('21'):
                            statistic[3] += val
                        if str(i).startswith('22'):
                            statistic[4] += val
                        if str(i).startswith('23'):
                            statistic[5] += val
                        if str(i).startswith('31'):
                            statistic[6] += val
                        if str(i).startswith('32'):
                            statistic[7] += val
                        if str(i).startswith('33'):
                            statistic[8] += val
                    elif str(i).endswith('F'):
                        val = str(i).count('F') * self.vof
                        if str(i).startswith('11'):
                            statistic[0] += val
                        if str(i).startswith('12'):
                            statistic[1] += val
                        if str(i).startswith('13'):
                            statistic[2] += val
                        if str(i).startswith('21'):
                            statistic[3] += val
                        if str(i).startswith('22'):
                            statistic[4] += val
                        if str(i).startswith('23'):
                            statistic[5] += val
                        if str(i).startswith('31'):
                            statistic[6] += val
                        if str(i).startswith('32'):
                            statistic[7] += val
                        if str(i).startswith('33'):
                            statistic[8] += val
            best_move = rnd.randint(0, 8)
            count = 0
            for i in statistic:
                if self.option[count] not in self.left:
                    statistic[count] = -100000
                else:
                    if i > statistic[best_move]:
                        best_move = count
                count += 1
            print(statistic)
            print(self.option[best_move])
            if self.option[best_move] in self.left:
                self.place(self.option[best_move])
            else:
                self.rnd_play()

    def super_play(self):
        if self.check_empty() == 'E':
            self.rnd_play()
            return
        else:
            xy = self.c_line_win()
            if xy == 'N':
                xy = self.c_row_win()
                if xy == 'N':
                    xy = self.c_diagonal_win()
                    if xy == 'N':
                        xy = self.c_line_lose()
                        if xy == 'N':
                            xy = self.c_row_lose()
                            if xy == 'N':
                                xy = self.c_diagonal_lose()
                                if xy == 'N':
                                    needed_games = []
                                    statistic = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                                    for i in self.games:
                                        if str(i).startswith(self.action):
                                            needed_games.append(str(i).replace(self.action, '').replace('\n', ''))
                                    if self.xturn:
                                        for i in needed_games:
                                            if str(i).endswith('X'):
                                                val = (str(i).count('X')) * self.vxw
                                                if str(i).startswith('11'):
                                                    statistic[0] += val
                                                elif str(i).startswith('12'):
                                                    statistic[1] += val
                                                elif str(i).startswith('13'):
                                                    statistic[2] += val
                                                elif str(i).startswith('21'):
                                                    statistic[3] += val
                                                elif str(i).startswith('22'):
                                                    statistic[4] += val
                                                elif str(i).startswith('23'):
                                                    statistic[5] += val
                                                elif str(i).startswith('31'):
                                                    statistic[6] += val
                                                elif str(i).startswith('32'):
                                                    statistic[7] += val
                                                elif str(i).startswith('33'):
                                                    statistic[8] += val
                                            elif str(i).endswith('O'):
                                                val = str(i).count('O') * self.vxl
                                                if str(i).startswith('11'):
                                                    statistic[0] += val
                                                elif str(i).startswith('12'):
                                                    statistic[1] += val
                                                elif str(i).startswith('13'):
                                                    statistic[2] += val
                                                elif str(i).startswith('21'):
                                                    statistic[3] += val
                                                elif str(i).startswith('22'):
                                                    statistic[4] += val
                                                elif str(i).startswith('23'):
                                                    statistic[5] += val
                                                elif str(i).startswith('31'):
                                                    statistic[6] += val
                                                elif str(i).startswith('32'):
                                                    statistic[7] += val
                                                elif str(i).startswith('33'):
                                                    statistic[8] += val
                                            elif str(i).endswith('F'):
                                                val = str(i).count('F') * self.vxf
                                                if str(i).startswith('11'):
                                                    statistic[0] += val
                                                elif str(i).startswith('12'):
                                                    statistic[1] += val
                                                elif str(i).startswith('13'):
                                                    statistic[2] += val
                                                elif str(i).startswith('21'):
                                                    statistic[3] += val
                                                elif str(i).startswith('22'):
                                                    statistic[4] += val
                                                elif str(i).startswith('23'):
                                                    statistic[5] += val
                                                elif str(i).startswith('31'):
                                                    statistic[6] += val
                                                elif str(i).startswith('32'):
                                                    statistic[7] += val
                                                elif str(i).startswith('33'):
                                                    statistic[8] += val
                                    else:
                                        for i in needed_games:
                                            if str(i).endswith('O'):
                                                val = (str(i).count('O')) * self.vow
                                                if str(i).startswith('11'):
                                                    statistic[0] += val
                                                if str(i).startswith('12'):
                                                    statistic[1] += val
                                                if str(i).startswith('13'):
                                                    statistic[2] += val
                                                if str(i).startswith('21'):
                                                    statistic[3] += val
                                                if str(i).startswith('22'):
                                                    statistic[4] += val
                                                if str(i).startswith('23'):
                                                    statistic[5] += val
                                                if str(i).startswith('31'):
                                                    statistic[6] += val
                                                if str(i).startswith('32'):
                                                    statistic[7] += val
                                                if str(i).startswith('33'):
                                                    statistic[8] += val
                                            elif str(i).endswith('X'):
                                                val = str(i).count('X') * self.vol
                                                if str(i).startswith('11'):
                                                    statistic[0] += val
                                                if str(i).startswith('12'):
                                                    statistic[1] += val
                                                if str(i).startswith('13'):
                                                    statistic[2] += val
                                                if str(i).startswith('21'):
                                                    statistic[3] += val
                                                if str(i).startswith('22'):
                                                    statistic[4] += val
                                                if str(i).startswith('23'):
                                                    statistic[5] += val
                                                if str(i).startswith('31'):
                                                    statistic[6] += val
                                                if str(i).startswith('32'):
                                                    statistic[7] += val
                                                if str(i).startswith('33'):
                                                    statistic[8] += val
                                            elif str(i).endswith('F'):
                                                val = str(i).count('F') * self.vof
                                                if str(i).startswith('11'):
                                                    statistic[0] += val
                                                if str(i).startswith('12'):
                                                    statistic[1] += val
                                                if str(i).startswith('13'):
                                                    statistic[2] += val
                                                if str(i).startswith('21'):
                                                    statistic[3] += val
                                                if str(i).startswith('22'):
                                                    statistic[4] += val
                                                if str(i).startswith('23'):
                                                    statistic[5] += val
                                                if str(i).startswith('31'):
                                                    statistic[6] += val
                                                if str(i).startswith('32'):
                                                    statistic[7] += val
                                                if str(i).startswith('33'):
                                                    statistic[8] += val
                                    best_move = rnd.randint(0, 8)
                                    count = 0
                                    for i in statistic:
                                        if self.option[count] not in self.left:
                                            statistic[count] = -100000
                                        else:
                                            if i > statistic[best_move]:
                                                best_move = count
                                        count += 1
                                    print(statistic)
                                    print(self.option[best_move])
                                    if self.option[best_move] in self.left:
                                        xy = int(self.option[best_move])
                                    else:
                                        self.rnd_play()
                                        return
        self.place(xy)

    def the_game(self, x_player, o_player):
        while True:
            self.print_board()
            if self.xturn:
                if x_player == 'ai':
                    self.AI_play()
                elif x_player == 'com':
                    self.com_play()
                elif x_player == 'rnd':
                    self.rnd_play()
                elif x_player == 'super':
                    self.super_play()
                else:
                    self.play()
            else:
                if o_player == 'ai':
                    self.AI_play()
                elif o_player == 'com':
                    self.com_play()
                elif o_player == 'rnd':
                    self.rnd_play()
                elif o_player == 'super':
                    self.super_play()
                else:
                    self.play()
            bo = self.check_win()
            if bo is not 'N':
                self.print_board()
                self.action = self.action + str(bo)
                self.train_ai()
                self.reboot()
                break

    def reboot(self):
        self.board = ['  11 ', '  12 ', '  13 ', '  21 ', '  22 ', '  23 ', '  31 ', '  32 ', '  33 ']
        self.left = [11, 12, 13, 21, 22, 23, 31, 32, 33]
        self.xturn = True
        self.action = ""
        self.file = open("AI", 'r')
        self.games = self.file.readlines()
        self.file.close()
        if self.what_to_play is not 'train':
            self.paint()
            self.g.destroy()

    def train_ai(self):
        count = 0
        ddd = False
        for i in self.games:
            if str(i).startswith(self.action.replace('[', '').replace(']', '').replace('\'', '').replace('\n', '')):
                self.games[count] = self.games[count].replace('\n', '') + self.games[count].replace('\n', '')[-1:] + '\n'
                print(self.games[count])
                AI = open("AI", 'w')
                AI.writelines(self.games)
                AI.close()
                ddd = True
            count += 1
        if not ddd:
            AI = open("AI", 'a')
            AI.write(self.action.replace('[', '').replace(']', '').replace('\'', '') + '\n')
            AI.close()

    @staticmethod
    def sort_ai():
        AI = open("AI", 'r')
        games = AI.readlines()
        AI.close()
        games.sort()
        AI = open("AI", 'w')
        AI.writelines(games)
        AI.close()

    def main(self):
        while True:
            print('chose the play: \n'
                  'for player vs player enter pvp\n'
                  'for player vs com enter pvc\n'
                  'for com vs com enter cvc')
            choice = input()
            if choice == 'pvp':
                self.the_game('p', 'p')
            elif choice == 'pvc':
                self.the_game('p', 'ai')
            elif choice == 'cvc':
                self.the_game('ai', 'ai')
            else:
                print('not an option, try again\n')

    def train(self):
        for i in range(self.number_of_train_runs):
            self.the_game(self.how_to_train_x, self.how_to_train_o)
            print('*****' + str(i+1) + '*****')
        self.sort_ai()

    def gui_game(self, xy):
        self.place(xy)
        self.paint()
        bo = self.check_win()
        if bo == ['X'] or bo == ['O']:
            messagebox.showinfo('winner', f'{str(bo)} win!!!')
            self.action = self.action + str(bo)
            self.train_ai()
            self.reboot()
            return
        elif bo == 'F':
            messagebox.showinfo('tie', 'it is a tie')
            self.action = self.action + str(bo)
            self.train_ai()
            self.reboot()
            return
        if self.player == 'ai':
            self.AI_play()
        elif self.player == 'com':
            self.com_play()
        elif self.player == 'rnd':
            self.rnd_play()
        elif self.player == 'super':
            self.super_play()
        if self.player == 'ai' or self.player == 'com' or self.player == 'rnd' or self.player == 'super':
            time.sleep(self.com_think_time)
            self.paint()
            bo = self.check_win()
            if bo == ['X'] or bo == ['O']:
                messagebox.showinfo('winner', f'{str(bo)} win!!!')
                self.action = self.action + str(bo)
                self.train_ai()
                self.reboot()
            elif bo == 'F':
                messagebox.showinfo('tie', 'it is a tie')
                self.action = self.action + str(bo)
                self.train_ai()
                self.reboot()

    def paint(self):
        count = 0
        for i in self.board:
            if i in self.newboard:
                self.bb[count].configure(image=self.N_photo)
            elif i == ['X']:
                self.bb[count].configure(image=self.X_photo)
            elif i == ['O']:
                self.bb[count].configure(image=self.O_photo)
            count += 1
        self.g.update()

    def b1p(self):
        if self.board[0] != ['X'] and self.board[0] != ['O']:
            self.gui_game('11')

    def b2p(self):
        if self.board[1] != ['X'] and self.board[1] != ['O']:
            self.gui_game('12')

    def b3p(self):
        if self.board[2] != ['X'] and self.board[2] != ['O']:
            self.gui_game('13')

    def b4p(self):
        if self.board[3] != ['X'] and self.board[3] != ['O']:
            self.gui_game('21')

    def b5p(self):
        if self.board[4] != ['X'] and self.board[4] != ['O']:
            self.gui_game('22')

    def b6p(self):
        if self.board[5] != ['X'] and self.board[5] != ['O']:
            self.gui_game('23')

    def b7p(self):
        if self.board[6] != ['X'] and self.board[6] != ['O']:
            self.gui_game('31')

    def b8p(self):
        if self.board[7] != ['X'] and self.board[7] != ['O']:
            self.gui_game('32')

    def b9p(self):
        if self.board[8] != ['X'] and self.board[8] != ['O']:
            self.gui_game('33')


class Choise:
    def __init__(self):
        self.keep_playing = True
        font_size = 20
        self.m = tk.Tk()
        self.m.title('XO')
        self.pvp = Button(self.m, text='Player Vs Player', font=('Helvetica', font_size), command=self.player_vs_player).pack()
        self.pvc = Button(self.m, text='Player VS Com', font=('Helvetica', font_size), command=self.player_vs_com).pack()
        self.pva = Button(self.m, text='Player Vs AI', font=('Helvetica', font_size), command=self.player_vs_ai).pack()
        self.pvs = Button(self.m, text='Player Vs Super', font=('Helvetica', font_size), command=self.player_vs_super).pack()
        self.pvs = Button(self.m, text='Train AI', font=('Helvetica', font_size), command=self.train_ai).pack()
        self.m.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.m.mainloop()

    def player_vs_player(self):
        self.m.destroy()
        x = XO('gui', 'p')
        del x
        self.m.mainloop()

    def player_vs_com(self):
        self.m.destroy()
        x = XO('gui', 'com')
        del x
        self.m.mainloop()

    def player_vs_ai(self):
        self.m.destroy()
        x = XO('gui', 'ai')
        del x
        self.m.mainloop()

    def player_vs_super(self):
        self.m.destroy()
        x = XO('gui', 'super')
        del x
        self.m.mainloop()

    def train_ai(self):
        self.m.destroy()
        t = Training_Mode()
        del t
        self.m.mainloop()

    def on_closing(self):
        self.keep_playing = False
        self.m.destroy()
        print('Good Game!!!')


class Training_Mode:
    def __init__(self):
        self.keep_playing = True
        font_label_size = 20
        font_item_size = 16
        l1 = 10
        l2 = 50
        l3 = 100
        self.player1 = 'super'
        self.player2 = 'super'
        self.m = tk.Tk()
        self.m.geometry('280x170')
        self.m.title('XO')
        self.l1 = Label(self.m, text='How to train:', font=('Helvetica', font_label_size)).place(x=45, y=l1)

        self.p1 = Menubutton(self.m, text='super', font=('Helvetica', font_item_size))
        self.mb1 = Menu(self.p1, tearoff=0)
        self.mb1.add_checkbutton(label='Super', command=self.p1s)
        self.mb1.add_checkbutton(label='AI', command=self.p1a)
        self.mb1.add_checkbutton(label='Com', command=self.p1c)
        self.mb1.add_checkbutton(label='Random', command=self.p1r)
        self.p1.configure(menu=self.mb1)
        self.p1.place(x=20, y=l2)
        self.vs = Label(self.m, text=' vs ', font=('Helvetica', font_label_size)).place(x=110, y=l2)
        self.p2 = Menubutton(self.m, text='super', font=('Helvetica', font_item_size))
        self.mb2 = Menu(self.p2, tearoff=0)
        self.mb2.add_checkbutton(label='Super', command=self.p2s)
        self.mb2.add_checkbutton(label='AI', command=self.p2a)
        self.mb2.add_checkbutton(label='Com', command=self.p2c)
        self.mb2.add_checkbutton(label='Random', command=self.p2r)
        self.p2.configure(menu=self.mb2)
        self.p2.place(x=190, y=l2)

        self.tb = Button(self.m, text='Train', font=('Helvetica', font_label_size), command=self.train).place(x=80, y=l3)

        self.m.mainloop()

    def p1s(self):
        self.p1.configure(text='Super')
        self.player1 = 'super'

    def p1a(self):
        self.p1.configure(text='AI')
        self.player1 = 'ai'

    def p1c(self):
        self.p1.configure(text='Com')
        self.player1 = 'com'

    def p1r(self):
        self.p1.configure(text='Random')
        self.player1 = 'rnd'

    def p2s(self):
        self.p2.configure(text='Super')
        self.player2 = 'super'

    def p2a(self):
        self.p2.configure(text='AI')
        self.player2 = 'ai'

    def p2c(self):
        self.p2.configure(text='Com')
        self.player2 = 'com'

    def p2r(self):
        self.p2.configure(text='Random')
        self.player2 = 'rnd'

    def train(self):
        XO.outside_train(self.player1, self.player2)


c = Choise()
while c.keep_playing:
    c = Choise()
