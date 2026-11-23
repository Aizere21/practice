import pygame
from player import MusicPlayer


pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

clock = pygame.time.Clock()

player = MusicPlayer()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.previous_track()

            elif event.key == pygame.K_q:
                running = False

    screen.fill((30, 30, 30))

    title = font.render("MUSIC PLAYER", True, (255, 255, 255))
    screen.blit(title, (200, 50))

    track_name = player.get_track_name()
    track_text = small_font.render(
        "Current track: " + track_name,
        True,
        (255, 255, 255)
    )
    screen.blit(track_text, (150, 130))

    position, duration = player.get_progress()

    progress_text = small_font.render(
        f"Time: {position} / {duration} seconds",
        True,
        (255, 255, 255)
    )
    screen.blit(progress_text, (170, 180))

    pygame.draw.rect(screen, (100, 100, 100), (100, 240, 400, 15))

    if duration > 0:
        progress_width = int(400 * position / duration)
        progress_width = min(progress_width, 400)

        pygame.draw.rect(
            screen,
            (0, 200, 100),
            (100, 240, progress_width, 15)
        )

    controls = small_font.render(
        "P - Play | S - Stop | N - Next | B - Previous | Q - Quit",
        True,
        (255, 255, 255)
    )
    screen.blit(controls, (35, 320))

    pygame.display.flip()

    clock.tick(30)


pygame.mixer.music.stop()
pygame.quit()