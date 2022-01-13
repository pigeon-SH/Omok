import numpy as np
import torch
import torch.nn as nn

import random
from Board import Board

class NN(nn.Module):
    def __init__(self, input_size, output_size):
        super(NN, self).__init__()
        self.layer = nn.Sequential(
            nn.Linear(input_size, 60),
            nn.ReLU(),
            nn.Linear(60, 120),
            nn.ReLU(),
            nn.Linear(120, 180),
            nn.ReLU(),
            nn.Linear(180, 240),
            nn.ReLU(),
            nn.Linear(240, 300),
            nn.ReLU(),
            nn.Linear(300, 400),
            nn.ReLU(),
            nn.Linear(400, 300),
            nn.ReLU(),
            nn.Linear(300, output_size),
            nn.ReLU()
        )
    
    def flatten(self, x):
        return torch.flatten(x, 1)
    
    def forward(self, x):
        #x = self.flatten(x)
        x = self.layer(x)
        return x

class Agent:
    def __init__(self, color, isAI):
        # color='B' or 'W'
        # isAI=true or false
        self.color = color
        self.isAI = isAI
        self.maxdepth = 3
        if self.color == 'W':
            self.enemy = 'B'
        else:
            self.enemy = 'W'
    """
    def f2(self, x):
        return x[1]
    
    # Override it
    def get_pos(self, board):
        poses = board.get_legal_pos()
        poses_dict = {}
        for i in range(len(poses)):
            poses_dict[poses[i]] = board.get_score(poses[i][0], poses[i][1], self.color, self.enemy)
        
        poses_dict = sorted(poses_dict.items(), key=self.f2, reverse=True)
        return poses_dict[0][0]
    """

class Minimax(Agent):
    def get_pos(self, board):
        _, pos = self.get_score_mine(board, 1)
        return pos

    def get_score_mine(self, board, depth):
        actions = board.get_legal_pos()
        score_max = 0
        for act in actions:
            if depth >= self.maxdepth:
                score = board.get_score(act[0], act[1], self.color, self.enemy)
            else:
                newboard = board.deepCopy()
                newboard.putdown(act, self.color)
                score, act = self.get_score_enemy(newboard, depth + 1)
            
            if score > score_max:
                score_max = score
                pos = act    
        return score_max, pos
    
    def get_score_enemy(self, board, depth):
        actions = board.get_legal_pos()
        score_max = 0
        for act in actions:
            if depth >= self.maxdepth:
                score = board.get_score(act[0], act[1], self.enemy, self.color)
            else:
                newboard = board.deepCopy()
                newboard.putdown(act, self.enemy)
                score, act = self.get_score_mine(newboard, depth + 1)
            
            if score > score_max:
                score_max = score
                pos = act
        
        return score_max, pos

class NNAgent:
    def __init__(self, color, isAI, input_size, output_size, weight):
        self.color = color
        self.isAI = isAI

        self.action_size = output_size
        self.learning_rate = 0.01
        self.epsilon = 1.0
        self.epsilon_decay = 0.99
        self.discount_factor = 0.9

        self.model = NN(input_size, output_size)
        self.target_model = NN(input_size, output_size)
        self.load_model(weight)
        self.update_target_model()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.loss_func = nn.CrossEntropyLoss()

        self.boards = []
        self.actions = []
    
    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())
    
    def load_model(self, state):
        self.model.load_state_dict(state)
    
    def save_model(self):
        return self.model.state_dict()
    
    def choose_action(self, board):
        while True:
            if np.random.rand() <= self.epsilon:
                arg = random.randrange(self.action_size)
            else:
                arg = np.argmax(self.model(board.boardRaw))
            
            row = int(arg // board.cols)
            col = arg % board.cols
            if board.can_putdown(row, col):
                return (row, col)
    
    def get_pos(self, board):
        pos = self.choose_action(board)
        arg = pos[0] * board.cols + pos[1]
        
        self.boards.append(board.boardRaw)
        action = torch.zeros(self.action_size, dtype=torch.float32)
        action[arg] = 1
        self.actions.append(action)

        return pos        
    
    def train(self, score):
        length = len(self.boards)
        for i in range(length):
            x = self.boards[i]
            action = self.actions[length - i - 1]

            x = self.preprocessX(self.boards[i])
            y = action * score
            score *= self.discount_factor

            self.model.train()
            self.optimizer.zero_grad()
            predict = self.target_model(x)
            predict = torch.multiply(predict, action)

            predict = predict.reshape((1, len(predict)))
            y = y.reshape((1, len(y)))

            loss = self.loss_func(predict, y)
            loss.backward()
            self.optimizer.step()
        
        self.update_target_model()
        self.boards.clear()
        self.actions.clear()
            
    def preprocessX(self, boardRaw):
        rows = len(boardRaw)
        cols = len(boardRaw[0])
        boardNum = np.zeros(rows * cols)
        for i in range(rows):
            for j in range(cols):
                if boardRaw[i][j] == self.color:
                    boardNum[i * cols + j] = 1
                elif not boardRaw[i][j] == '.':
                    boardNum[i * cols + j] = 2
        return torch.tensor(boardNum, dtype=torch.float32)





########################################
# input: board
# output: position (row, col)
# training: input -> action
#           loss: action_onehot - reward
#           reward: score * discount_factor
########################################