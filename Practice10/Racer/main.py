import pygame
import random


pygame.init()


WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
YELLOW = (255, 220, 0)


clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)


player_width = 50
player_height = 90

player_x = 225
player_y = 560

player_speed = 7


enemy_width = 50
enemy_height = 90

enemy_x = random.randint(120, 330)
enemy_y = -100

enemy_speed = 5


coin_radius = 12

coin_x = random.randint(120, 380)
coin_y = -300

coin_speed = 5


coins = 0


game_over = False
running = True



while running:

    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and game_over:

                player_x = 225
                enemy_y = -100
                coin_y = -300

                coins = 0
                game_over = False

    
    keys = pygame.key.get_pressed()

    if not game_over:

        
        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        
        if player_x < 105:
            player_x = 105

        if player_x > 345:
            player_x = 345

        
        enemy_y += enemy_speed

        
        if enemy_y > HEIGHT:

            enemy_y = -100
            enemy_x = random.randint(120, 330)

        
        coin_y += coin_speed

        
        if coin_y > HEIGHT:

            coin_y = -100
            coin_x = random.randint(120, 380)

        
        player_rect = pygame.Rect(
            player_x,
            player_y,
            player_width,
            player_height
        )

        
        enemy_rect = pygame.Rect(
            enemy_x,
            enemy_y,
            enemy_width,
            enemy_height
        )

        
        coin_rect = pygame.Rect(
            coin_x - coin_radius,
            coin_y - coin_radius,
            coin_radius * 2,
            coin_radius * 2
        )

        
        if player_rect.colliderect(enemy_rect):

            game_over = True

        
        if player_rect.colliderect(coin_rect):

            coins += 1

            
            coin_y = -100
            coin_x = random.randint(120, 380)

    
    screen.fill(GREEN)

   
    pygame.draw.rect(
        screen,
        GRAY,
        (80, 0, 340, HEIGHT)
    )

    
    for y in range(0, HEIGHT, 100):

        pygame.draw.rect(
            screen,
            WHITE,
            (245, y, 10, 50)
        )

    
    pygame.draw.rect(
        screen,
        RED,
        (player_x, player_y, player_width, player_height)
    )

    
    pygame.draw.rect(
        screen,
        BLACK,
        (enemy_x, enemy_y, enemy_width, enemy_height)
    )

    
    if not game_over:

        pygame.draw.circle(
            screen,
            YELLOW,
            (coin_x, coin_y),
            coin_radius
        )

    
    coin_text = font.render(
        "Coins: " + str(coins),
        True,
        WHITE
    )

    screen.blit(coin_text, (330, 20))

    
    if game_over:

        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            WHITE
        )

        screen.blit(text, (100, 300))
        screen.blit(restart_text, (130, 370))

    
    pygame.display.flip()

    
    clock.tick(60)



pygame.quit()