import copy

INFINITY = 100000000

class State:
    def __init__(self, board, rows, cols, blank_cnt, blanks):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.blank_cnt = blank_cnt
        self.blanks = blanks
        self.__blank=  '.'

        self.terminal = False
        self.winner = None
    
    def actions(self):
        return self.blanks
    
    def player(self):
        if (self.rows * self.cols - self.blank_cnt) % 2 == 0:
            return 'B'
        else:
            return 'W'

    def result(self, act):
        # For Debug
        if self.board[act[0]][act[1]] != self.__blank:
            print("You cannot act:", act)
            return
        
        player = self.player()
        self.board[act[0]][act[1]] = player
        self.blank_cnt -= 1
        self.blanks.remove(act)
        self.check_terminal(act)
    
    def undo(self, act):
        # For Debug
        if self.board[act[0]][act[1]] == self.__blank:
            print("You cannot act:", act)
            return
        
        self.board[act[0]][act[1]] = self.__blank
        self.blank_cnt += 1
        self.blanks.append(act)

        if self.terminal:
            self.terminal = False
            self.winner = ''

    def check_terminal(self, act):
        player = self.board[act[0]][act[1]] # check terminal would execute after do act
        # check Horizontal
        cnt = 0
        row = act[0]
        start = max(act[1] - 4, 0)
        end = min(act[1] + 5, self.cols)
        for j in range(start, end):
            if self.board[row][j] == player:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.terminal = True
                self.winner = player
                return
        
        # check Vertical
        cnt = 0
        col = act[1]
        start = max(act[0] - 4, 0)
        end = min(act[0] + 5, self.rows)
        for i in range(start, end):
            if self.board[i][col] == player:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.terminal = True
                self.winner = player
                return
        
        # check Diagonal from Left Top
        cnt = 0
        dist_left = min(4, act[0], act[1])
        dist_right = min(4, self.rows - act[0] - 1, self.cols - act[1] - 1)
        start = (act[0] - dist_left, act[1] - dist_left)
        for i in range(dist_left + dist_right + 1):
            if self.board[start[0] + i][start[1] + i] == player:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.terminal = True
                self.winner = player
                return
        
        # check Diagonal from Left Down
        cnt = 0
        dist_left = min(4, self.rows - act[0] - 1, act[1])
        dist_right = min(4, act[0], self.cols - act[1] - 1)
        start = (act[0] + dist_left, act[1] - dist_left)
        for i in range(dist_left + dist_right + 1):
            if self.board[start[0] - i][start[1] + i] == player:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.terminal = True
                self.winner = player
                return
        
        if self.blank_cnt == 0:
            self.terminal = True
            self.winner = 'Tie'

class Minimax:
    def __init__(self, rows, cols, color):
        self.rows = rows
        self.cols = cols
        self.__blank = '.'

        self.my = color
        self.maxdepth = 1

    # if prediction is too slow, use the method that in youtube
    # do move, pass the state to next Agent, remove the move
    def actions(self, state):
        return state.actions()
    
    def utility(self, state):
        if state.winner == self.my:
            return 10
        elif state.winner == '':
            return 0
        else:
            return -10
    
    def maxAgent(self, state, depth):
        if depth >= self.maxdepth or state.terminal:
            return self.utility(state)
        
        v = -INFINITY
        actions = state.actions()
        for act in actions:
            state.result(act)
            v = max(v, self.minAgent(state, depth + 1))
            state.undo(act)
        
        return v
    
    def minAgent(self, state, depth):
        if depth >= self.maxdepth or state.terminal:
            return self.utility(state)
        
        v = INFINITY
        actions = state.actions()
        for act in actions:
            state.result(act)
            v = min(v, self.maxAgent(state, depth + 1))
            state.undo(act)
        
        return v
    
    def get_spot(self, state):
        v = -INFINITY
        spot = None

        actions = state.actions()
        for act in actions:
            state.result(act)
            score = self.minAgent(state, 0)
            if score > v:
                v = score
                spot = act
            state.undo(act)
        
        return spot

class AlphaBeta:
    def __init__(self, rows, cols, color):
        self.rows = rows
        self.cols = cols
        self.__blank = '.'

        self.my = color
        self.maxdepth = 3

    # if prediction is too slow, use the method that in youtube
    # do move, pass the state to next Agent, remove the move
    def actions(self, state):
        return state.actions()
    
    def utility(self, state):
        if state.winner == self.my:
            return 10
        elif state.winner == '':
            return 0
        else:
            return -10
    
    def maxAgent(self, state, depth, alpha, beta):
        if depth >= self.maxdepth or state.terminal:
            return self.utility(state)
        
        v = -INFINITY
        actions = state.actions()
        for act in actions:
            state.result(act)
            v = max(v, self.minAgent(state, depth + 1, alpha, beta))
            state.undo(act)
            if v > alpha:
                alpha = v
                if alpha >= beta:
                    break

        return v
    
    def minAgent(self, state, depth, alpha, beta):
        if depth >= self.maxdepth or state.terminal:
            return self.utility(state)
        
        v = INFINITY
        actions = state.actions()
        for act in actions:
            state.result(act)
            v = min(v, self.maxAgent(state, depth + 1, alpha, beta))
            state.undo(act)
            if v < beta:
                beta = v
                if beta <= alpha:
                    break
        
        return v
    
    def get_spot(self, state):
        v = -INFINITY
        spot = None
        alpha = -INFINITY
        beta = INFINITY

        actions = state.actions()
        for act in actions:
            state.result(act)
            score = self.minAgent(state, 0, alpha, beta)
            if score > v:
                v = score
                spot = act
            state.undo(act)
            if v > alpha:
                alpha = v
                if alpha >= beta:
                    break
        
        return spot
