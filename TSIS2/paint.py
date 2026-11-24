import pygame
import math
import os
from datetime import datetime

from tools import (
    draw_pencil,
    draw_line,
    draw_rectangle,
    draw_circle,
    draw_square,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    erase,
    flood_fill
)


pygame.init()


WIDTH = 1100
HEIGHT = 750
TOOLBAR_HEIGHT = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 - Paint Application")

clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (70, 70, 70)

RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 200)
ORANGE = (255, 140, 0)
PINK = (255, 100, 150)

colors = [
    BLACK, WHITE, RED, GREEN, BLUE,
    YELLOW, PURPLE, ORANGE, PINK
]

selected_color = BLACK


brush_sizes = [2, 5, 10]
brush_index = 1
brush_size = brush_sizes[brush_index]


tool_names = [
    "Pencil",
    "Line",
    "Rectangle",
    "Circle",
    "Square",
    "Right Triangle",
    "Equilateral Triangle",
    "Rhombus",
    "Eraser",
    "Fill",
    "Text"
]

selected_tool = "Pencil"


canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)


preview = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
preview.fill((0, 0, 0))
preview.set_colorkey((0, 0, 0))

font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 24)


drawing = False
start_pos = None
previous_pos = None


text_active = False
text_input = ""
text_position = None


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

  
    for i, name in enumerate(tool_names):
        x = 10 + (i % 6) * 180
        y = 10 + (i // 6) * 40

        color = (120, 170, 220) if selected_tool == name else WHITE

        pygame.draw.rect(screen, color, (x, y, 165, 30))
        pygame.draw.rect(screen, BLACK, (x, y, 165, 30), 1)

        label = font.render(name, True, BLACK)
        screen.blit(label, (x + 5, y + 5))

  
    for i, color in enumerate(colors):
        x = 10 + i * 35
        y = 85

        pygame.draw.rect(screen, color, (x, y, 25, 12))
        pygame.draw.rect(screen, BLACK, (x, y, 25, 12), 1)

   
    size_text = font.render(
        f"Brush: {brush_size}px (1/2/3)",
        True,
        BLACK
    )

    screen.blit(size_text, (370, 82))


def save_canvas():
    filename = datetime.now().strftime("painting_%Y%m%d_%H%M%S.png")

    pygame.image.save(canvas, filename)

    print("Canvas saved:", filename)


def draw_current_shape(surface, start, end):
    if selected_tool == "Line":
        draw_line(surface, start, end, selected_color, brush_size)

    elif selected_tool == "Rectangle":
        draw_rectangle(surface, start, end, selected_color, brush_size)

    elif selected_tool == "Circle":
        draw_circle(surface, start, end, selected_color, brush_size)

    elif selected_tool == "Square":
        draw_square(surface, start, end, selected_color, brush_size)

    elif selected_tool == "Right Triangle":
        draw_right_triangle(surface, start, end, selected_color, brush_size)

    elif selected_tool == "Equilateral Triangle":
        draw_equilateral_triangle(surface, start, end, selected_color, brush_size)

    elif selected_tool == "Rhombus":
        draw_rhombus(surface, start, end, selected_color, brush_size)


running = True

while running:

    screen.fill(WHITE)

    draw_toolbar()

    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

      
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                text_active = False
                text_input = ""

            if event.key == pygame.K_1:
                brush_index = 0
                brush_size = brush_sizes[brush_index]

            if event.key == pygame.K_2:
                brush_index = 1
                brush_size = brush_sizes[brush_index]

            if event.key == pygame.K_3:
                brush_index = 2
                brush_size = brush_sizes[brush_index]

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            if text_active:

                if event.key == pygame.K_RETURN:

                    text_surface = text_font.render(
                        text_input,
                        True,
                        selected_color
                    )

                    canvas.blit(text_surface, text_position)

                    text_active = False
                    text_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                elif event.unicode and event.unicode.isprintable():
                    text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

           
            if mouse_y < TOOLBAR_HEIGHT:

                for i, name in enumerate(tool_names):

                    x = 10 + (i % 6) * 180
                    y = 10 + (i // 6) * 40

                    if x <= mouse_x <= x + 165 and y <= mouse_y <= y + 30:
                        selected_tool = name

             
                if mouse_y >= 80:

                    for i, color in enumerate(colors):

                        x = 10 + i * 35

                        if x <= mouse_x <= x + 25:
                            selected_color = color

            else:

                canvas_pos = (
                    mouse_x,
                    mouse_y - TOOLBAR_HEIGHT
                )

                if selected_tool == "Fill":

                    flood_fill(canvas, canvas_pos, selected_color)

                elif selected_tool == "Text":

                    text_active = True
                    text_position = canvas_pos
                    text_input = ""

                elif selected_tool == "Pencil":

                    drawing = True
                    previous_pos = canvas_pos

                elif selected_tool == "Eraser":

                    drawing = True
                    previous_pos = canvas_pos

                else:

                    drawing = True
                    start_pos = canvas_pos

       
        if event.type == pygame.MOUSEMOTION:

            if drawing:

                mouse_x, mouse_y = event.pos

                current_pos = (
                    mouse_x,
                    mouse_y - TOOLBAR_HEIGHT
                )

                if selected_tool == "Pencil":

                    draw_pencil(
                        canvas,
                        previous_pos,
                        current_pos,
                        selected_color,
                        brush_size
                    )

                    previous_pos = current_pos

                elif selected_tool == "Eraser":

                    erase(
                        canvas,
                        previous_pos,
                        current_pos,
                        brush_size * 5
                    )

                    previous_pos = current_pos

       
        if event.type == pygame.MOUSEBUTTONUP:

            if drawing:

                mouse_x, mouse_y = event.pos

                end_pos = (
                    mouse_x,
                    mouse_y - TOOLBAR_HEIGHT
                )

                if selected_tool not in ["Pencil", "Eraser"]:

                    draw_current_shape(
                        canvas,
                        start_pos,
                        end_pos
                    )

                drawing = False

    
    if text_active:

        text_surface = text_font.render(
            text_input,
            True,
            selected_color
        )

        screen.blit(
            text_surface,
            text_position
        )


    if drawing and selected_tool not in ["Pencil", "Eraser"]:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        current_pos = (
            mouse_x,
            mouse_y - TOOLBAR_HEIGHT
        )

        preview.fill((0, 0, 0))

        draw_current_shape(
            preview,
            start_pos,
            current_pos
        )

        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    pygame.display.flip()

    clock.tick(60)


pygame.quit()