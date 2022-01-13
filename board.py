import copy

class Board:
    def __init__(self):
        self.__black = 'B'
        self.__white = 'W'
        self.__blank = '.'

        self.rows = 15
        self.cols = 15
        self.boardRaw = [['.' for i in range(self.cols)] for j in range(self.rows)] # boardRaw[rows][cols]
        self.boardNum = [[0 for i in range(self.cols)] for j in range(self.rows)] # boardRaw[rows][cols]
        self.blank_cnt = self.rows * self.cols

    def check_win(self, pos, turn):
        row, col = pos
        if self.count_horizontal(row, col, turn) >=5 or self.count_vertical(row, col, turn) >= 5 or self.count_diagonal_LU(row, col, turn) >= 5 or self.count_diagonal_RU(row, col, turn) >= 5:
            return True
        else:
            return False
    
    def get_score(self, row, col, turn, enemy):
        ####################################################################
        #   TODO:                                                          #
        #   check win method: only have to check nearby of putdown         #
        #   get score method: have to check entire board                   #
        #       if my turn is black, check black weight and plus score     #
        #       if my turn is black, check white weight and minus score    #
        ####################################################################
        mycounts = []
        enemycounts = []
        mycounts.append(self.count_horizontal(row, col, turn))
        mycounts.append(self.count_vertical(row, col, turn))
        mycounts.append(self.count_diagonal_LU(row, col, turn))
        mycounts.append(self.count_diagonal_RU(row, col, turn))
        enemycounts.append(self.count_horizontal(row, col, enemy))
        enemycounts.append(self.count_vertical(row, col, enemy))
        enemycounts.append(self.count_diagonal_LU(row, col, enemy))
        enemycounts.append(self.count_diagonal_RU(row, col, enemy))

        score_sum = 0
        for cnt in mycounts:
            if cnt >= 5:
                score_sum += 100000
            elif cnt >= 4:
                score_sum += 10000
            elif cnt >= 3:
                score_sum += 1000
            else:
                score_sum += cnt
        for cnt in enemycounts:
            if cnt >= 5:
                score_sum += 50000
            elif cnt >= 4:
                score_sum += 5000
            elif cnt >= 3:
                score_sum += 500
            else:
                score_sum += cnt

        return score_sum

    def count_horizontal(self, row, col, turn):
        cnt = 1 # (x,y) is already == turn
        
        # check left
        i = col - 1
        while i >= 0:
            if self.boardRaw[row][i] == turn:
                cnt += 1
                i -= 1
            else:
                break
            if cnt >= 5:
                return cnt

        # check right
        i = col + 1
        while i < self.cols:
            if self.boardRaw[row][i] == turn:
                cnt += 1
                i += 1
            else:
                break
            if cnt >= 5:
                return cnt
        
        return cnt
        
    def count_vertical(self, row, col, turn):
        cnt = 1 # (row,col) is already == turn
        
        # check up
        i = row - 1
        while i >= 0:
            if self.boardRaw[i][col] == turn:
                cnt += 1
                i -= 1
            else:
                break
            if cnt >= 5:
                return cnt

        # check down
        i = row + 1
        while i < self.rows:
            if self.boardRaw[i][col] == turn:
                cnt += 1
                i += 1
            else:
                break
            if cnt >= 5:
                return cnt
        
        return cnt

    def count_diagonal_LU(self, row, col, turn):
        cnt = 1 # (x,y) is already == turn
        
        # check left up
        i = row - 1
        j = col - 1
        while i >= 0 and j >= 0:
            if self.boardRaw[i][j] == turn:
                cnt += 1
                i -= 1
                j -= 1
            else:
                break
            if cnt >= 5:
                return cnt

        # check right down
        i = row + 1
        j = col + 1
        while i < self.rows and j < self.cols:
            if self.boardRaw[i][j] == turn:
                cnt += 1
                i += 1
                j += 1
            else:
                break
            if cnt >= 5:
                return cnt
        
        return cnt
    
    def count_diagonal_RU(self, row, col, turn):
        cnt = 1 # (x,y) is already == turn
        
        # check right up
        i = row - 1
        j = col + 1
        while i >= 0 and j < self.cols:
            if self.boardRaw[i][j] == turn:
                cnt += 1
                i -= 1
                j += 1
            else:
                break
            if cnt >= 5:
                return cnt

        # check left down
        i = row + 1
        j = col - 1
        while i < self.rows and j >= 0:
            if self.boardRaw[i][j] == turn:
                cnt += 1
                i += 1
                j -= 1
            else:
                break
            if cnt >= 5:
                return cnt
        
        return cnt
    
    def can_putdown(self, row, col):
        return self.boardRaw[row][col] == self.__blank

    def putdown(self, pos, turn):
        row, col = pos
        if self.can_putdown(row, col):
            self.boardRaw[row][col] = turn
            self.blank_cnt -= 1
            return True
        else:
            return False
    
    def deepCopy(self):
        newBoard = Board()
        newBoard.boardRaw = copy.deepcopy(self.boardRaw)
        return newBoard
    
    def get_legal_pos(self):
        legal_list = []
        for i in range(self.rows):
            for j in range(self.rows):
                if self.boardRaw[i][j] == self.__blank:
                    legal_list.append((i, j))
        return legal_list
    
    def check_tie(self):
        return (self.blank_cnt == 0)

