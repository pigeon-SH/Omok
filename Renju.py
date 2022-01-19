import pygame
from AI import *
import copy

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player:
    def __init__(self, color, isAI):
        self.isAI = isAI
        if isAI:
            self.AI = AlphaBeta(15, 15, color)

class Game:
    def __init__(self):
        self.player = {'B': Player('B', isAI=False), 'W': Player('W', isAI=True)}
        self.turn = 'B'

        self.rows = 15
        self.cols = 15
        self.board = [['.' for i in range(self.cols)] for j in range(self.rows)]
        self.blank_cnt=  self.cols * self.rows
        #self.blanks = [[i, j] for i in range(self.rows) for j in range(self.cols)]

        self.gameEnd = False
        self.result = ''

        self.screen_size = (600, 600)   # (width, height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.margin = 20

        self.box_size = ((self.screen_size[0] - self.margin * 2) / (self.cols - 1), (self.screen_size[1] - self.margin * 2) / (self.rows - 1)) # (width, height)

        self.radius = 10
        self.line_width = 2

    def nextTurn(self):
        if self.turn == 'B':
            self.turn = 'W'
        else:
            self.turn = 'B'
    
    def checkResult(self, spot):
        # spot: last spot

        # check Horizontal
        cnt = 0
        row = spot[0]
        start = max(spot[1] - 4, 0)
        end = min(spot[1] + 5, self.cols)
        for j in range(start, end):
            if self.board[row][j] == self.turn:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.gameEnd = True
                self.result = "winner: " + self.turn
                return
        
        # check Vertical
        cnt = 0
        col = spot[1]
        start = max(spot[0] - 4, 0)
        end = min(spot[0] + 5, self.rows)
        for i in range(start, end):
            if self.board[i][col] == self.turn:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.gameEnd = True
                self.result = "winner: " + self.turn
                return
        
        # check Diagonal from Left Top
        cnt = 0
        dist_left = min(4, spot[0], spot[1])
        dist_right = min(4, self.rows - spot[0] - 1, self.cols - spot[1] - 1)
        start = (spot[0] - dist_left, spot[1] - dist_left)
        for i in range(dist_left + dist_right + 1):
            if self.board[start[0] + i][start[1] + i] == self.turn:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.gameEnd = True
                self.result = "winner: " + self.turn
                return
        
        # check Diagonal from Left Down
        cnt = 0
        dist_left = min(4, self.rows - spot[0] - 1, spot[1])
        dist_right = min(4, spot[0], self.cols - spot[1] - 1)
        start = (spot[0] + dist_left, spot[1] - dist_left)
        for i in range(dist_left + dist_right + 1):
            if self.board[start[0] - i][start[1] + i] == self.turn:
                cnt += 1
            elif cnt > 0:
                cnt = 0
            if cnt >= 5:
                self.gameEnd = True
                self.result = "winner: " + self.turn
                return
        
        if self.blank_cnt == 0:
            self.gameEnd = True
            self.result = "Game Tie"
    
    def putdown(self, spot):
        r, c = spot
        if self.board[r][c] == '.':
            self.board[r][c] = self.turn
            self.draw(spot, self.turn)
            self.blank_cnt -= 1
            return True
        else:
            print("Cannot putdown at", spot)
            return False
    
    def get_blanks(self):
        blanks = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == '.':
                    blanks.append((i, j))
        return blanks
    
    def get_spot(self):
        # AI Player
        if self.player[self.turn].isAI:
            state = State(copy.deepcopy(self.board), self.rows, self.cols, self.blank_cnt, self.get_blanks())
            spot = self.player[self.turn].AI.get_spot(state)
            return spot
        
        # Human Player
        else:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        point = pygame.mouse.get_pos()
                        board_point = self.winToboard(point)
                        return board_point

                    elif event.type == pygame.QUIT:
                        self.gameEnd = True
                        self.result = 'Quit'
                        return None

    def winToboard(self, winpos):
        # winpos: (x, y)
        # boardpos: (row, col)
        row = int((winpos[1] - self.margin + self.box_size[1] / 2) / self.box_size[1])
        col = int((winpos[0] - self.margin + self.box_size[0] / 2) / self.box_size[0])
        return (row, col)
    
    def drawBoard(self):
        # start and end points of line are (x, y)
        # Draw Horizontal
        for i in range(self.rows):
            start_point = (self.margin, self.margin + self.box_size[1] * i)
            end_point = (self.screen_size[0] - self.margin, self.margin + self.box_size[1] * i)
            pygame.draw.line(self.screen, BLACK, start_point, end_point)
        
        # Draw Vertical
        for i in range(self.cols):
            start_point = (self.margin + self.box_size[0] * i, self.margin)
            end_point = (self.margin + self.box_size[0] * i, self.screen_size[1] - self.margin)
            pygame.draw.line(self.screen, BLACK, start_point, end_point)
    
    def draw(self, spot, color):
        x = spot[1] * self.box_size[0] + self.margin
        y = spot[0] * self.box_size[1] + self.margin
        if color == 'B':
            pygame.draw.circle(self.screen, BLACK, (x, y), self.radius)
        else:
            pygame.draw.circle(self.screen, BLACK, (x, y), self.radius, self.line_width)

    def start(self):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption("Renju")
        self.screen.fill(WHITE)

        self.drawBoard()

        while not self.gameEnd:
            pygame.display.flip()

            spot = self.get_spot()
            while spot and not self.putdown(spot):
                spot = self.get_spot()
            
            if spot:
                self.checkResult(spot)
                self.nextTurn()
        
        print(self.result)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.start()