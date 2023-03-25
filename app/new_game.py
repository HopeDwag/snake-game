import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Falling Squares")

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.Font(None, 30)

# Set up the player
player_x = screen_width // 2
player_y = screen_height - 50
player_width = 50
player_height = 50
player_speed = 5

# Set up the square
square_x = random.randint(0, screen_width - player_width)
square_y = -50
square_width = 50
square_height = 50
square_speed = 5

# Set up the score
score = 0

# Main game loop
game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Move the square
    square_y += square_speed

    # Check for collision
    if player_x < square_x + square_width and player_x + player_width > square_x and \
       player_y < square_y + square_height and player_y + player_height > square_y:
        square_x = random.randint(0, screen_width - player_width)
        square_y = -50
        square_speed += 1
        score += 1

    # Draw the screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, (255, 0, 0), (square_x, square_y, square_width, square_height))
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Clean up
pygame.quit()