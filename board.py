import copy

class Board:

    def __init__(self):
        self.__black = 'B'
        self.__white = 'W'
        self.__blank = '.'

        self.rows = 15
        self.cols = 15
        self.boardRaw = [['.' for i in range(self.cols)] for j in range(self.rows)] # boardRaw[rows][cols]
        self.blank_cnt = self.rows * self.cols

    def check_win(self, pos, turn):
        row, col = pos
        if self.count_horizontal(row, col, turn) >=5 or self.count_vertical(row, col, turn) >= 5 or self.count_diagonal_LU(row, col, turn) >= 5 or self.count_diagonal_RU(row, col, turn) >= 5:
            return True
        else:
            return False
    
    def get_score(self, row, col, turn):
        return self.count_horizontal(row, col, turn) + self.count_vertical(row, col, turn) + self.count_diagonal_LU(row, col, turn) + self.count_diagonal_RU(row, col, turn)

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
        newBoardRaw = copy.deepcopy(self.boardRaw)
        return Board(newBoardRaw)
    
    def get_legal_pos(self):
        legal_list = []
        for i in range(self.rows):
            for j in range(self.rows):
                if self.boardRaw[i][j] == self.__blank:
                    legal_list.append((i, j))
        return legal_list
    
    def check_tie(self):
        return (self.blank_cnt == 0)