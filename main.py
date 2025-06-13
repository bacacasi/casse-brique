import pygame

# Initialize Pygame modules
pygame.init()

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Brick Breaker")

# Paddle class
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect) # Use self.rect for drawing

    def move(self, direction):
        self.x += self.speed * direction
        # Boundary checking
        if self.x < 0:
            self.x = 0
        if self.x + self.width > screen_width:
            self.x = screen_width - self.width
        self.rect.x = self.x # Update rect position

# Ball class
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = 3  # Initial velocity
        self.dy = -3 # Initial velocity (moves upwards)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # Left/Right wall collision
        if self.x + self.radius > screen_width:
            self.x = screen_width - self.radius
            self.dx *= -1
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.dx *= -1

        # Top wall collision
        if self.y - self.radius < 0:
            self.y = self.radius
            self.dy *= -1
        # Note: Bottom wall collision will be handled later for game over

# Brick class
class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)

# Paddle properties
paddle_width = 100
paddle_height = 20
paddle_x = (screen_width / 2) - (paddle_width / 2)
paddle_y = screen_height - paddle_height - 30  # 30 pixels from the bottom
paddle = Paddle(paddle_x, paddle_y, paddle_width, paddle_height, GREEN)

# Ball properties
ball_radius = 10
ball_x = screen_width / 2
ball_y = screen_height / 2
ball = Ball(ball_x, ball_y, ball_radius, WHITE)

# Brick properties
bricks = []
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_HEIGHT = 20
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50

# Calculate brick_width based on screen width, columns, and padding
available_width_for_bricks = screen_width - (2 * BRICK_PADDING) # Initial side padding
BRICK_WIDTH = (available_width_for_bricks - ((BRICK_COLS - 1) * BRICK_PADDING)) // BRICK_COLS

# Calculate offset_left to center the brick grid
total_bricks_width = (BRICK_COLS * BRICK_WIDTH) + ((BRICK_COLS - 1) * BRICK_PADDING)
BRICK_OFFSET_LEFT = (screen_width - total_bricks_width) // 2

for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
        brick_y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
        brick = Brick(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT, BLUE)
        bricks.append(brick)

# Clock for managing FPS
clock = pygame.time.Clock()
FPS = 60

# Game state variables
game_over = False
game_won = False # To be used later

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not game_won:
        # Get pressed keys for continuous movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-1) # Move left
        if keys[pygame.K_RIGHT]:
            paddle.move(1)  # Move right

        # Update game state
        ball.update()

        # Check for game over condition (ball below screen)
        if ball.y + ball.radius > screen_height:
            game_over = True
            # Optional: Stop the ball exactly at the edge or let it go slightly past
            # ball.y = screen_height - ball.radius
            # ball.dx = 0 # Stop ball movement will be handled below
            # ball.dy = 0


        # Ball-Paddle Collision
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)

        if ball_rect.colliderect(paddle.rect):
            if ball.dy > 0: # Only bounce if ball is moving downwards
                ball.dy *= -1
                ball.y = paddle.rect.top - ball.radius # Adjust ball position to sit on top of paddle

        # Ball-Brick Collision
        # ball_rect is already current from paddle collision or needs recalculation if ball could have moved
        # For safety, let's assume ball_rect might need to be fresh if ball.update() was complex
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)

        for brick in bricks:
            if brick.visible: # Only check collision with visible bricks
                if ball_rect.colliderect(brick.rect):
                    brick.visible = False # Mark brick as broken
                    ball.dy *= -1       # Reverse ball's vertical direction
                    # Note: Score will be added later. No break, allow multiple breaks per frame.

        # Check for game won condition (all bricks cleared) - Placeholder for later
        # if all(not brick.visible for brick in bricks):
        # game_won = True

    else: # If game_over or game_won is True
        # Stop ball movement completely if game has ended
        ball.dx = 0
        ball.dy = 0

    # Fill the screen
    screen.fill(BLACK)

    # Draw the paddle
    paddle.draw(screen)
    # Draw the ball
    ball.draw(screen)
    # Draw the bricks
    for brick in bricks:
        brick.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
