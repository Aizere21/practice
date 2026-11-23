import datetime
import math
import os

import pygame


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "images", "mickey_hand.png")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def get_time():
    now = datetime.datetime.now()
    seconds = min(now.second, 59)  
    return now.minute, seconds


def make_hand(image, length):
    
    ratio = length / image.get_height()
    width = int(image.get_width() * ratio)
    hand = pygame.transform.smoothscale(image, (width, length))

    side = length * 2                                  
    canvas = pygame.Surface((side, side), pygame.SRCALPHA)  
    
    canvas.blit(hand, (side // 2 - width // 2, side // 2 - length))
    return canvas


class MickeyClock:
    
    def __init__(self, center, radius):
        self.center = center      # (x, y) of the clock center
        self.radius = radius

        image = pygame.image.load(IMAGE_PATH).convert_alpha()

        self.minute_hand = make_hand(image, int(radius * 0.75))
        
        mirrored = pygame.transform.flip(image, True, False)
        self.second_hand = make_hand(mirrored, int(radius * 0.92))

        self.font = pygame.font.SysFont("arial", 34, bold=True)

    def draw_face(self, screen):
       
        cx, cy = self.center
        pygame.draw.circle(screen, WHITE, self.center, self.radius)
        pygame.draw.circle(screen, BLACK, self.center, self.radius, 6)

        for i in range(60):
            angle = math.radians(i * 6)          
            dx, dy = math.sin(angle), -math.cos(angle)   
            size = 22 if i % 5 == 0 else 10     
            outer = self.radius - 8
            inner = outer - size
            pygame.draw.line(
                screen, BLACK,
                (cx + dx * outer, cy + dy * outer),
                (cx + dx * inner, cy + dy * inner),
                4 if i % 5 == 0 else 2,
            )

        for n in range(1, 13):
            angle = math.radians(n * 30)         
            x = cx + math.sin(angle) * (self.radius - 55)
            y = cy - math.cos(angle) * (self.radius - 55)
            text = self.font.render(str(n * 5), True, BLACK)
            screen.blit(text, text.get_rect(center=(x, y)))

    def draw_hand(self, screen, hand, angle):
       
        
        rotated = pygame.transform.rotate(hand, -angle)
        
        screen.blit(rotated, rotated.get_rect(center=self.center))

    def draw(self, screen):
       
        minutes, seconds = get_time()

        
        second_angle = seconds * 6
        minute_angle = (minutes + seconds / 60) * 6  

        self.draw_face(screen)
        self.draw_hand(screen, self.minute_hand, minute_angle)
        self.draw_hand(screen, self.second_hand, second_angle)
        pygame.draw.circle(screen, BLACK, self.center, 10) 

       
        label = self.font.render(f"{minutes:02d}:{seconds:02d}", True, BLACK)
        x, y = self.center
        screen.blit(label, label.get_rect(center=(x, y + self.radius + 35)))
