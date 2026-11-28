import pygame
import random

pygame.init()


WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)


BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)


snake = [[300, 300], [280, 300], [260, 300]]
direction = "RIGHT"

score = 0
speed = 10


food_x = 100
food_y = 100
food_value = 1
food_color = RED

FOOD_TIME = 5
food_timer = pygame.time.get_ticks()


def create_food():
    global food_x, food_y, food_value, food_color, food_timer

    while True:
        food_x = random.randrange(0, WIDTH, CELL_SIZE)
        food_y = random.randrange(0, HEIGHT, CELL_SIZE)

        
        if [food_x, food_y] not in snake:
            break

    
    food_type = random.choice([1, 2, 3])

    if food_type == 1:
        food_value = 1
        food_color = RED
    elif food_type == 2:
        food_value = 2
        food_color = ORANGE
    else:
        food_value = 5
        food_color = YELLOW

    
    food_timer = pygame.time.get_ticks()


running = True
game_over = False

create_food()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"

            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"

            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"

            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

            
            elif event.key == pygame.K_r and game_over:
                snake = [[300, 300], [280, 300], [260, 300]]
                direction = "RIGHT"
                score = 0
                speed = 10
                game_over = False
                create_food()

    if not game_over:

        
        head_x, head_y = snake[0]

        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = [head_x, head_y]

        
        snake.insert(0, new_head)

        
        if head_x == food_x and head_y == food_y:
            score += food_value
            create_food()
        else:
            snake.pop()

        
        if (head_x < 0 or head_x >= WIDTH or
                head_y < 0 or head_y >= HEIGHT):
            game_over = True

        
        if new_head in snake[1:]:
            game_over = True

        
        current_time = pygame.time.get_ticks()

        if current_time - food_timer > FOOD_TIME * 1000:
            create_food()

    
    screen.fill(BLACK)

    
    for part in snake:
        pygame.draw.rect(
            screen, GREEN,
            (part[0], part[1], CELL_SIZE, CELL_SIZE)
        )

    
    pygame.draw.rect(
        screen, food_color,
        (food_x, food_y, CELL_SIZE, CELL_SIZE)
    )


    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    
    if not game_over:
        elapsed = (pygame.time.get_ticks() - food_timer) // 1000
        remaining = max(0, FOOD_TIME - elapsed)

        timer_text = font.render(
            "Food time: " + str(remaining), True, WHITE
        )
        screen.blit(timer_text, (400, 10))

    if game_over:
        text = font.render("GAME OVER - Press R", True, WHITE)
        screen.blit(text, (150, 280))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()