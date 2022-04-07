import random

def block_shape(sidx, ridx):
    block_color = [(0, 255, 255),   # Sky
                   (255, 165, 0),   # Orange
                   (128, 0, 128),   # Purple
                   (255, 255, 0),   # Yello
                   (0, 0, 255),     # Blue 
                   (0, 255, 0),     # Green
                   (255, 0, 0)]     # Red

    block_shape=[       # 1:Shape 1:Rotate
        [['..1...',    # I
          '..1..',
          '..1..',
          '..1..',
          '.....'],
         ['.....',
          '1111.'
          '.....',
          '.....',
          '.....']],
        [['.....',      # L-1
          '..1..',
          '..1..',
          '..11.',
          '.....'],
         ['.....',
          '...1.',
          '.111.',
          '.....',
          '.....'],
         ['.....',
          '.11..',
          '..1..',
          '..1..',
          '.....'],
         ['.....',
          '.111.',
          '.1...',
          '.....',
          '.....']],
        [['.....',      # T-1
          '..1..',
          '.11..',
          '..1..',
          '.....'],
         ['.....',
          '.111.',
          '..1..',
          '.....',
          '.....'],
         ['.....',
          '..1..',
          '..11.',
          '..1..',
          '.....'],
         ['.....',      
          '..1..',
          '.111.',
          '.....',
          '.....']],
        [['.....',     # square
          '.11..',
          '.11..',
          '.....',
          '.....']],
        [['.....',      # L-2
          '..1..',
          '..1..',
          '.11..',
          '.....'],
         ['.....',
          '.111.',
          '...1.',
          '.....',
          '.....'],
         ['.....',
          '..11.',
          '..1..',
          '..1..',
          '.....'],
         ['.....',
          '.1...',
          '.111.',
          '.....',
          '.....']],
        [['.....',       # S-1
          '..11.',
          '.11..',
          '.....',
          '.....'],
         ['.....',
          '..1..',
          '..11.',
          '...1.',
          '.....']],
        [['.....',       # S-2
          '.11..',
          '..11.',
          '.....',
          '.....'],
         ['.....',
          '..1..',
          '.11..',
          '.1...',
          '.....']]]
    
    max_rotate = len(block_shape[sidx])
    return block_color[sidx], max_rotate, block_shape[sidx][ridx]


class Block(object):
    def __init__(self):
        self.row = 0    # y position
        self.col = 0    # x position
        self.rsize = 20
        self.csize = 20
        self.shape = random.randint(0,6)
        self.rotate = 0
        self.color, self.max_rotate, self.block_shape = block_shape(self.shape, self.rotate)
        self.coord = self.to_coordinate()
        self.move_to_zero()

    def rotation(self, dir=1):
        self.rotate = (self.rotate + dir) % self.max_rotate
        self.color, self.max_rotate, self.block_shape = block_shape(self.shape, self.rotate)
        self.coord = self.to_coordinate()
        self.convert_shape()
        self.move_to_zero()

    def set_rowcol(self, row, col):
        self.row = row
        self.col = col

    def convert_shape(self):
        self.block_shape = block_shape(self.shape, self.rotate)

    def to_coordinate(self):
        coordinate = []
        for ridx, rowline in enumerate(self.block_shape):
            line = list(rowline)
            for cidx, col in enumerate(line):
                if col == '1':
                    coordinate.append((ridx, cidx))
        return coordinate

    def move_to_zero(self):
        minr = min(self.coord, key=lambda k:k[0])[0]
        minc = min(self.coord, key=lambda k:k[1])[1]
        zero_base = []
        for r, c in self.coord:
            zero_base.append((r-minr, c-minc))

        return zero_base