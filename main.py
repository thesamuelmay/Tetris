import pygame
import sys


pygame.init()


screen_width = 1200
screen_height = 800


white = (255, 255, 255)
black = (0, 0, 0)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

#Paddle and Ball settings
paddle_width = 25
paddle_height = 150
ball_size = 25


paddle_speed = 5
ball_speed_initial = 3


player1_score = 0
player2_score = 0


player1_paddle_y = (screen_height - paddle_height) // 2
player2_paddle_y = (screen_height - paddle_height) // 2

#Ball position
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed_x = ball_speed_initial
ball_speed_y = ball_speed_initial

#Score font
font = pygame.font.Font(None, 74)

#Render text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Function to reset the ball
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_speed_x *= -1  # Change ball direction
    ball_speed_y = ball_speed_initial

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_paddle_y > 0:
        player1_paddle_y -= paddle_speed
    if keys[pygame.K_s] and player1_paddle_y < screen_height - paddle_height:
        player1_paddle_y += paddle_speed
    if keys[pygame.K_UP] and player2_paddle_y > 0:
        player2_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and player2_paddle_y < screen_height - paddle_height:
        player2_paddle_y += paddle_speed

    #Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    #Ball collision with top and bottom
    if ball_y <= 0 or ball_y >= screen_height - ball_size:
        ball_speed_y *= -1

    #Ball collision with paddles
    if (ball_x <= paddle_width and player1_paddle_y < ball_y < player1_paddle_y + paddle_height) or \
       (ball_x >= screen_width - paddle_width - ball_size and player2_paddle_y < ball_y < player2_paddle_y + paddle_height):
        ball_speed_x *= -1

    #Scoring
    if ball_x < 3:
        player2_score += 1
        reset_ball()
    elif ball_x > screen_width:
        player1_score += 1
        reset_ball()

    #Display objects 
    screen.fill(black)
    pygame.draw.rect(screen, white, (0, player1_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (screen_width - paddle_width, player2_paddle_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, white, (ball_x, ball_y, ball_size, ball_size))

    #Display scores
    draw_text(str(player1_score), font, white, screen, 5, 5)
    draw_text(str(player2_score), font, white, screen, screen_width - 50, 5)

    pygame.display.update()

pygame.quit()
sys.exit()
