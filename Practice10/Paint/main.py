import pygame


pygame.init()


WIDTH = 900
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Paint")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
GRAY = (200, 200, 200)


font = pygame.font.SysFont("Arial", 18)


canvas = pygame.Surface((WIDTH, HEIGHT - 80))
canvas.fill(WHITE)


current_color = BLACK
current_tool = "pencil"

drawing = False
start_pos = None
last_pos = None


brush_size = 5


color_buttons = [
    (BLACK, pygame.Rect(10, 20, 30, 30)),
    (RED, pygame.Rect(50, 20, 30, 30)),
    (GREEN, pygame.Rect(90, 20, 30, 30)),
    (BLUE, pygame.Rect(130, 20, 30, 30)),
    (YELLOW, pygame.Rect(170, 20, 30, 30)),
    (PINK, pygame.Rect(210, 20, 30, 30))
]


tool_buttons = {
    "pencil": pygame.Rect(270, 15, 80, 40),
    "rectangle": pygame.Rect(360, 15, 90, 40),
    "circle": pygame.Rect(460, 15, 70, 40),
    "eraser": pygame.Rect(540, 15, 80, 40),
    "clear": pygame.Rect(630, 15, 70, 40)
}


running = True

clock = pygame.time.Clock()

while running:

    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_x, mouse_y = event.pos

                
                for color, rect in color_buttons:

                    if rect.collidepoint(event.pos):

                        current_color = color

                
                for tool, rect in tool_buttons.items():

                    if rect.collidepoint(event.pos):

                        if tool == "clear":

                            canvas.fill(WHITE)

                        else:

                            current_tool = tool

                
                if mouse_y >= 80:

                    drawing = True

                    start_pos = (
                        mouse_x,
                        mouse_y - 80
                    )

                    last_pos = start_pos

        
        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and drawing:

                mouse_x, mouse_y = event.pos

                end_pos = (
                    mouse_x,
                    max(0, min(HEIGHT - 81, mouse_y - 80))
                )

                
                if current_tool == "rectangle":

                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    rect = pygame.Rect(
                        min(x1, x2),
                        min(y1, y2),
                        abs(x2 - x1),
                        abs(y2 - y1)
                    )

                    pygame.draw.rect(
                        canvas,
                        current_color,
                        rect,
                        3
                    )

                
                elif current_tool == "circle":

                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    radius = int(
                        ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    )

                    pygame.draw.circle(
                        canvas,
                        current_color,
                        start_pos,
                        radius,
                        3
                    )

                drawing = False

                start_pos = None
                last_pos = None

   
    if drawing and current_tool in ["pencil", "eraser"]:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_y >= 80:

            current_pos = (
                mouse_x,
                mouse_y - 80
            )

            
            if current_tool == "eraser":

                draw_color = WHITE
                size = 25

            else:

                draw_color = current_color
                size = brush_size

           
            pygame.draw.line(
                canvas,
                draw_color,
                last_pos,
                current_pos,
                size
            )

            
            pygame.draw.circle(
                canvas,
                draw_color,
                current_pos,
                size // 2
            )

            last_pos = current_pos

    
    screen.fill(GRAY)

    
    pygame.draw.rect(
        screen,
        (180, 180, 180),
        (0, 0, WIDTH, 80)
    )

    
    for color, rect in color_buttons:

        pygame.draw.rect(
            screen,
            color,
            rect
        )

        pygame.draw.rect(
            screen,
            BLACK,
            rect,
            2
        )

    
    for tool, rect in tool_buttons.items():

        pygame.draw.rect(
            screen,
            WHITE,
            rect
        )

        pygame.draw.rect(
            screen,
            BLACK,
            rect,
            2
        )

        text = font.render(
            tool.capitalize(),
            True,
            BLACK
        )

        screen.blit(
            text,
            (rect.x + 8, rect.y + 10)
        )

    
    selected_text = font.render(
        "Selected: " + current_tool,
        True,
        BLACK
    )

    screen.blit(
        selected_text,
        (720, 25)
    )

    
    screen.blit(canvas, (0, 80))

    
    pygame.display.flip()

    clock.tick(60)



pygame.quit()