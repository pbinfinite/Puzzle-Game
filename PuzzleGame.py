import sys
import random
import pygame,os,copy,time,datetime

print("\nWelcome !")
intro='''The sliding game is a puzzle which is set in a grid.An image is shuffled and has to be rearranged by the player in the correct order.

In our game you can select the level,the topic,or can be set in a custom grid.'''
print(intro)

s='''Select a topic and enter the respective number:
1.Fruits
2.Cartoon
3.Harry Potter
4.Numbers ( If you select this as the topic,note that you can't have a custom level!)'''

print(s)
n=int(input())

lev='''Which level:
1.Easy
2.Medium
3.Master
4.Custom'''
print(lev)
level1=int(input())

#The image selection part
if n==1:
    IMAGE_FILE=r'fruit.jpg'
elif n==2:
    IMAGE_FILE=r'dduck800_600.jpg'
elif n==3:
    IMAGE_FILE=r'hogwarts_train.jpg'
elif n==4 and level1==1:
    IMAGE_FILE=r'slide-3x3.jpg'
elif n==4 and level1==2:
    IMAGE_FILE=r'slide-4x4.jpg'
elif n==4 and level1==3:
    IMAGE_FILE=r'slide-5x5.jpg'
else:
    print("Enter a valid number")
    


if level1==1:
    COLUMNS=3
    ROWS=3
elif level1==2:
    COLUMNS=4
    ROWS=4
elif level1==3:
    COLUMNS=5
    ROWS=5
elif level1==4:
    print("Enter the grid size: Number of columns followed by number of rows")
    COLUMNS=int(input("No of columns:"))
    ROWS=int(input("No of rows:"))
else:
    print("Enter valid level")



BOARDSIZE=(700,700)
IMAGE_SIZE = (540,540)# Is size of image
TILE_WIDTH = 540//COLUMNS# width of each tile
TILE_HEIGHT = 540//ROWS# height of each tile


# bottom right corner contains no tile
EMPTY_TILE = (COLUMNS-1, ROWS-1)   

BLACK = (0, 0, 0)

# horizontal and vertical borders for D_TILES  (these borders are 1 px Thick)
hor_border = pygame.Surface((TILE_WIDTH, 1))
hor_border.fill(BLACK)
ver_border = pygame.Surface((1, TILE_HEIGHT))
ver_border.fill(BLACK)

#Loads img to screen and to divide
image = pygame.image.load(IMAGE_FILE)
D_TILES = {}
for c in range(COLUMNS) :
    for r in range(ROWS) :
        tile = image.subsurface (c*TILE_WIDTH, r*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT) # create subsurfaces from image.Each tile is a subsurface
        D_TILES [(c, r)] = tile
        if (c, r) != EMPTY_TILE:
            tile.blit(hor_border, (0, 0))       # copying all borders to the tile surface 
            tile.blit(hor_border, (0, TILE_HEIGHT-1))   #blit():blit(whatever to copy, position)
            tile.blit(ver_border, (0, 0))
            tile.blit(ver_border, (TILE_WIDTH-1, 0))
            # make the corners a bit rounded
            tile.set_at((1, 1), BLACK)  #set_at() sets the color for a single pixel         
            tile.set_at((1, TILE_HEIGHT-2), BLACK)
            tile.set_at((TILE_WIDTH-2, 1), BLACK)
            tile.set_at((TILE_WIDTH-2, TILE_HEIGHT-2), BLACK)
D_TILES[EMPTY_TILE].fill(BLACK)

# keep track of which tile is in which position
state = {(col, row): (col, row) for col in range(COLUMNS) for row in range(ROWS)}

# keep track of the position of the empty tile
(emptyc, emptyr) = EMPTY_TILE

# start game and display the completed puzzle(initial screen)
pygame.init()
display = pygame.display.set_mode(BOARDSIZE)
pygame.display.set_caption("Sliding Puzzle Game")

yellow=(255,255,0)
display.fill(yellow)
display.blit (image, (0, 0))
    
pygame.display.flip()   # flip updates and copies entire screen(all surfaces)

# swap a tile (c, r) with the neighbouring (emptyc, emptyr) tile
def shift (c, r) :
    global emptyc, emptyr 
    display.blit(D_TILES[state[(c, r)]],(emptyc*TILE_WIDTH, emptyr*TILE_HEIGHT))
    display.blit(D_TILES[EMPTY_TILE],(c*TILE_WIDTH, r*TILE_HEIGHT))
    state[(emptyc, emptyr)] = state[(c, r)]    #where (emptyc,emptyr) was old pos of empty tile. (c,r) is the position swapped with.
    state[(c, r)] = EMPTY_TILE
    (emptyc, emptyr) = (c, r)
    pygame.display.flip()


# shuffle the puzzle by making some random shift moves
def shuffle() :
    global emptyc, emptyr
    # keep track of last shuffling direction to avoid "undo" shuffle moves
    last_move = 0 
    for i in range(75):
        # slow down shuffling for visual effect
        pygame.time.delay(50)
        while True:                                 # pick a random direction and make a shuffling move
            move = random.randint(1, 4)             # if that is possible in that direction
            if (last_move + move == 5):   #their sum will be 5 only if the prev move and current move isnt same.
                continue                  # don't undo the last shuffling move          
            if move == 1 and (emptyc > 0):  # if tile at first place, cant move left or right
                shift(emptyc - 1, emptyr)   # shift left
            elif move == 4 and (emptyc < COLUMNS - 1):
                shift(emptyc + 1, emptyr)   # shift right
            elif move == 2 and (emptyr > 0):
                shift(emptyc, emptyr - 1)   # shift up
            elif move == 3 and (emptyr < ROWS - 1):
                shift(emptyc, emptyr + 1)   # shift down
            else:
                 continue                   # the random shuffle move didn't fit in that direction  
            last_move=move
            break                           # a shuffling move was made

# process mouse clicks 
at_start = True
showing_solution = False
while True:
    event = pygame.event.wait()      #waits till event of user input
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN :  #mousebuttondown :checks if mouse key is pressed
        if at_start:
            shuffle()                       # shuffle after the first mouse click
            at_start = False
        elif event.dict['button'] == 1:             #get_pos()returns the X and Y position of the mouse cursor. The position is
            mouse_pos = pygame.mouse.get_pos()                                        #relative the the top-left corner of the display. The cursor position
                                                    #can be located outside of the display window, but is always constrained to the screen.   
                                                      
            c = mouse_pos[0] // TILE_WIDTH  #x coord of cursor
            r = mouse_pos[1] // TILE_HEIGHT  #y coord 
            if ((abs(c-emptyc) == 1 and r == emptyr) or (abs(r-emptyr) == 1 and c == emptyc)):       #checks if dirn of move is valid(abs(c-emptyc) == 1 (1 because its the border width
                shift (c, r)                                                                            #abs = absolute value (modulus)
        
        
        elif event.dict['button'] == 3:
            saved_image = display.copy()
            display.blit(image, (0, 0))
            pygame.display.flip()
            showing_solution = True
    elif showing_solution and (event.type == pygame.MOUSEBUTTONUP):    #mousebuttonup= mouse released
        display.blit (saved_image, (0, 0))                          # stop showing the solution
        pygame.display.flip()
        showing_solution = False


pygame.display.update()






