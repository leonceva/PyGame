import imp
import random, pygame, sys
from tkinter.tix import DisplayStyle
from pygame.locals import *

FPS = 30
WINDOW_WDITH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8 # Speed boxes' sliding reveals and covers
BOX_SIZE = 40 # Size of box height/width
GAP_SIZE = 10 # Size of gap between boxes
BOARD_WIDTH = 10
BOARD_HEIGHT = 7

assert (BOARD_WIDTH*BOARD_HEIGHT) % 2 == 0, 'Board needs to have a total number of even boxes to make pairs'

X_MARGIN = int((WINDOW_WDITH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

GRAY        = (100, 100, 100)		
NAVY_BLUE   = ( 60,  60, 100)		
WHITE       = (255, 255, 255)		
RED         = (255,   0,   0)		
GREEN       = (  0, 255,   0)		
BLUE        = (  0,   0, 255)		
YELLOW      = (255, 255,   0)		
ORANGE      = (255, 128,   0)		
PURPLE      = (255,   0, 255)		
CYAN        = (  0, 255, 255)

BG_COLOR = NAVY_BLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALL_COLORS) * len(ALL_SHAPES) >= BOARD_HEIGHT * BOARD_WIDTH, 'Board size is too big for the number of shapes/colors'

def main():
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPPLAY_SURF = pygame.display.set_mode((WINDOW_WDITH, WINDOW_HEIGHT))

    # Mouse event coordinates
    mouse_x = 0 
    mouse_y = 0

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # (x,y) of first box clicked

    DISPPLAY_SURF.fill(BG_COLOR)
    startGameAnimation(mainBoard)
    
    while True:
        mouseClicked = False

        DISPPLAY_SURF.fill(BG_COLOR)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == K_LALT and event.type == K_F4):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos

            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouseClicked = True

        box_x, box_y = getBoxAtPixel(mouse_x, mouse_y)

        # If mouse is on a box
        if box_x != None and box_y != None:
            # If box is not revealed
            if not revealedBoxes[box_x][box_y]:
                drawHighlightBox(box_x, box_y)
            # If box is not revealed and user clicked
            if not revealedBoxes[box_x][box_y] and mouseClicked:
                revealedBoxesAnimation(mainBoard, [(box_x, box_y)]) # Reveal animation
                revealedBoxes[box_x][box_y] = True # Set box as revealed
                # If first box selection
                if firstSelection == None:
                    firstSelection = (box_x, box_y)
                # If second box selection
                else:
                    # Check if matching boxes



