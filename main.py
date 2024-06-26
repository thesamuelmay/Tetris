import pygame
import random
from threading import Timer
from pygame import mixer

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
pygame.init()
pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30
score = 0
rowcheck = 0
White = (255,255,255)
Black = (0,0,0)
Grey = (105,105,105)
BG = (0,0,0)
fall_speed = 0.27
bag = []

touchdown = mixer.Sound('placed.wav')
remove = mixer.Sound('score.wav')
Gameoversound = mixer.Sound('GameOver.wav')


top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

win = pygame.display.set_mode((s_width, s_height))
# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape



# Define the path to your textures
texture_path = 'MAT2GUI/'  # Update this to the actual path

# Load textures
textures = {
    'S': pygame.image.load(texture_path + 'Green.png').convert(),
    'Z': pygame.image.load(texture_path + 'Red.png').convert(),
    'I': pygame.image.load(texture_path + 'Blue.png').convert(),
    'O': pygame.image.load(texture_path + 'Yellow.png').convert(),
    'J': pygame.image.load(texture_path + 'Purple.png').convert(),
    'L': pygame.image.load(texture_path + 'Orange.png').convert(),  # Change as necessary
    'T': pygame.image.load(texture_path + 'Aqua.png').convert()  # Change as necessary
}

class Piece(object):
    def __init__(self, column, row, shape, type):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        self.type = type  # Added type attribute





def get_shape():
    global shapes, shape_colors, bag
    
    # Check if bag is empty
    if not bag:
        bag = shapes[:]
        random.shuffle(bag)  # Shuffle Bag
    
   
    shape_types = {
        0: 'S',
        1: 'Z',
        2: 'I',
        3: 'O',
        4: 'J',
        5: 'L',
        6: 'T'
    }
    
    
    chosen_shape = bag.pop(0) #Remove piece from bag
    return Piece(5, 0, chosen_shape, shape_types[shapes.index(chosen_shape)])



def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False





def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

########
#SCORES CALCULATE HERE
########
def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
    global score
    global rowcheck
    global fall_speed
    
    

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            remove.play()
            
            # add positions to remove from locked
        
            
        

            

            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    

    touchdown.play()
    if inc == 4:
     scoremultiplyer = inc *4
    elif inc == 3:
        scoremultiplyer = inc*3
    elif inc == 2:
        scoremultiplyer = inc*2
    else:
        scoremultiplyer = inc
    score+= scoremultiplyer

    if inc != 0:
        speed_multi = score *0.002
        fall_speed =  0.27 - speed_multi
        print(fall_speed)
    print(inc) 

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    formatted = convert_shape_format(shape)

    for (x, y) in formatted:
        if shape.type in textures:
            texture = textures[shape.type]
            surface.blit(texture, (sx + (x-2) * block_size, sy + (y-4) * block_size))  # Adjust x, y for next shape display

def draw_score(surface, x, y):
    global score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, (255, 255, 255))
    surface.blit(label, (x, y))

def draw_piece(surface, grid, piece):
    formatted_shape = convert_shape_format(piece)

    for (x, y) in formatted_shape:
        if y > -1:  # If the y position is on the screen
            texture = textures[piece.type]
            # Transform grid position to pixel coordinates for blitting
            pixel_x = top_left_x + x * block_size
            pixel_y = top_left_y + y * block_size
            # Blit the texture instead of drawing a rectangle
            surface.blit(texture, (pixel_x, pixel_y))


def draw_window(surface,grid, current_piece, locked_positions):
    global score
    surface.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    draw_score(surface, 650, 250)

    draw_piece(surface, grid, current_piece)

    for (x, y), shape_type in locked_positions.items():
        if shape_type in textures:
            texture = textures[shape_type]
            pixel_x = top_left_x + x * block_size
            pixel_y = top_left_y + y * block_size
            surface.blit(texture, (pixel_x, pixel_y))
    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()

def timeout():
    change_piece = True

def main():
    global run
    global grid
    global change_piece
    global score
    global fall_speed
    

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0


    


    move_delay = 100  # Delay in milliseconds for a repeat movement
    quick_drop_speed = 50  # Delay in milliseconds for quick drop

    last_move_sideways_time = pygame.time.get_ticks()  # Time when the last move was made sideways
    last_quick_drop_time = pygame.time.get_ticks()  # Tim   

    # Quick drop variables
    quick_drop = False
    

    while run:
        

        
        
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

        
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.display.quit()
                    quit()
                if event.key == pygame.K_w:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    print(convert_shape_format(current_piece))  # todo fix

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a] and pygame.time.get_ticks() - last_move_sideways_time > move_delay:
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1
            last_move_sideways_time = pygame.time.get_ticks()

        if keys_pressed[pygame.K_d] and pygame.time.get_ticks() - last_move_sideways_time > move_delay:
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1
            last_move_sideways_time = pygame.time.get_ticks()

        if keys_pressed[pygame.K_s] and pygame.time.get_ticks() - last_quick_drop_time > quick_drop_speed:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
            last_quick_drop_time = pygame.time.get_ticks()

        shape_pos = convert_shape_format(current_piece)
        formatted = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        
        
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # Store the shape type in locked_positions instead of color
                locked_positions[p] = current_piece.type
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(win, grid, current_piece,locked_positions)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            draw_text_middle("You Lost", 40, (255,255,255), win)
            Gameoversound.play()
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            main_menu()

    pygame.display.flip()
    pygame.display.update()




def main_menu():
    global run
    global score
    run = False
    score = 0
    print(run)
    Main_open = True
    imgX=200
    imgY=40
    PlayB = pygame.image.load(texture_path+ 'Play.png').convert()
    MenuButtonDefultSize = (imgX, imgY)
    PlayB = pygame.transform.scale(PlayB, MenuButtonDefultSize)
    button = pygame.rect.Rect(s_width/2-75,350,imgX,imgY)
    BG = (0,0,0)
    def draw_bg():
        win.fill(BG)

    while Main_open:
        win.fill((BG))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Closed")
                Main_open = False
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    print('hi')
                    Main_open = False
                    run = True
                    main()
    
        a,b = pygame.mouse.get_pos()
        if button.x <= a <= button.x +imgX and button.y <= b <= button.y + imgY:
            win.blit(PlayB, (s_width/2-(imgX/2),350))
        else:
            win.blit(PlayB, (s_width/2-(imgX/2),350))
        pygame.display.flip()
        pygame.display.update()  
       # pygame.quit()


pygame.display.set_caption('Tetristhingy')

main_menu()  # start game