import sys
import numpy as np
from random import randrange
from datetime import datetime

from flow.venv.Scripts.flow.combined import Combined
from flow.venv.Scripts.flow.path import Path

DETERMINISTIC = True


class State:
    def __init__(self, BOARD_ROWS, BOARD_COLS, WIN_STATE, LOSE_STATE, START, state):
        self.BOARD_ROWS = BOARD_ROWS
        self.BOARD_COLS = BOARD_COLS
        self.WIN_STATE = WIN_STATE
        self.LOSE_STATE = LOSE_STATE
        self.START = START
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.board[0, 1] = 2
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC


    def giveReward(self):
        if self.state == self.WIN_STATE:
            return 1
        elif self.state == self.LOSE_STATE:
            return -1
        else:
            return 0


    def isEndFunc(self):
        if (self.state == self.WIN_STATE) or (self.state == self.LOSE_STATE):
            self.isEnd = True


    def nxtPosition(self, action):
        if self.determine:
            if action == "up":
                nxtState = (self.state[0] - 1, self.state[1])
            elif action == "down":
                nxtState = (self.state[0] + 1, self.state[1])
            elif action == "left":
                nxtState = (self.state[0], self.state[1] - 1)
            else:
                nxtState = (self.state[0], self.state[1] + 1)
            # if next state legal
            if (nxtState[0] >= 0) and (nxtState[0] <= (self.BOARD_ROWS - 1)):
                if (nxtState[1] >= 0) and (nxtState[1] <= (self.BOARD_COLS - 1)):
                    if nxtState != (0, 0):
                        return nxtState
            return self.state


    def showBoard(self):
        self.board[self.state] = 1
        for i in range(0, self.BOARD_ROWS):
            # print('-----------------')
            out = '| '
            for j in range(0, self.BOARD_COLS):
                if self.board[i, j] == 1:
                    token = '*'
                if self.board[i, j] == -1:
                    token = 'z'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
        #   print(out)
        # print('-----------------')


# Agent of player

class Agent:

    def __init__(self, BOARD_ROWS, BOARD_COLS, WIN_STATE, LOSE_STATE, START, state):
        self.BOARD_ROWS = BOARD_ROWS
        self.BOARD_COLS = BOARD_COLS
        self.WIN_STATE = WIN_STATE
        self.LOSE_STATE = LOSE_STATE
        self.START = START
        self.state = state
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State(self.BOARD_ROWS, self.BOARD_COLS, self.WIN_STATE, self.LOSE_STATE, self.START, self.state)
        self.lr = 0.2
        self.exp_rate = 0.3

        # initial state reward
        self.state_values = {}
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.state_values[(i, j)] = 0  # set initial value to 0


    def chooseAction(self):
        # choose action with most expected value
        mx_nxt_reward = 0
        action = ""

        if np.random.uniform(0, 1) <= self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                # if the action is deterministic
                nxt_reward = self.state_values[self.State.nxtPosition(a)]
                if nxt_reward >= mx_nxt_reward:
                    action = a
                    mx_nxt_reward = nxt_reward
        return action


    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        return State(self.BOARD_ROWS, self.BOARD_COLS, self.WIN_STATE, self.LOSE_STATE, self.START, state=position)


    def reset(self):
        self.states = []
        self.State = State(self.BOARD_ROWS, self.BOARD_COLS, self.WIN_STATE, self.LOSE_STATE, self.START, self.state)


    def play(self, rounds=10):
        i = 0
        while i < rounds:
            # to the end of game back propagate reward
            if self.State.isEnd:
                # back propagate
                reward = self.State.giveReward()
                # explicitly assign end state to reward values
                self.state_values[self.State.state] = reward  # this is optional
                # print("Game End Reward", reward)
                for s in reversed(self.states):
                    reward = self.state_values[s] + self.lr * (reward - self.state_values[s])
                    self.state_values[s] = round(reward, 3)
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                # append trace
                self.states.append(self.State.nxtPosition(action))
                # print("current position {} action {}".format(self.State.state, action))
                # by taking the action, it reaches the next state
                self.State = self.takeAction(action)
                # mark is end
                self.State.isEndFunc()
                # print("nxt state", self.State.state)
                # print("---------------------")


    def showValues(self):
        for i in range(0, self.BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, self.BOARD_COLS):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')
        return self.state_values


if __name__ == "__main__":
    start = datetime.now()
    # ## original board
    # list_arg_steps = [[3, 3, [1], [(2, 0)], [(2, 2)], [(0, 0)]],
    #                   [3, 3, [2], [(2, 2)], [(2, 0)], [(0, 1)]]]
    #
    # starters = {1: [0, 0], 2: [0, 1]}
    # ends = {1: [2, 0], 2: [2, 2]}

    ## different colors
    # list_arg_steps = [[3, 3, [1], [(2, 0)], [(2, 2)], [(0, 0)]],
    #                   [3, 3, [4], [(2, 2)], [(2, 0)], [(0, 1)]]]

    # list_arg_steps = [[3, 3, [1], [(2, 0)], [(2, 1), (2, 2)], [(0, 0)]],
    #                   [3, 3, [2], [(2, 1)], [(2, 0), (2, 2)], [(0, 1)]],
    #                   [3, 3, [3], [(2, 2)], [(2, 0), (2, 1)], [(0, 2)]]]

    # list_arg_steps = [[4, 4, [1], [(3, 0)], [(3, 1), (3, 2), (3, 3)], [(0, 0)]],
    #                   [4, 4, [2], [(3, 1)], [(3, 0), (3, 2), (3, 3)], [(0, 1)]],
    #                   [4, 4, [3], [(3, 2)], [(3, 0), (3, 1), (3, 3)], [(0, 2)]],
    #                   [4, 4, [4], [(3, 3)], [(3, 0), (3, 1), (3, 2)], [(0, 3)]]]

    # list_arg_steps = [[5, 5, [1], [(4, 2)], [(0, 4), (1, 1), (1, 2), (1, 3), (4, 4), (3, 4)], [(0, 3)]],
    #                   [5, 5, [2], [(1, 3)], [(0, 3), (1, 1), (1, 2), (4, 2), (4, 4), (3, 4)], [(0, 4)]],
    #                   [5, 5, [3], [(4, 4)], [(0, 4), (0, 3), (1, 2), (4, 2), (1, 3), (3, 4)], [(1, 1)]],
    #                   [5, 5, [4], [(3, 4)], [(0, 3), (1, 1), (0, 4), (4, 2), (1, 3), (4, 4)], [(1, 2)]]]
    #
    # starters = {1: [0, 3], 2: [0, 4], 3: [1, 1], 4: [1, 2]}
    # ends = {1: [4, 2], 2: [1, 3], 3: [4, 4], 4: [3, 4]}

    list_arg_steps = [[7, 7, [1], [(6, 5)], [(2, 1), (5, 4), (4, 2), (6, 6), (5, 5), (1, 5), (1, 6), (3, 3), (3, 4), (4, 5)], [(0, 6)]], #B
                      [7, 7, [2], [(2, 1)], [(6, 5), (5, 4), (4, 2), (6, 6), (5, 5), (0, 6), (1, 6), (3, 3), (3, 4), (4, 5)], [(1, 5)]], #O
                      [7, 7, [3], [(5, 4)], [(2, 1), (6, 5), (4, 2), (6, 6), (5, 5), (1, 5), (0, 6), (3, 3), (3, 4), (4, 5)], [(1, 6)]],   #R
                      [7, 7, [4], [(4, 2)], [(2, 1), (5, 4), (6, 5), (6, 6), (5, 5), (1, 5), (1, 6), (0, 6), (3, 4), (4, 5)], [(3, 3)]],    #G
                      [7, 7, [5], [(6, 6)], [(2, 1), (5, 4), (4, 2), (6, 5), (5, 5), (1, 5), (1, 6), (3, 3), (0, 6), (4, 5)], [(3, 4)]],    #C
                      [7, 7, [6], [(5, 5)], [(2, 1), (5, 4), (4, 2), (6, 6), (6, 5), (1, 5), (1, 6), (3, 3), (3, 4), (0, 6)], [(4, 5)]]]    #Y

    starters = {1: [0, 6], 2: [1, 5], 3: [1, 6], 4: [3, 3], 5: [3, 4], 6: [4, 5]}
    ends = {1: [6, 5], 2: [2, 1], 3: [5, 4], 4: [4, 2], 5: [6, 6], 6: [5, 5]}


    def print_grid(grid_p):
        ## check grid_end before printing it
        for item in grid_p:
            print(item, '\n')
        # return grid_end


    dict_loses = {}
    # already_pos = []
    # for element in list_arg_steps:
    #     already_pos.append(element)

    scores = []
    grides = []
    for t in range(2):
        for i in range(0, len(list_arg_steps)):
            # pos = randrange(len(already_pos))
            # already_pos.remove(already_pos[pos])
            BOARD_ROWS = list_arg_steps[i][0]
            BOARD_COLS = list_arg_steps[i][1]
            colors = list_arg_steps[i][2]
            wins = list_arg_steps[i][3]
            loses = list_arg_steps[i][4]
            starts = list_arg_steps[i][5]
            dict_paths = {}
            if i == 0:
                grid = np.zeros([BOARD_ROWS, BOARD_COLS])
                for key in starters:
                    grid[starters[key][0], starters[key][1]] = key
                    grid[ends[key][0], ends[key][1]] = key
            else:
                grid = grid_end

            for k in range(0, len(colors)):
                for key in dict_loses.keys():
                    for cell in dict_loses[key]:
                        list(loses[k]).append((cell[0], cell[1]))

                ag = Agent(BOARD_ROWS, BOARD_COLS, wins[k], loses[k], starts[k], starts[k])
                ag.play(50)
                weighted_grid = ag.showValues()
                path_tracker = Path(BOARD_ROWS, BOARD_COLS, wins[k], starts[k], weighted_grid)
                path = path_tracker.get_path()
                dict_paths[colors[k]] = path
                dict_loses[colors[k]] = path
                combined_grid = Combined(BOARD_ROWS, BOARD_COLS, dict_paths, grid, starters, ends)
                grid_end, score = combined_grid.print_grid()
        print('score num {}: '.format(t), score)
        scores.append(score)
        grides.append(grid_end)
        # print_grid(grid_end)
    index_max = scores.index(max(scores))
    print('max_score: ', max(scores))
    print_grid(grides[index_max])
    reduce_time = (datetime.now() - start).total_seconds()
    print(reduce_time)

