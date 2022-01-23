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
            print("You cannot undo:", act)
            return
        
        self.board[act[0]][act[1]] = self.__blank
        self.blank_cnt += 1
        self.blanks.append(act)

        if self.terminal:
            self.terminal = False
            self.winner = ''
    
    def compute_score(self, data, ismine):
        open_cnt = 0
        if data[0] == self.__blank:
            open_cnt += 1
        if data[-1] == self.__blank:
            open_cnt += 1
        
        score = 0
        jump_idx = data[1:-1].find(self.__blank)
        if jump_idx < 0:            # no jump
            cnt = len(data) - 2
            if cnt >= 5:            # 오목, 육목
                score = 100000      # winscore
            elif cnt >= 4:
                if open_cnt >= 2:   # 열린사
                    score = 100000   # winscore
                elif open_cnt >= 1: # 닫힌사
                    score = 1000
            elif cnt >= 3:
                if open_cnt >= 2:   # 열린삼
                    score = 1000
                elif open_cnt >= 1: # 닫힌삼
                    score = 200
            elif cnt >= 2:
                if open_cnt >= 2:   # 열린이
                    score = 100
                elif open_cnt >= 1: # 닫힌이
                    score = 10
        else:
            cnt_before = jump_idx - 1
            cnt_after = len(data) - jump_idx - 2
            if (cnt_before == 3 and cnt_after == 1) or (cnt_before == 1 and cnt_after == 3):
                if open_cnt >= 2:   # 열린삼일
                    score = 800
                elif open_cnt >= 1: # 닫힌삼일
                    score = 300
            elif cnt_before == 2 and cnt_after == 2:
                if open_cnt >= 2:   # 열린이이
                    score = 500
                elif open_cnt >= 1: # 닫힌이이
                    score = 300
            elif (cnt_before == 2 and cnt_after == 1) or (cnt_before == 1 and cnt_after == 2):
                if open_cnt >= 2:   # 열린띈삼
                    score = 300
                elif open_cnt >= 1: # 닫힌띈삼
                    score = 100
            
        if ismine:
            return score
        else:
            return score * -1

    def get_score_one_line(self, mine, start, delta):
        score = 0
        data = 'E'  # stands for End
        now_color = None
        i, j = start
        while i >= 0 and i < self.rows and j >= 0 and j < self.cols:
            if self.board[i][j] != self.__blank:
                if now_color == None:
                    now_color = self.board[i][j]
                if now_color != self.board[i][j]:
                    data += self.board[i][j]
                    score += self.compute_score(data, now_color == mine)  # compute score
                    data = '' + self.board[i - delta[0]][j - delta[1]]
                    now_color=  self.board[i][j]

            elif data[-1] == self.__blank:  # 2 blanks in a row
                    score += self.compute_score(data, now_color == mine)  # compute score
                    data = ''
                    now_color = None
            
            data += self.board[i][j]
            i += delta[0]
            j += delta[1]
        
        return score

    def get_score(self, mine):
        score = 0
        
        for i in range(self.rows):  # Horizontal
            start = (i, 0)
            delta = (0, 1)
            score += self.get_score_one_line(mine, start, delta)
        for i in range(self.cols):  # Vertical
            start = (0, i)
            delta = (1, 0)
            score += self.get_score_one_line(mine, start, delta)
        
        for i in range(self.rows - 4):
            start = (i, 0)
            delta = (1, 1)
            score += self.get_score_one_line(mine, start, delta)
        for i in range(self.cols - 4):
            start = (0, i)
            delta = (1, 1)
            score += self.get_score_one_line(mine, start, delta)
        
        for i in range(4, self.rows):
            start = (i, 0)
            delta = (-1, 1)
            score += self.get_score_one_line(mine, start, delta)
        for i in range(self.cols - 4):
            start = (self.rows, i)
            delta = (-1, 1)
            score += self.get_score_one_line(mine, start, delta)
        
        return score

    """
    def getScore(self, color, enemy):
        score = 0

        # check Horizontal
        for i in range(self.rows):
            cnt_mine = 0
            cnt_enemy = 0
            for j in range(self.cols):
                if self.board[i][j] == color:
                    cnt_mine += 1
                    if cnt_enemy > 0:
                        if cnt_enemy >= 4:
                            score -= 1000
                        elif cnt_enemy >= 3:
                            score -= 100
                        cnt_enemy = 0
                elif self.board[i][j] == enemy:
                    cnt_enemy += 1
                    if cnt_mine > 0:
                        if cnt_mine >= 4:
                            score += 1000
                        elif cnt_mine >= 3:
                            score += 100
                        cnt_mine = 0
                
                if cnt_mine >= 5:
                    score += 10000
                    break
                
                if cnt_enemy >= 5:
                    score -= 10000
                    break
        
        #Debug
        print("Horizontal Score:", score)
        
        # check Vertical
        for j in range(self.cols):
            cnt_mine = 0
            cnt_enemy = 0
            for i in range(self.rows):
                if self.board[i][j] == color:
                    cnt_mine += 1
                    if cnt_enemy > 0:
                        if cnt_enemy >= 4:
                            score -= 1000
                        elif cnt_enemy >= 3:
                            score -= 100
                        cnt_enemy = 0
                elif self.board[i][j] == enemy:
                    cnt_enemy += 1
                    if cnt_mine > 0:
                        if cnt_mine >= 4:
                            score += 1000
                        elif cnt_mine >= 3:
                            score += 100
                        cnt_mine = 0
                
                if cnt_mine >= 5:
                    score += 10000
                    break
                
                if cnt_enemy >= 5:
                    score -= 10000
                    break
        
        #Debug
        print("Vertical Score:", score)
        
        # check Diagonal(From Left Up)
        for row in range(self.rows - 4):
            cnt_mine = 0
            cnt_enemy = 0
            for k in range(self.cols - row):
                if self.board[row + k][k] == color:
                    cnt_mine += 1
                    if cnt_enemy > 0:
                        if cnt_enemy >= 4:
                            score -= 1000
                        elif cnt_enemy >= 3:
                            score -= 100
                        cnt_enemy = 0
                elif self.board[row + k][k] == enemy:
                    cnt_enemy += 1
                    if cnt_mine > 0:
                        if cnt_mine >= 4:
                            score += 1000
                        elif cnt_mine >= 3:
                            score += 100
                        cnt_mine = 0
                
                if cnt_mine >= 5:
                    score += 10000
                    break
                
                if cnt_enemy >= 5:
                    score -= 10000
                    break

        for col in range(1, self.cols - 4):
            cnt_mine = 0
            cnt_enemy = 0
            for k in range(self.rows - col):
                if self.board[k][col + k] == color:
                    cnt_mine += 1
                    if cnt_enemy > 0:
                        if cnt_enemy >= 4:
                            score -= 1000
                        elif cnt_enemy >= 3:
                            score -= 100
                        cnt_enemy = 0
                if self.board[k][col + k] == enemy:
                    cnt_enemy += 1
                    if cnt_mine > 0:
                        if cnt_mine >= 4:
                            score += 1000
                        elif cnt_mine >= 3:
                            score += 100
                        cnt_mine = 0
                
                if cnt_mine >= 5:
                    score += 10000
                    break
                
                if cnt_enemy >= 5:
                    score -= 10000
                    break
        
        #Debug
        print("Diagonal Left Up Score:", score)
        
        # check Diagonal(From Left Down)
        for row in range(4, self.rows):
            cnt_mine = 0
            cnt_enemy = 0
            for k in range(row + 1):
                if self.board[row - k][k] == color: 
                    cnt_mine += 1
                    if cnt_enemy > 0:
                        if cnt_enemy >= 4:
                            score -= 1000
                        elif cnt_enemy >= 3:
                            score -= 100
                        cnt_enemy = 0
                elif self.board[row - k][k] == enemy:
                    cnt_enemy += 1
                    if cnt_mine > 0:
                        if cnt_mine >= 4:
                            score += 1000
                        elif cnt_mine >= 3:
                            score += 100
                        cnt_mine = 0
                
                if cnt_mine >= 5:
                    score += 10000
                    break
                
                if cnt_enemy >= 5:
                    score -= 10000
                    break

        for col in range(1, self.cols - 4):
            cnt_mine = 0
            cnt_enemy = 0
            for k in range(self.rows - col):
                if self.board[self.rows - k - 1][col + k] == color: 
                    cnt_mine += 1
                    if cnt_enemy > 0:
                        if cnt_enemy >= 4:
                            score -= 1000
                        elif cnt_enemy >= 3:
                            score -= 100
                        cnt_enemy = 0
                if self.board[self.rows - k - 1][col + k] == enemy: 
                    cnt_enemy += 1
                    if cnt_mine > 0:
                        if cnt_mine >= 4:
                            score += 1000
                        elif cnt_mine >= 3:
                            score += 100
                        cnt_mine = 0
                
                if cnt_mine >= 5:
                    score += 10000
                    break
                
                if cnt_enemy >= 5:
                    score -= 10000
                    break
        
        #Debug
        print("Diagonal Left Down Score:", score)
        
        return score
        """

        
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
    def __init__(self, rows, cols, color):
        self.rows = rows
        self.cols = cols
        self.__blank = '.'

        self.my = color
        self.maxdepth = 2

        if self.my == 'B':
            self.enemy = 'W'
        else:
            self.enemy = 'B'

    def actions(self, state):
        return state.actions()
    
    def utility(self, state):
        return state.get_score(self.my)
    
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
