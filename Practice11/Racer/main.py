import pygame
import random

pygame.init()


WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GOLD = (255, 200, 0)


player_x = 175
player_y = 480
player_width = 50
player_height = 80
player_speed = 5


enemy_x = random.randint(50, 300)
enemy_y = -100
enemy_speed = 4


coin_x = random.randint(50, 350)
coin_y = -300
coin_speed = 4
coin_value = 1

score = 0
COINS_TO_SPEED_UP = 10


def create_coin():
    global coin_x, coin_y, coin_value

    coin_x = random.randint(50, 350)
    coin_y = -30

    
    coin_type = random.choice([1, 2, 3])

    if coin_type == 1:
        coin_value = 1
    elif coin_type == 2:
        coin_value = 2
    else:
        coin_value = 5


running = True
game_over = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                player_x = 175
                enemy_y = -100
                enemy_speed = 4
                score = 0
                game_over = False
                create_coin()

    if not game_over:

        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        
        enemy_y += enemy_speed
        coin_y += coin_speed

        
        if enemy_y > HEIGHT:
            enemy_y = -100
            enemy_x = random.randint(50, 300)

        
        if coin_y > HEIGHT:
            create_coin()

        
        player_rect = pygame.Rect(
            player_x, player_y, player_width, player_height
        )

        enemy_rect = pygame.Rect(
            enemy_x, enemy_y, 50, 80
        )

        coin_rect = pygame.Rect(
            coin_x, coin_y, 25, 25
        )

        
        if player_rect.colliderect(enemy_rect):
            game_over = True

        
        if player_rect.colliderect(coin_rect):
            score += coin_value

            
            if score // COINS_TO_SPEED_UP > (score - coin_value) // COINS_TO_SPEED_UP:
                enemy_speed += 1

            create_coin()

    
    screen.fill(GRAY)

    
    pygame.draw.rect(screen, BLACK, (50, 0, 300, HEIGHT))

    
    for y in range(0, HEIGHT, 100):
        pygame.draw.rect(screen, WHITE, (195, y, 10, 50))

    
    pygame.draw.rect(
        screen, BLUE,
        (player_x, player_y, player_width, player_height)
    )

    
    pygame.draw.rect(
        screen, RED,
        (enemy_x, enemy_y, 50, 80)
    )

    
    if coin_value == 1:
        coin_color = YELLOW
    elif coin_value == 2:
        coin_color = ORANGE
    else:
        coin_color = GOLD

    pygame.draw.circle(screen, coin_color, (coin_x + 12, coin_y + 12), 12)

    
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        text = font.render("GAME OVER - Press R", True, WHITE)
        screen.blit(text, (45, 280))

    pygame.display.update()
    clock.tick(60)

pygame.quit()