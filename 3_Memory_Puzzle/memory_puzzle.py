import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOW_WDITH = 800
WINDOW_HEIGHT = 800
REVEAL_SPEED = int(1280*0.0135) # Speed boxes' sliding reveals and covers
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
GAP_SIZE = 10 # Size of gap between boxes

BOX_WIDTH = int((WINDOW_WDITH - (GAP_SIZE*(BOARD_WIDTH+1))) / BOARD_WIDTH) # Size of box height/width
BOX_HEIGHT = int((WINDOW_HEIGHT - (GAP_SIZE*(BOARD_HEIGHT+1))) / BOARD_HEIGHT)



assert (BOARD_WIDTH*BOARD_HEIGHT) % 2 == 0, 'Board needs to have a total number of even boxes to make pairs'

X_MARGIN = int((WINDOW_WDITH - (BOARD_WIDTH * (BOX_WIDTH + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_HEIGHT + GAP_SIZE))) / 2)

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
HIGHLIGHT_COLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, OVAL, LINES)

assert len(ALL_COLORS)*len(ALL_SHAPES)*2 >= BOARD_HEIGHT * BOARD_WIDTH, 'Board size is too big for the number of shapes/colors'

pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(loops=-1, start=0)

def main():
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WDITH, WINDOW_HEIGHT))

    # Mouse event coordinates
    mouse_x = 0 
    mouse_y = 0
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # (x,y) of first box clicked

    DISPLAY_SURF.fill(BG_COLOR)
    startGameAnimation(mainBoard)
    
    while True:
        pygame.mixer.music.unpause()
        mouseClicked = False

        DISPLAY_SURF.fill(BG_COLOR)
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
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, box_x, box_y)
                    
                    # If icons don't match
                    if icon1shape!=icon2shape or icon1color!=icon2color:
                        bad_guess = pygame.mixer.Channel(0).set_volume(3)
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("bad_guess.mp3"), loops=0)
                        # Cover up both selections
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (box_x, box_y)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[box_x][box_y] = False

                    else:
                        # Check if all the pairs have been found
                        if hasWon(revealedBoxes):
                            pygame.mixer.music.pause()
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound("win.mp3"), loops=2)
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(1500)
                            # Reset the board
                            pygame.mixer.music.unpause()
                            pygame.mixer.music.play(loops=-1, start=0)
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)
                            # Show the fully unrevealed box for a second
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)
                            # Replay the start game animation
                            startGameAnimation(mainBoard)                            
                        else:
                            pygame.mixer.Channel(0).set_volume(0.3)
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound("good_guess.mp3"), loops=0)
                    
                    # Reset the first selection variable
                    firstSelection = None
        
        # Redraw the screen and wait a clock tick
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


# Function definitions
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARD_WIDTH):
        revealedBoxes.append([val] * BOARD_HEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    # Get a list of every shape in every possible color
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((shape, color))
    # Randomize the order of icons list
    random.shuffle(icons) 
    # Calculate how many icons are needed
    numIconsUsed = int(BOARD_WIDTH * BOARD_HEIGHT / 2)
    icons = icons[:numIconsUsed] * 2 # Get two of each to make pairs
    random.shuffle(icons)
    # Create board data structure, with randomly placed icons
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for i in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0] # Delete the icons as we assign the,
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    # Splits a list into a list of lists, where the inner lists have at most groupSize number of items
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i+groupSize])
    return result

def leftTopCoordsOfBox(box_x, box_y):
    left = box_x * (BOX_WIDTH + GAP_SIZE) + X_MARGIN
    top = box_y * (BOX_HEIGHT + GAP_SIZE) + Y_MARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for box_x in range(BOARD_WIDTH):
        for box_y in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(box_x, box_y)
            boxRect = pygame.Rect(left, top, BOX_WIDTH, BOX_HEIGHT)
            if boxRect.collidepoint(x, y):
                return (box_x, box_y)
    # Return None if there is no box at (x, y)
    return (None, None)

def drawIcon(shape, color, box_x, box_y):    
    quarter_width = int(BOX_WIDTH * 0.25)
    half_width = int(BOX_WIDTH * 0.5)
    quarter_height = int(BOX_HEIGHT * 0.25)
    half_height = int(BOX_HEIGHT * 0.5)
    left, top = leftTopCoordsOfBox(box_x, box_y)
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAY_SURF, color, (left+half_width, top+half_height), min(half_width,half_height)-5)
        pygame.draw.circle(DISPLAY_SURF, BG_COLOR, (left+half_width, top+half_height), min(quarter_width,quarter_height)-5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY_SURF, color, (left+quarter_width, top+quarter_height, BOX_WIDTH-half_width, BOX_HEIGHT-half_height))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY_SURF, color, ((left+half_width, top), (left+BOX_WIDTH-1, top+half_height), (left+half_width, top+BOX_HEIGHT-1), (left, top+half_height)))
    elif shape == LINES:        
        for i in range(int(BOX_WIDTH/4), int(BOX_WIDTH*3/4), 5):
            pygame.draw.line(DISPLAY_SURF, color, (left+i,top+int(BOX_HEIGHT/4)), (left+i, top+int(BOX_HEIGHT*3/4)))
        for i in range(int(BOX_HEIGHT/4), int(BOX_HEIGHT*3/4), 5):
            pygame.draw.line(DISPLAY_SURF, color, (left+int(BOX_WIDTH/4), top+i), (left+int(BOX_WIDTH*3/4), top+i)) 
        pygame.draw.line(DISPLAY_SURF, color, (left+int(BOX_WIDTH*3/4), top+int(BOX_HEIGHT/4)), (left+int(BOX_WIDTH*3/4), top+int(BOX_HEIGHT*3/4)))
        pygame.draw.line(DISPLAY_SURF, color, (left+int(BOX_WIDTH/4), top+int(BOX_HEIGHT*3/4)), (left+int(BOX_WIDTH*3/4), top+int(BOX_HEIGHT*3/4)))            
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY_SURF, color, (left, top+quarter_height, BOX_WIDTH, half_height))

def getShapeAndColor(board, box_x, box_y):
    # Shape value for x,y spot is stored in board[x][y][0]
    # Color value for x,y spot is stored in board[x][y][0]
    return board[box_x][box_y][0], board[box_x][box_y][1]

def drawBoxCovers(board, boxes, coverage):
    # Draw boxes being covered/revealed;  'boxes' is a list of two-item lists,
    # which have the x,y spot of the box
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (left, top, BOX_WIDTH, BOX_HEIGHT))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        # Only draw the ocver if there is a coverage
        if coverage > 0: 
            pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left, top, coverage, BOX_HEIGHT))
    pygame.display.update()
    FPS_CLOCK.tick(FPS)

def revealedBoxesAnimation(board, boxesToReveal):
    # Do the 'box reveal' animation
    for coverage in range (BOX_WIDTH, (-REVEAL_SPEED)-1, -REVEAL_SPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    # Do the 'box cover' animation
    for coverage in range(0, BOX_WIDTH+REVEAL_SPEED, REVEAL_SPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    # Draw all the boxes in their covered/revealed state
    for box_x in range(BOARD_WIDTH):
        for box_y in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(box_x, box_y)
            if not revealed[box_x][box_y]:
                # Draw covered box
                pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left, top, BOX_WIDTH, BOX_HEIGHT))
            else:
                # Draw the revealed shape/color
                shape, color = getShapeAndColor(board, box_x, box_y)
                drawIcon(shape, color, box_x, box_y)

def drawHighlightBox(box_x, box_y):
    left, top = leftTopCoordsOfBox(box_x, box_y)
    pygame.draw.rect(DISPLAY_SURF, HIGHLIGHT_COLOR, (left-5, top-5, BOX_WIDTH+10, BOX_HEIGHT+10), 4)

def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append((x, y))

    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealedBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    # Flash the background color
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHT_BG_COLOR
    color2 = BG_COLOR

    for i in range (13):
        color1, color2 = color2, color1 # Swap the colors
        DISPLAY_SURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # Return False if an boxes are covered
    return True

if __name__ == '__main__':
    main()
