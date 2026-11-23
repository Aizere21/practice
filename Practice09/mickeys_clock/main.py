import sys

import pygame

from clock import MickeyClock

WIDTH, HEIGHT = 700, 750
FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    fps_clock = pygame.time.Clock()

    clock = MickeyClock(center=(WIDTH // 2, 340), radius=300)

    running = True
    while running:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        
        screen.fill((200, 230, 255))
        clock.draw(screen)
        pygame.display.flip()

        
        fps_clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
