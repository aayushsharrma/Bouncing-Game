import pygame
import random


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SIZE = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BRICK_WIDTH = 50
BRICK_HEIGHT = 25
BRICK_MARGIN = 5
BRICK_COLUMNS = SCREEN_WIDTH // (BRICK_WIDTH + BRICK_MARGIN)
BRICK_ROWS = 5

# Colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
TRANSPARENT_RED = (255, 0, 0, 0)
SEMI_TRANSPARENT_WHITE = (255, 255, 255, 128) 
YELLOW = (255, 255, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bounce Game")
clock = pygame.time.Clock()

class Ball:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
        self.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-3, 3])
        self.dy = -3
        self.color = CYAN

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Collision with screen boundaries
        if self.x <= 0 or self.x >= SCREEN_WIDTH - BALL_SIZE:
            self.dx = -self.dx
        if self.y <= 0:
            self.dy = -self.dy
        elif self.y >= SCREEN_HEIGHT:
            return True  # Ball touched the ground
        return False

    def draw(self):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, BALL_SIZE, BALL_SIZE))

    def bounce(self):
        self.dy = -self.dy

class Paddle:
    def __init__(self):
        self.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.y = SCREEN_HEIGHT - 40
        self.dx = 5
        self.color = TRANSPARENT_RED

    def move(self, left, right):
        if left and self.x > 0:
            self.x -= self.dx
        if right and self.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.x += self.dx

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = YELLOW
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT))

    def hit(self):
        self.active = False
        return 10  # score for hitting a brick

# Create objects
ball = Ball()
paddle = Paddle()
bricks = [Brick((BRICK_WIDTH + BRICK_MARGIN) * j, (BRICK_HEIGHT + BRICK_MARGIN) * i) for i in range(BRICK_ROWS) for j in range(BRICK_COLUMNS)]
score = 0

running = True
while running:
    screen.fill(SEMI_TRANSPARENT_WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    paddle.move(keys[pygame.K_LEFT], keys[pygame.K_RIGHT])

    # Ball movement and collision
    if ball.move():
        running = False  # Game over if ball hits the ground

    # Ball-Paddle collision
    if paddle.y < ball.y + BALL_SIZE < paddle.y + PADDLE_HEIGHT and paddle.x < ball.x < paddle.x + PADDLE_WIDTH:
        ball.bounce()

    # Ball-Brick collision
    for brick in bricks:
        if brick.active and brick.y < ball.y < brick.y + BRICK_HEIGHT and brick.x < ball.x < brick.x + BRICK_WIDTH:
            score += brick.hit()
            ball.bounce()

    ball.draw()
    paddle.draw()
    for brick in bricks:
        brick.draw()

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
