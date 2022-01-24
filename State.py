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
        #return self.score
        return self.get_score_entire()

        
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
    
    def get_score_entire(self):
        score = 0
        if self.mine == 'B':
            alpha = 1
        else:
            alpha = -1
        
        row_data = [''.join(self.board[i, :]) for i in range(self.rows)]
        col_data = [''.join(self.board[:, i]) for i in range(self.cols)]
        diag_data = []
        for i in range(self.rows - 4):
            data = ''
            for j in range(self.cols - i):
                data += self.board[i + j][j]
            diag_data.append(data)
        for i in range(1, self.cols - 4):
            data = ''
            for j in range(self.rows - i):
                data += self.board[j][i + j]
            diag_data.append(data)
        for i in range(4, self.rows):
            data = ''
            for j in range(i + 1):
                data += self.board[i - j][j]
            diag_data.append(data)
        for i in range(1, self.cols - 4):
            data = ''
            for j in range(self.rows - i):
                data += self.board[self.rows - 1 - j][i + j]
            diag_data.append(data)

        line_data = row_data + col_data + diag_data
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
        return score