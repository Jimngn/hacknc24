import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROCKET_WIDTH = 50
ROCKET_HEIGHT = 50
ASTEROID_WIDTH = 50
ASTEROID_HEIGHT = 50
FPS = 60
SPEED = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket through Asteroid Field")

# Load rocket image
rocket_image = pygame.transform.scale(pygame.image.load('rocket.png'), (ROCKET_WIDTH, ROCKET_HEIGHT))

# Rocket class
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = rocket_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - ROCKET_HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += SPEED

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ASTEROID_WIDTH, ASTEROID_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
            self.rect.y = random.randint(-100, -40)

# Sprite groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Create rocket instance
rocket = Rocket()
all_sprites.add(rocket)

# Create asteroids
for i in range(10):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# Main game loop
clock = pygame.time.Clock()

def home_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Rocket through Asteroid Field", True, BLACK)
    start_font = pygame.font.Font(None, 50)
    start_text = start_font.render("Press S to Start", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    waiting = False

def crash_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("You Crashed!", True, BLACK)
    replay_font = pygame.font.Font(None, 50)
    replay_text = replay_font.render("Press R to Replay", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

# Show home screen before starting the game
home_screen()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollide(rocket, asteroids, False):
        crash_screen()
        # Reset positions
        rocket.rect.x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
        rocket.rect.y = SCREEN_HEIGHT - ROCKET_HEIGHT - 10
        for asteroid in asteroids:
            asteroid.rect.x = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
            asteroid.rect.y = random.randint(-100, -40)

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Refresh screen
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)
