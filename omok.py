import pygame
from pygame.locals import *
from board import Board

# cordinate: (y, x) = (row, col)

class Game:
    def __init__(self):
        self.turn = 'B'
        self.board = Board()
        self.colors = {'B': (0, 0, 0), 'W': (255, 255, 255)}
        self.backgroundColor = (255, 255, 255)

        self.boxSize = (40, 40) # (height, width)
        self.boardSize = (self.boxSize[0] * (self.board.rows - 2), self.boxSize[1] * (self.board.cols - 2)) # height, width / you can putdown at the endline of boardbox
        self.boardZeroPoint = (50, 50)    # (y, x) / the point of board's zero point in window coordinate
        self.windowSize = (self.boardSize[0] + 2 * self.boardZeroPoint[0], self.boardSize[1] + 2 * self.boardZeroPoint[1]) # (height, width)
        
        self.screen = None
        self.gameEnd = False
        self.gameWin = False
    
    def drawBoard(self):
        for i in range(self.board.rows):
            # pygame.draw.line(screen, color(R,G,B), start[x,y], end[x,y], brushwidth)
            pygame.draw.line(self.screen, self.colors['B'], [self.boardZeroPoint[1], self.boardZeroPoint[0] + i * self.boxSize[0]], [self.boardZeroPoint[1] + self.boardSize[1], self.boardZeroPoint[0] + i * self.boxSize[0]], 1)
        for j in range(self.board.cols):
            pygame.draw.line(self.screen, self.colors['B'], [self.boardZeroPoint[1] + j * self.boxSize[1], self.boardZeroPoint[0]], [self.boardZeroPoint[1] + j * self.boxSize[1], self.boardZeroPoint[0] + self.boardSize[0]], 1)


    def turnover(self):
        if self.turn == 'B':
            self.turn = 'W'
        elif self.turn == 'W':
            self.turn = 'B'
        else:
            raise Exception("turnover Error: Now Turn =", self.turn)
    
    def windowpos_to_boardpos(self, pos):
        return (int((pos[0] - self.boardZeroPoint[0] + self.boxSize[0] / 2) / self.boxSize[0]), int((pos[1] - self.boardZeroPoint[1] + self.boxSize[1] / 2) / self.boxSize[1]))
    
    def boardpos_to_windowpos(self, pos):
        return (self.boardZeroPoint[0] + self.boxSize[0] * pos[0], self.boardZeroPoint[1] + self.boxSize[1] * pos[1])
    
    def draw_circle(self, pos):
        windowpoint = self.boardpos_to_windowpos(pos)
        windowpoint_xy = (windowpoint[1], windowpoint[0])   # pygame.draw.circle's point should be (x, y)
        if self.turn == 'B':
            pygame.draw.circle(self.screen, self.colors['B'], windowpoint_xy, 10)
        elif self.turn == 'W':
            pygame.draw.circle(self.screen, self.colors['B'], windowpoint_xy, 10, 2)
        else:
            raise Exception("draw_circle Error: self.turn is not either 'B' or 'W'. Now Turn =", self.turn)
    
    def put_down(self, pos):    # pos = (row, col) on board
        if self.board.putdown(pos[0], pos[1], self.turn):
            self.draw_circle(pos)
            self.gameWin = self.board.check_win(pos[0], pos[1], self.turn)
            if not self.gameWin:
                self.turnover()
        else:
            print("You cannot put down there. Please Retry")

    def start(self):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption("Omok")
        self.screen = pygame.display.set_mode((self.windowSize[1], self.windowSize[0])) # set_mode((width, height))
        self.screen.fill(self.backgroundColor)
        
        self.drawBoard()

        while not (self.gameEnd or self.gameWin):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()    # (x, y)
                    pos = self.windowpos_to_boardpos((mousepos[1], mousepos[0]))
                    self.put_down(pos)
                    
                elif event.type == pygame.QUIT:
                    self.gameEnd = True
            
            pygame.display.flip()   # draw screen


        if self.gameEnd:
            print("Game END")
        elif self.gameWin:
            if self.turn == 'B':
                print("BLACK Win!!")
            else:
                print("WHITE Win!!")
        pygame.quit()
    
if __name__ == "__main__":
    game = Game()
    game.start()