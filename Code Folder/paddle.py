import pygame

class Paddle:
    def __init__(self, x, y, width=100, height=15, color=(0,255,255), speed=8):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0  # Prevent crossing left wall

    def move_right(self, WIDTH, balls):
        self.x += self.speed
        # Prevent crossing right wall
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
        # Prevent paddle from going above any ball
        for ball in balls:
            if self.y < ball.y - ball.radius:
                self.y = ball.y - ball.radius

    def check_collision(self, ball):
        if (ball.y + ball.radius >= self.y and 
            self.x <= ball.x <= self.x + self.width and
            ball.dy > 0):
            ball.dy = -abs(ball.dy)  # bounce upwards
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
