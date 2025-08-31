import pygame
import random
import os
import time

class Ball:
    def __init__(self, x, y, radius, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

class Paddle:
    def __init__(self, x, y, width, height, speed, screen_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.screen_width = screen_width

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bouncing Ball Game")

        # Load background once
        self.bg_image = pygame.image.load("background.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))

        # Load sounds once
        self.bounce_sound = pygame.mixer.Sound("bounce.wav")
        self.life_lost_sound = pygame.mixer.Sound("life_lost.wav")
        self.game_over_sound = pygame.mixer.Sound("game_over.wav")

        # Background music
        pygame.mixer.music.load("bg_music.mp3")
        pygame.mixer.music.play(-1)

        # HUD surface (semi-transparent)
        self.hud_surface = pygame.Surface((220, 90))
        self.hud_surface.set_alpha(150)
        self.hud_surface.fill((255, 255, 255))

        self.clock = pygame.time.Clock()
        self.reset_game_vars()
        self.running = True

        # Sound cooldown
        self.last_bounce_time = 0
        self.bounce_cooldown = 50  # milliseconds

        # High score
        self.highscore_file = "highscore.txt"
        self.highscore = self.load_highscore()

    def reset_game_vars(self):
        self.balls = [Ball(400, 300, 15, random.choice([-4, 4]), -4)]
        self.paddle = Paddle(350, 580, 100, 15, 7, self.WIDTH)
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.speed_multiplier = 1.05
        self.speed_increment_interval = 5000
        self.last_speed_increase_time = pygame.time.get_ticks()

    def load_highscore(self):
        if os.path.exists(self.highscore_file):
            with open(self.highscore_file, "r") as f:
                return int(f.read())
        return 0

    def save_highscore(self):
        with open(self.highscore_file, "w") as f:
            f.write(str(self.highscore))

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game_vars()
                    elif event.key == pygame.K_q:
                        self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.paddle.move(keys)

        current_time = pygame.time.get_ticks()

        for ball in self.balls:
            ball.move()

            # Wall bounce
            if ball.x - ball.radius <= 0 or ball.x + ball.radius >= self.WIDTH:
                ball.dx *= -1
                if current_time - self.last_bounce_time > self.bounce_cooldown:
                    self.bounce_sound.play()
                    self.last_bounce_time = current_time
            if ball.y - ball.radius <= 0:
                ball.dy *= -1
                if current_time - self.last_bounce_time > self.bounce_cooldown:
                    self.bounce_sound.play()
                    self.last_bounce_time = current_time

            # Paddle bounce
            if (self.paddle.y <= ball.y + ball.radius <= self.paddle.y + self.paddle.height) and \
               (self.paddle.x <= ball.x <= self.paddle.x + self.paddle.width):
                ball.dy *= -1
                self.score += 1
                if current_time - self.last_bounce_time > self.bounce_cooldown:
                    self.bounce_sound.play()
                    self.last_bounce_time = current_time

                if self.score % 5 == 0:
                    ball.dx *= 1.1
                    ball.dy *= 1.1
                    if self.paddle.width > 50:
                        self.paddle.width -= 10

            # Ball touches ground
            if ball.y + ball.radius >= self.HEIGHT:
                self.lives -= 1
                self.life_lost_sound.play()
                if self.lives > 0:
                    ball.x, ball.y = 400, 300
                    ball.dx, ball.dy = random.choice([-4, 4]), -4
                else:
                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.save_highscore()
                    self.game_over_sound.play()
                    self.game_over = True

        # Gradual speed increase
        if current_time - self.last_speed_increase_time > self.speed_increment_interval:
            for ball in self.balls:
                ball.dx *= self.speed_multiplier
                ball.dy *= self.speed_multiplier
            self.last_speed_increase_time = current_time

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.paddle.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)

        # HUD
        self.screen.blit(self.hud_surface, (0, 0))
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {self.lives}", True, (0, 0, 0))
        highscore_text = font.render(f"High Score: {self.highscore}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(highscore_text, (10, 70))

        # Game Over screen
        if self.game_over:
            font_big = pygame.font.SysFont(None, 80)
            font_small = pygame.font.SysFont(None, 40)

            game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
            score_text2 = font_small.render(f"Your Score: {self.score}", True, (255, 255, 255))
            highscore_text2 = font_small.render(f"High Score: {self.highscore}", True, (255, 255, 255))
            restart_text = font_small.render("Press R to Restart", True, (255, 255, 0))
            quit_text = font_small.render("Press Q to Quit", True, (255, 255, 0))

            self.screen.blit(game_over_text, (self.WIDTH//2 - 180, 150))
            self.screen.blit(score_text2, (self.WIDTH//2 - 120, 300))
            self.screen.blit(highscore_text2, (self.WIDTH//2 - 140, 350))
            self.screen.blit(restart_text, (self.WIDTH//2 - 150, 450))
            self.screen.blit(quit_text, (self.WIDTH//2 - 120, 500))

        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
    pygame.quit()
