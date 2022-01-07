import random

class Agent:
    def __init__(self, color, isAI):
        # color='B' or 'W'
        # isAI=true or false
        self.color = color
        self.isAI = isAI
    
    def get_pos(self, board):
        candidates = board.get_legal_pos()
        idx = random.randrange(0, len(candidates))
        return candidates[idx]