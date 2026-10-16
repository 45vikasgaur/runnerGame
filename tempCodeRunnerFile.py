import pygame
import random
import sys

# Coin Runner - a simple 2D endless runner built with Pygame
pygame.init()

WIDTH, HEIGHT = 900, 500
GROUND_Y = 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Runner")
clock = pygame.time.Clock()

# Colors
SKY = (135, 206, 235)
WHITE = (255, 255, 255)
DARK = (30, 40, 55)
GREEN = (60, 175, 85)
DARK_GREEN = (40, 135, 65)
GOLD = (255, 205, 40)
ORANGE = (245, 145, 40)
RED = (220, 65, 65)
BLUE = (45, 105, 220)
BROWN = (130, 85, 45)

font = pygame.font.SysFont("arial", 26, bold=True)
big_font = pygame.font.SysFont("arial", 52, bold=True)
small_font = pygame.font.SysFont("arial", 20)

def draw_text(text, font_obj, color, x, y, center=False):
    surface = font_obj.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

class Player:
    def __init__(self):
        self.x = 120
        self.y = GROUND_Y - 58
        self.width = 38
        self.height = 58
        self.vel_y = 0
        self.on_ground = True
        self.run_frame = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, int(self.y), self.width, self.height)

    def jump(self):
        if self.on_ground:
            self.vel_y = -16
            self.on_ground = False

    def update(self):
        self.vel_y += 0.75
        self.y += self.vel_y
        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True
        self.run_frame += 1

    def draw(self):
        # Head
        pygame.draw.circle(screen, (245, 195, 150), (self.x + 19, int(self.y + 12)), 12)
        # Hair
        pygame.draw.arc(screen, DARK, (self.x + 7, int(self.y), 24, 20), 3.14, 6.2, 5)
        # Body
        pygame.draw.rect(screen, BLUE, (self.x + 7, int(self.y + 24), 25, 22), border_radius=6)
        # Arms
        swing = 5 if (self.run_frame // 7) % 2 == 0 else -5
        pygame.draw.line(screen, (245, 195, 150), (self.x + 8, int(self.y + 29)),
                         (self.x + 1, int(self.y + 37 + swing)), 5)
        pygame.draw.line(screen, (245, 195, 150), (self.x + 30, int(self.y + 29)),
                         (self.x + 37, int(self.y + 37 - swing)), 5)
        # Legs
        if self.on_ground:
            leg_swing = 7 if (self.run_frame // 6) % 2 == 0 else -7
        else:
            leg_swing = 0
        pygame.draw.line(screen, DARK, (self.x + 13, int(self.y + 44)),
                         (self.x + 10 + leg_swing, int(self.y + 57)), 6)
        pygame.draw.line(screen, DARK, (self.x + 26, int(self.y + 44)),
                         (self.x + 29 - leg_swing, int(self.y + 57)), 6)
        # Shoes
        pygame.draw.line(screen, RED, (self.x + 3 + leg_swing, int(self.y + 57)),
                         (self.x + 14 + leg_swing, int(self.y + 57)), 5)
        pygame.draw.line(screen, RED, (self.x + 24 - leg_swing, int(self.y + 57)),
                         (self.x + 35 - leg_swing, int(self.y + 57)), 5)

class Coin:
    def __init__(self, x):
        self.x = x
        self.y = random.choice([GROUND_Y - 65, GROUND_Y - 105, GROUND_Y - 145])
        self.radius = 13
        self.collected = False

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def update(self, speed):
        self.x -= speed

    def draw(self):
        pygame.draw.circle(screen, (210, 145, 15), (int(self.x), self.y), self.radius + 2)
        pygame.draw.circle(screen, GOLD, (int(self.x), self.y), self.radius)
        pygame.draw.circle(screen, (255, 238, 120), (int(self.x - 4), self.y - 4), 4)
        draw_text("$", small_font, (150, 100, 0), int(self.x - 6), self.y - 12)

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.width = random.choice([28, 36, 44])
        self.height = random.choice([35, 45, 55])

    @property
    def rect(self):
        return pygame.Rect(int(self.x), GROUND_Y - self.height,
                           self.width, self.height)

    def update(self, speed):
        self.x -= speed

    def draw(self):
        r = self.rect
        pygame.draw.rect(screen, BROWN, r, border_radius=5)
        pygame.draw.rect(screen, ORANGE, (r.x + 5, r.y + 5, max(5, r.width - 10), 7),
                         border_radius=3)
        pygame.draw.line(screen, (95, 55, 30), (r.x + 5, r.y + 17),
                         (r.right - 5, r.y + 28), 3)

def reset_game():
    return Player(), [], [], 0, 0, 6.0, False

def draw_background(distance):
    screen.fill(SKY)
    # Soft clouds
    for cx, cy in [(120, 85), (400, 65), (710, 105)]:
        pygame.draw.circle(screen, WHITE, (cx, cy), 18)
        pygame.draw.circle(screen, WHITE, (cx + 20, cy - 8), 22)
        pygame.draw.circle(screen, WHITE, (cx + 42, cy), 17)
    # Distant hills
    pygame.draw.ellipse(screen, (115, 195, 130), (-80, 250, 360, 180))
    pygame.draw.ellipse(screen, (95, 180, 115), (240, 270, 400, 160))
    pygame.draw.ellipse(screen, (115, 195, 130), (570, 245, 420, 190))
    # Ground
    pygame.draw.rect(screen, GREEN, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.rect(screen, DARK_GREEN, (0, GROUND_Y, WIDTH, 8))
    # Moving ground marks
    offset = int(distance * 3) % 55
    for x in range(-55, WIDTH + 55, 55):
        pygame.draw.line(screen, (90, 190, 100), (x - offset, GROUND_Y + 25),
                         (x + 18 - offset, GROUND_Y + 25), 3)

player, coins, obstacles, score, distance, speed, game_over = reset_game()
coin_timer = 0
obstacle_timer = 0
best_score = 0
running = True
started = False

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if not started:
                    started = True
                elif game_over:
                    player, coins, obstacles, score, distance, speed, game_over = reset_game()
                    coin_timer = obstacle_timer = 0
                    started = True
                else:
                    player.jump()
            if event.key == pygame.K_r and game_over:
                player, coins, obstacles, score, distance, speed, game_over = reset_game()
                coin_timer = obstacle_timer = 0
                started = True

    draw_background(distance)

    if not started:
        player.draw()
        draw_text("COIN RUNNER", big_font, DARK, WIDTH // 2, 145, center=True)
        draw_text("Press SPACE to start and jump", font, DARK, WIDTH // 2, 215, center=True)
        draw_text("Collect coins • Avoid obstacles • Beat your high score",
                  small_font, DARK, WIDTH // 2, 255, center=True)
    elif not game_over:
        player.update()
        distance += speed
        speed = min(12.0, 6.0 + distance / 1800)

        coin_timer += 1
        obstacle_timer += 1

        if coin_timer > random.randint(42, 72):
            coins.append(Coin(WIDTH + 30))
            coin_timer = 0
        if obstacle_timer > random.randint(75, 115):
            obstacles.append(Obstacle(WIDTH + 30))
            obstacle_timer = 0

        for coin in coins[:]:
            coin.update(speed)
            coin.draw()
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                score += 10
            elif coin.x < -30:
                coins.remove(coin)

        for obstacle in obstacles[:]:
            obstacle.update(speed)
            obstacle.draw()
            if player.rect.colliderect(obstacle.rect):
                game_over = True
                best_score = max(best_score, score)
            elif obstacle.x < -60:
                obstacles.remove(obstacle)

        player.draw()
        draw_text(f"Score: {score}", font, DARK, 20, 18)
        draw_text(f"Best: {best_score}", font, DARK, 20, 52)
        draw_text("SPACE / ↑ = Jump", small_font, DARK, WIDTH - 220, 22)
    else:
        for coin in coins:
            coin.draw()
        for obstacle in obstacles:
            obstacle.draw()
        player.draw()
        draw_text("GAME OVER", big_font, RED, WIDTH // 2, 155, center=True)
        draw_text(f"Your score: {score}", font, DARK, WIDTH // 2, 220, center=True)
        draw_text(f"Best score this session: {best_score}", font, DARK,
                  WIDTH // 2, 258, center=True)
        draw_text("Press SPACE or R to play again", small_font, DARK,
                  WIDTH // 2, 305, center=True)

    pygame.display.flip()

pygame.quit()
sys.exit()
