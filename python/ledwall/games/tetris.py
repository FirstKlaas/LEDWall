import random

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5


S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

BLANK = '.'

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

PIECES_COLOR = {'S': (255,  0,  0),
                'Z': (255,255,  0),
                'I': (  0,255,  0),
                'J': (  0,255,255),
                'L': (255,  0,255),
                'O': (  0,  0,255),
                'T': (255,255,255),
                BLANK : (0,0,0),
                }

PIECES_ORDER = {'S': 0,'Z': 1,'I': 2,'J': 3,'L': 4,'O': 5,'T': 6}

class Tetris(object):

    def __init__(self, display):
        self._display = display
        self._currentPiece = self.getNewPiece()
        self._matrix = [[BLANK for x in range(display.columns)] for y in range(display.rows)]
        self._falling_speed = 0.1

    @property
    def matrix(self):
        return self._matrix

    @property
    def width(self):
        return self._display.columns

    @property
    def height(self):
        return self._display.rows    
    
    def fallDown(self):
        if self._currentPiece is None:
            return False
        #TODO: Wie ist das Verhaeltnis von Frame Nummer und FrameRate zu Zeit und Geschwindigkeit?


    def checkForCollision(self, piece):
        shapeToTest = self.getShape(piece)
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shapeToTest[y][x] != BLANK and self.matrix[x][y] != BLANK:
                    return True
        return False
    
    def isRowComplete(self, row):
        for x in range(TEMPLATEWIDTH):
            if self.matrix[x][row] == BLANK:
                return False
        return True

    def getShape(self, piece):
        return PIECES[piece['shape']][piece['rotation']]

    def writePieceToMatrix(self, piece):
        shape = self.getShape(piece)
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shape[y][x] != BLANK:
                    self.matrix[x][y] = piece['shape']
                
    def writeMatrixToDisplay(self):
        for x in range(self.width):
            for y in range(self.height):
                shape = self.matrix[x][y]
                self._display.setPixel(x,y, PIECES_COLOR[shape])

    def getNewPiece(self):
        # return a random new piece in a random rotation and color
        shape = random.choice(list(PIECES.keys()))
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(PIECES[shape]) - 1),
                    'x': int(self.width / 2) - int(TEMPLATEWIDTH / 2),
                    'y': 1, # start it above the board (i.e. less than 0)
                    'color': PIECES_COLOR.get(shape)}
        return newPiece

    def copyRow(self, src, dst):
        for x in range(self.width):
            self.matrix[x][dst] = self.matrix[x][src]

    def drawPiece(self,piece, pixelx=None, pixely=None):
        shapeToDraw = self.getShape(piece)
        if pixelx == None and pixely == None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx=piece['x']
            pixely=piece['y']

        # draw each of the boxes that make up the piece
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shapeToDraw[y][x] != BLANK:
                    self._display.setPixel( pixelx+ x , pixely+y,piece['color'])
