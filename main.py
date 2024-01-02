import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load sound effects
eat_sound = pygame.mixer.Sound("eat.wav")  # Replace with your sound file
game_over_sound = pygame.mixer.Sound("gameover.mp3")  # Replace with your sound file

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Snake initial position and movement
snake = [(WIDTH // 2, HEIGHT // 2)]
dx, dy = CELL_SIZE, 0

# Food initial position
food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
        random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

clock = pygame.time.Clock()

score = 0
font = pygame.font.SysFont(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def game_over():
    screen.fill(BLACK)
    draw_text("Game Over! Your score was: {}".format(score), RED, WIDTH // 4, HEIGHT // 2)
    draw_text("Click anywhere to play again", WHITE, WIDTH // 5, HEIGHT // 2 + 50)
    pygame.display.flip()
    game_over_sound.play()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
                reset_game()

def reset_game():
    global snake, dx, dy, food, score
    snake = [(WIDTH // 2, HEIGHT // 2)]
    dx, dy = CELL_SIZE, 0
    food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    score = 0

def generate_shades_of_green(index, length):
    # Generate shades of green based on the index and length of the snake
    green_value = 255 - int(200 * (index / length))
    return (0, green_value, 0)

# Initial game start
running = True
game_started = False
while running:
    screen.fill(BLACK)
    if not game_started:
        draw_text("Snake Game", WHITE, WIDTH // 4, HEIGHT // 2)
        draw_text("Click anywhere to start", WHITE, WIDTH // 5, HEIGHT // 2 + 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_started = True

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL_SIZE
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL_SIZE, 0

        # Move the snake
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        snake.insert(0, new_head)

        # Check collision with food
        if snake[0] == food:
            food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                    random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
            score += 1
            eat_sound.play()  # Play eat sound
        else:
            snake.pop()

        # Check for collision with walls or itself
        if (snake[0][0] >= WIDTH or snake[0][0] < 0 or
            snake[0][1] >= HEIGHT or snake[0][1] < 0 or
            snake[0] in snake[1:]):
            game_over()

        # Draw the snake with shades of green
        snake_length = len(snake)
        for i, segment in enumerate(snake):
            color = generate_shades_of_green(i, snake_length)
            pygame.draw.rect(screen, color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Draw the food
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Display score
        draw_text("Score: {}".format(score), WHITE, 10, 10)

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()