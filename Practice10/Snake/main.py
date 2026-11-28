import pygame
import random


pygame.init()


WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


CELL_SIZE = 20


clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)


snake = [
    [100, 100],
    [80, 100],
    [60, 100]
]


dx = CELL_SIZE
dy = 0


score = 0
level = 1
speed = 10


game_over = False
running = True



def generate_food():

    while True:

        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        food = [x, y]

        
        if food not in snake:
            return food


food = generate_food()



while running:

    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN and not game_over:

            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -CELL_SIZE

            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = CELL_SIZE

            elif event.key == pygame.K_LEFT and dx == 0:
                dx = -CELL_SIZE
                dy = 0

            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = CELL_SIZE
                dy = 0

        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and game_over:

                snake = [
                    [100, 100],
                    [80, 100],
                    [60, 100]
                ]

                dx = CELL_SIZE
                dy = 0

                score = 0
                level = 1
                speed = 10

                food = generate_food()

                game_over = False

    if not game_over:

        
        new_head = [
            snake[0][0] + dx,
            snake[0][1] + dy
        ]

        
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):

            game_over = True

        else:

            
            eating = new_head == food

            
            body = snake if eating else snake[:-1]

            if new_head in body:

                game_over = True

            else:

                
                snake.insert(0, new_head)

                
                if eating:

                    score += 1

                    
                    new_level = score // 3 + 1

                    if new_level > level:

                        level = new_level
                        speed += 2

                    
                    food = generate_food()

                else:

                    
                    snake.pop()

    
    screen.fill(BLACK)

    
    for part in snake:

        pygame.draw.rect(
            screen,
            GREEN,
            (part[0], part[1], CELL_SIZE, CELL_SIZE)
        )

    
    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
    )

    
    score_text = font.render(
        "Score: " + str(score),
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))

    
    level_text = font.render(
        "Level: " + str(level),
        True,
        WHITE
    )

    screen.blit(level_text, (10, 40))

    
    if game_over:

        game_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            WHITE
        )

        screen.blit(game_text, (150, 250))
        screen.blit(restart_text, (190, 320))

   
    pygame.display.flip()

    
    clock.tick(speed)



pygame.quit()