import pygame
import math



def draw_pencil(surface, start_pos, end_pos, color, brush_size):
    pygame.draw.line(
        surface,
        color,
        start_pos,
        end_pos,
        brush_size
    )

    pygame.draw.circle(
        surface,
        color,
        end_pos,
        brush_size // 2
    )



def draw_line(surface, start_pos, end_pos, color, brush_size):
    pygame.draw.line(
        surface,
        color,
        start_pos,
        end_pos,
        brush_size
    )



def draw_rectangle(surface, start_pos, end_pos, color, brush_size):
    rect = pygame.Rect(start_pos, end_pos)
    rect.normalize()

    pygame.draw.rect(
        surface,
        color,
        rect,
        brush_size
    )



def draw_circle(surface, start_pos, end_pos, color, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

    pygame.draw.circle(
        surface,
        color,
        start_pos,
        radius,
        brush_size
    )



def draw_square(surface, start_pos, end_pos, color, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x = x1 - side
    else:
        x = x1

    if y2 < y1:
        y = y1 - side
    else:
        y = y1

    pygame.draw.rect(
        surface,
        color,
        (x, y, side, side),
        brush_size
    )



def draw_right_triangle(surface, start_pos, end_pos, color, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(
        surface,
        color,
        points,
        brush_size
    )



def draw_equilateral_triangle(surface, start_pos, end_pos, color, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    width = abs(x2 - x1)
    height = width * math.sqrt(3) / 2

    center_x = (x1 + x2) / 2

    if y2 < y1:
        top_y = y1 - height
    else:
        top_y = y1

    points = [
        (center_x, top_y),
        (center_x - width / 2, top_y + height),
        (center_x + width / 2, top_y + height)
    ]

    pygame.draw.polygon(
        surface,
        color,
        points,
        brush_size
    )



def draw_rhombus(surface, start_pos, end_pos, color, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    pygame.draw.polygon(
        surface,
        color,
        points,
        brush_size
    )



def erase(surface, start_pos, end_pos, brush_size):
    pygame.draw.line(
        surface,
        (255, 255, 255),
        start_pos,
        end_pos,
        brush_size
    )

    pygame.draw.circle(
        surface,
        (255, 255, 255),
        end_pos,
        brush_size // 2
    )



def flood_fill(surface, start_pos, new_color):
    x, y = start_pos

    width, height = surface.get_size()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    pixels = [(x, y)]

    while pixels:
        current_x, current_y = pixels.pop()

        if current_x < 0 or current_x >= width:
            continue

        if current_y < 0 or current_y >= height:
            continue

        if surface.get_at((current_x, current_y)) != target_color:
            continue

        surface.set_at((current_x, current_y), new_color)

        pixels.append((current_x + 1, current_y))
        pixels.append((current_x - 1, current_y))
        pixels.append((current_x, current_y + 1))
        pixels.append((current_x, current_y - 1))