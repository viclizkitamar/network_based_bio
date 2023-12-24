import numpy as np

class Path:
    def __init__(self, BOARD_ROWS, BOARD_COLS, end, start, board):
        self.BOARD_ROWS = BOARD_ROWS  # 3
        self.BOARD_COLS = BOARD_COLS  # 3
        self.END_STATE = end
        self.START = start
        self.board = board


    def get_path(self):
        path = [[self.START[0], self.START[1]]]
        i = self.START[0]
        j = self.START[1]
        while i < self.BOARD_ROWS:
            while j < self.BOARD_COLS:
                if self.END_STATE == (i + 1, j) or self.END_STATE == (i - 1, j) or self.END_STATE == (
                i, j + 1) or self.END_STATE == (i, j - 1):
                    i = self.BOARD_ROWS
                    j = self.BOARD_COLS
                    path.append([self.END_STATE[0], self.END_STATE[1]])
                    #print(path)
                else:
                    compare_list = []
                    valid_places = []

                    if i != 0:
                        compare_list.append(self.board[(i - 1, j)])
                        valid_places.append((i - 1, j))
                    else:
                        compare_list = compare_list
                    if j != 0:
                        compare_list.append(self.board[(i, j - 1)])
                        valid_places.append((i, j - 1))
                    else:
                        compare_list = compare_list
                    if i != self.BOARD_ROWS -1:
                        compare_list.append(self.board[(i + 1, j)])
                        valid_places.append((i + 1, j))
                    else:
                        compare_list = compare_list
                    if j != self.BOARD_COLS -1:
                        compare_list.append(self.board[(i, j + 1)])
                        valid_places.append((i, j + 1))
                    else:
                        compare_list = compare_list

                    max_next = max(compare_list)

                    for item in valid_places:
                        if max_next == self.board[(item[0], item[1])]:
                            path.append([item[0], item[1]])
                            i = item[0]
                            j = item[1]
        return path
