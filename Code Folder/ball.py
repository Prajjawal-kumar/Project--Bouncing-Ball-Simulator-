import pygame
import random

class Ball:
    def __init__(self, x, y, radius=15, color=None, dx=None, dy=None, mass=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color if color else random.choice([(255,0,0),(0,255,0),(0,0,255),(255,255,0)])
        self.dx = dx if dx else random.choice([-3,-2,2,3])
        self.dy = dy if dy else random.choice([-3,-2,2,3])
        self.mass = mass
        self.gravity = 0.2

    def move(self, WIDTH, HEIGHT):
        self.dy += self.gravity   # gravity
        self.x += self.dx
        self.y += self.dy

        # Left/Right wall collisions
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = -self.dx
        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.dx = -self.dx

        # Bottom wall → life lost
        if self.y + self.radius >= HEIGHT:
            return True

        # Top wall
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = -self.dy

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
