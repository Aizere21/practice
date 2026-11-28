import pygame

pygame.init()


WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)


current_color = BLACK
current_shape = "PENCIL"

drawing = False
start_pos = None
end_pos = None

screen.fill(WHITE)


colors = [BLACK, RED, GREEN, BLUE, YELLOW, ORANGE]


shapes = [
    "PENCIL",
    "SQUARE",
    "RIGHT TRIANGLE",
    "EQUILATERAL TRIANGLE",
    "RHOMBUS",
    "CLEAR"
]

font = pygame.font.SysFont("Arial", 16)



def draw_square(surface, color, start, end):
    width = end[0] - start[0]
    height = end[1] - start[1]

    
    size = min(abs(width), abs(height))

    rect = pygame.Rect(start[0], start[1], size, size)
    pygame.draw.rect(surface, color, rect, 3)



def draw_right_triangle(surface, color, start, end):
    points = [
        start,
        (start[0], end[1]),
        end
    ]

    pygame.draw.polygon(surface, color, points, 3)



def draw_equilateral_triangle(surface, color, start, end):
    width = end[0] - start[0]
    height = int(abs(width) * 0.866)

    points = [
        (start[0] + width // 2, start[1]),
        (start[0], start[1] + height),
        (end[0], start[1] + height)
    ]

    pygame.draw.polygon(surface, color, points, 3)



def draw_rhombus(surface, color, start, end):
    middle_x = (start[0] + end[0]) // 2
    middle_y = (start[1] + end[1]) // 2

    points = [
        (middle_x, start[1]),
        (end[0], middle_y),
        (middle_x, end[1]),
        (start[0], middle_y)
    ]

    pygame.draw.polygon(surface, color, points, 3)


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            if y < 40:
                if x < 40:
                    current_color = BLACK
                elif x < 80:
                    current_color = RED
                elif x < 120:
                    current_color = GREEN
                elif x < 160:
                    current_color = BLUE
                elif x < 200:
                    current_color = YELLOW
                elif x < 240:
                    current_color = ORANGE

            
            elif y < 80:
                if x < 100:
                    current_shape = "PENCIL"
                elif x < 200:
                    current_shape = "SQUARE"
                elif x < 350:
                    current_shape = "RIGHT TRIANGLE"
                elif x < 550:
                    current_shape = "EQUILATERAL TRIANGLE"
                elif x < 700:
                    current_shape = "RHOMBUS"
                else:
                    current_shape = "CLEAR"
                    screen.fill(WHITE)

            
            else:
                drawing = True
                start_pos = event.pos
                end_pos = event.pos

        
        if event.type == pygame.MOUSEBUTTONUP:

            if drawing:
                end_pos = event.pos

                if current_shape == "SQUARE":
                    draw_square(screen, current_color, start_pos, end_pos)

                elif current_shape == "RIGHT TRIANGLE":
                    draw_right_triangle(
                        screen, current_color, start_pos, end_pos
                    )

                elif current_shape == "EQUILATERAL TRIANGLE":
                    draw_equilateral_triangle(
                        screen, current_color, start_pos, end_pos
                    )

                elif current_shape == "RHOMBUS":
                    draw_rhombus(
                        screen, current_color, start_pos, end_pos
                    )

                drawing = False

        
        if event.type == pygame.MOUSEMOTION:
            if drawing and current_shape == "PENCIL":
                pygame.draw.line(
                    screen, current_color,
                    event.pos, event.pos, 5
                )

    
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 80))

    
    for i, color in enumerate(colors):
        pygame.draw.rect(
            screen, color,
            (i * 40, 0, 35, 35)
        )

    
    labels = [
        "PENCIL", "SQUARE", "RIGHT TRIANGLE",
        "EQUILATERAL TRIANGLE", "RHOMBUS", "CLEAR"
    ]

    positions = [5, 105, 205, 355, 555, 710]

    for i in range(len(labels)):
        text = font.render(labels[i], True, BLACK)
        screen.blit(text, (positions[i], 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()