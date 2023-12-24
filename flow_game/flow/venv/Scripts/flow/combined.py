import numpy as np
import random


class Combined:

    def __init__(self, BOARD_ROWS, BOARD_COLS, path_dict, grid, starters, ends):
        self.BOARD_ROWS = BOARD_ROWS
        self.BOARD_COLS = BOARD_COLS
        self.grid = grid
        self.colors = []
        self.path_dict = {}
        self.starters = starters
        self.ends = ends
        for key in path_dict:
            self.path_dict[key] = path_dict[key]
            self.colors.append(key)


    def get_score_on_grid(self):
        # 1. if there are zeros in it
        # 2. check paths
        score = 0
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                if self.grid[i][j] == 0:
                    score -= 1

        for key, value in self.path_dict.items():
            for key2, value2 in self.path_dict.items():
                if key != key2 and value == value2:
                    score -= 2

        for key in self.starters.keys():
            if self.grid[self.starters[key][0]][self.starters[key][1]] != key or self.grid[self.ends[key][0]][
                self.ends[key][1]] != key:
                score -= 10

        return score


    def print_grid(self):
        for key, value in self.path_dict.items():
            for item in value:
                self.grid[item[0]][item[1]] = key

        score = self.get_score_on_grid()
        # print('score: ', score)
        # self.check_all_valid(collors_not_allowed)
        # self.check_collision()

        return self.grid, score


    def check_collision(self):
        for key, value in self.path_dict.items():
            for key2, value2 in self.path_dict.items():
                if key != key2 and value == value2:
                    print('collision between {} and {} colors, send one of the colors with blocked places? '.format(key,
                                                                                                                    key2))


    def check_all_valid(self, collors_not_allowed):
        for key in collors_not_allowed.keys():
            for i in range(self.BOARD_ROWS):
                for j in range(self.BOARD_COLS):
                    if self.grid[i][j] == 0 and (i, j) not in collors_not_allowed[key]:
                        self.grid[i][j] = key  # random.choice(self.colors)
