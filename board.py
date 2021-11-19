class Board:

    def __init__(self):
        self.__black = 'B'
        self.__white = 'W'
        self.__blank = '.'

        self.rows = 20
        self.cols = 20
        self.boardRaw = [['.' for i in range(self.cols)] for j in range(self.rows)] # boardRaw[rows][cols]    

    def check_win(self, row, col, turn):
        if self.check_win_horizontal(row, col, turn) or self.check_win_vertical(row, col, turn) or self.check_win_diagonal(row, col, turn):
            return True
        else:
            return False

    def check_win_horizontal(self, row, col, turn):
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
                return True

        # check right
        i = col + 1
        while i < self.cols:
            if self.boardRaw[row][i] == turn:
                cnt += 1
                i += 1
            else:
                break
            if cnt >= 5:
                return True
        
        return False
        
    def check_win_vertical(self, row, col, turn):
        cnt = 1 # (x,y) is already == turn
        
        # check up
        i = row - 1
        while i >= 0:
            if self.boardRaw[i][col] == turn:
                cnt += 1
                i -= 1
            else:
                break
            if cnt >= 5:
                return True

        # check down
        i = row + 1
        while i < self.rows:
            if self.boardRaw[i][col] == turn:
                cnt += 1
                i += 1
            else:
                break
            if cnt >= 5:
                return True
        
        return False

    def check_win_diagonal(self, row, col, turn):
        cnt = 1 # (x,y) is already == turn
        
        # check left up
        i = row - 1
        j = col - 1
        while i >= 0:
            if self.boardRaw[i][j] == turn:
                cnt += 1
                i -= 1
                j -= 1
            else:
                break
            if cnt >= 5:
                return True

        # check right down
        i = row + 1
        j = col + 1
        while i < self.rows:
            if self.boardRaw[i][j] == turn:
                cnt += 1
                i += 1
                j += 1
            else:
                break
            if cnt >= 5:
                return True
        
        return False
    
    def can_putdown(self, row, col):
        return self.boardRaw[row][col] == self.__blank

    def putdown(self, row, col, turn):
        if self.can_putdown(row, col):
            self.boardRaw[row][col] = turn
            return True
        else:
            return False