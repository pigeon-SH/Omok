import copy

INFINITY = 100000000

class Minimax:
    def __init__(self, rows, cols, color):
        self.rows = rows
        self.cols = cols
        self.__blank = '.'

        self.my = color
        self.maxdepth = 1

        if self.my == 'B':
            self.enemy = 'W'
        else:
            self.enemy = 'B'

    def actions(self, state):
        return state.actions()
    
    def utility(self, state):
        return state.get_score(self.my)
    
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

####################################################################################################################

class AlphaBeta:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.__blank = '.'

        self.maxdepth = 1

    def actions(self, state):
        return state.actions()
    
    def utility(self, state):
        return state.get_score()
    
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
        if state.blank_cnt >= self.rows * self.cols - 1:
            return (5, 5)
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
        print("select spot:", spot, "score:", score)
        return spot

####################################################################################################################
