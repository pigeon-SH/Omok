import copy

INFINITY = 100000000

class State:
    def __init__(self, board, rows, cols, blank_cnt, blanks, mine):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.blank_cnt = blank_cnt
        self.blanks = blanks
        self.__blank=  '.'

        self.terminal = False
        self.winner = None
        self.score = 0
        self.score_change_stack = []
        self.mine = mine
    
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
        self.update_score(act)
        self.check_terminal(act)
    
    def undo(self, act):
        # For Debug
        if self.board[act[0]][act[1]] == self.__blank:
            print("You cannot undo:", act)
            return
        
        self.board[act[0]][act[1]] = self.__blank
        self.blank_cnt += 1
        self.blanks.append(act)

        if self.terminal:
            self.terminal = False
            self.winner = ''
        
        self.score -= self.score_change_stack[-1]
        self.score_change_stack.pop(-1)
    
    def update_score(self, spot):
        score = 0
        if self.mine == 'B':
            alpha = 1
        else:
            alpha = -1
        
        row_start = max(spot[0] - 4, 0)
        row_end = min(spot[0] + 5, self.rows)
        col_start = max(spot[1] - 4, 0)
        col_end = min(spot[1] + 5, self.cols)
        row_data = ''.join(self.board[row_start : row_end, spot[1]])
        col_data = ''.join(self.board[spot[0], col_start : col_end])

        diag_lu_data = ''.join([self.board[spot[0] + k][spot[1] + k] for k in range(-4, 5) if spot[0] + k >= 0 and spot[0] + k < self.rows and spot[1] + k >= 0 and spot[1] + k < self.cols])
        diag_ld_data = ''.join([self.board[spot[0] - k][spot[1] + k] for k in range(-4, 5) if spot[0] - k >= 0 and spot[0] - k < self.rows and spot[1] + k >= 0 and spot[1] + k < self.cols])
        line_data = [row_data, col_data, diag_ld_data, diag_lu_data]
        line_data.append
        for data in line_data:
            if data.find('BBBBB') > 0 or data.find('.BBBB.') > 0:
                score += 10000 * alpha
            if data.find('WBBBB.') > 0 or data.find('.BBBBW') > 0 or data.find('.BBB.') > 0:
                score += 1000 * alpha
            if data.find('.BBB.B.') > 0 or data.find('.B.BBB.') > 0:
                score += 800 * alpha
            if data.find('.BB.BB.') > 0:
                score += 500 * alpha
            if data.find('WBBB.B.') > 0 or data.find('.BBB.BW') > 0 or data.find('WB.BBB.') > 0 or data.find('.B.BBBW') > 0:
                score += 300 * alpha
            if data.find('WBB.BB.') > 0 or data.find('.BB.BBW') > 0:
                score += 300 * alpha
            if data.find('WBB.BBW') > 0:
                score += 300 * alpha
            if data.find('.BB.B.') > 0 or data.find('.B.BB.') > 0:
                score += 300 * alpha
            if data.find('.BB.') > 0:
                score += 200 * alpha
            if data.find('WBB.B.') > 0 or data.find('.BB.BW') > 0 or data.find('WB.BB.') > 0 or data.find('.B.BBW') > 0:
                score += 100 * alpha
            if data.find('WBB.') > 0 or data.find('.BBW') > 0:
                score += 10 * alpha
            
            alpha *= -1
            if data.find('WWWWW') > 0 or data.find('.WWWW.') > 0:
                score += 10000 * alpha
            if data.find('BWWWW.') > 0 or data.find('.WWWWB') > 0 or data.find('.WWW.') > 0:
                score += 1000 * alpha
            if data.find('.WWW.W.') > 0 or data.find('.W.WWW.') > 0:
                score += 800 * alpha
            if data.find('.WW.WW.') > 0:
                score += 500 * alpha
            if data.find('BWWW.W.') > 0 or data.find('.WWW.WB') > 0 or data.find('BW.WWW.') > 0 or data.find('.W.WWWB') > 0:
                score += 300 * alpha
            if data.find('BWW.WW.') > 0 or data.find('.WW.WWB') > 0:
                score += 300 * alpha
            if data.find('BWW.WWB') > 0:
                score += 300 * alpha
            if data.find('.WW.W.') > 0 or data.find('.W.WW.') > 0:
                score += 300 * alpha
            if data.find('.WW.') > 0:
                score += 200 * alpha
            if data.find('BWW.W.') > 0 or data.find('.WW.WB') > 0 or data.find('BW.WW.') > 0 or data.find('.W.WWB') > 0:
                score += 100 * alpha
            if data.find('BWW.') > 0 or data.find('.WWB') > 0:
                score += 10 * alpha

        self.score += score
        self.score_change_stack.append(score)
        return score
    
    def get_score(self):
        return self.score

        
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

class AlphaBeta:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.__blank = '.'

        self.maxdepth = 2

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
