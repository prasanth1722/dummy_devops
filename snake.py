import pygame
import time
import random
import os

port = int(os.environ.get("PORT", 8080))  # Cloud Run sets $PORT

# Initialize pygame
pygame.init()

# Define window size
WIDTH = 600
HEIGHT = 400

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Snake block size
SNAKE_BLOCK = 10

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
SNAKE_SPEED = 15

# Define font
font = pygame.font.SysFont("bahnschrift", 25)

def message(msg, color, x, y):
    text = font.render(msg, True, color)
    screen.blit(text, [x, y])

def gameLoop():
    game_over = False
    game_close = False
    
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0
    
    snake_list = []
    length_of_snake = 1
    
    food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    
    while not game_over:
        while game_close:
            screen.fill(WHITE)
            message("Game Over! Press Q-Quit or C-Play Again", RED, WIDTH / 6, HEIGHT / 3)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_BLOCK
                    x_change = 0
        
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
        
        x += x_change
        y += y_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
        
        for segment in snake_list:
            pygame.draw.rect(screen, BLUE, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])
        
        pygame.display.update()
        
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1
        
        clock.tick(SNAKE_SPEED)
    
    pygame.quit()
    quit()

gameLoop()
