#TODO
#If there's no where to putdown but game is not Win-state

import pygame
from newAgent import Agent
from board import Board

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR = {'B': BLACK, 'W': WHITE}

class Game:
    def __init__(self):
        self.player = None
        self.turn = 'B' # start turn: B
        self.board = Board()
        self.backgroundColor = WHITE

        self.boxSize = (40, 40) # (Height, Width)
        self.boardSize = (self.boxSize[0] * (self.board.rows - 1), self.boxSize[1] * (self.board.cols - 1))
        self.margin = (50, 50)
        self.windowSize = (self.boardSize[0] + self.margin[0] * 2, self.boardSize[1] + self.margin[1] * 2)
        self.radius = 10

        self.screen = None
        self.gameQuit = False
        self.gameWin = False
        self.gameTie = False
        
    def setPlayers(self):
        # set players
        print("AI: Enter A / Player: Enter P")
        player_B = input("Black Player:")
        player_W = input("White Player:")
        self.player = {'B': Agent('B', (player_B == 'A')), 'W': Agent('W', (player_W == 'A'))}
    
    def drawBoard(self):
        endpoint = [self.margin[0] + self.boxSize[0] * (self.board.rows - 1), self.margin[1] + self.boxSize[1] * (self.board.cols - 1)]
        # draw horizontal lines
        for i in range(self.board.rows):
            pygame.draw.line(self.screen, BLACK, (self.margin[0] + self.boxSize[0] * i, self.margin[1]), (self.margin[0] + self.boxSize[0] * i, endpoint[1]))
        # draw vertical lines
        for i in range(self.board.cols):
            pygame.draw.line(self.screen, BLACK, (self.margin[0], self.margin[1] + self.boxSize[1] * i), (endpoint[0], self.margin[1] + self.boxSize[1] * i))
    
    def turnover(self):
        if self.turn == 'B':
            self.turn = 'W'
        else:
            self.turn = 'B'
    
    def put_down(self, windowpos, boardpos):
        if self.board.check_tie():
            self.gameTie = True
            return
        if self.board.putdown(boardpos, self.turn): #if can putdown
            pygame.draw.circle(self.screen, COLOR[self.turn], windowpos, self.radius)
            if self.board.check_win(boardpos, self.turn):
                self.gameWin = True
                return
            self.turnover()
        else:
            print("You cannot put down here.")
            #else: not turnover
    
    def window_to_board(self, windowpos):
        boardpos = (int((windowpos[0] - self.margin[0] + self.boxSize[0] / 2) // self.boxSize[0]), int((windowpos[1] - self.margin[1] + self.boxSize[1] / 2) / self.boxSize[1]))
        return boardpos
    def board_to_window(self, boardpos):
        windowpos = ((boardpos[0] * self.boxSize[0] + self.margin[0], boardpos[1] * self.boxSize[1] + self.margin[1]))
        return windowpos

    def get_pos(self):
        if self.player[self.turn].isAI:
            boardpos = self.player[self.turn].get_pos(self.board)
            windowpos = self.board_to_window(boardpos)
            return windowpos, boardpos
        else:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        windowpos = pygame.mouse.get_pos()
                        boardpos = self.window_to_board(windowpos)
                        windowpos = self.board_to_window(boardpos)
                        return windowpos, boardpos
                    elif event.type == pygame.QUIT:
                        self.gameQuit = True
                        pygame.quit
                        return None, None

    
    def start(self):
        self.setPlayers()
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption("Omok")
        self.screen = pygame.display.set_mode((self.windowSize[1], self.windowSize[0])) # set_mode((width, height))
        self.screen.fill(self.backgroundColor)

        self.drawBoard()

        while not(self.gameWin or self.gameQuit or self.gameTie):
            pygame.display.flip()   # draw screen
            winpos, boardpos = self.get_pos()
            if winpos != None:
                self.put_down(winpos, boardpos)
        
        if self.gameWin:
            print(self.turn, "is Win!!")
        elif self.gameQuit:
            print("Game Quit")
        elif self.gameTie:
            print("Tie game")

if __name__ == "__main__":
    game = Game()
    game.start()