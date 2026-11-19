# hi
import pygame
import random
import math

# Simulation settings
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 40
ANT_COUNT = 50
ANT_RADIUS = 6
ANT_SPEED = 2

# Colors
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BROWN = (130, 70, 30)


class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * ANT_SPEED
        self.vy = math.sin(angle) * ANT_SPEED

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x <= ANT_RADIUS or self.x >= WIDTH - ANT_RADIUS:
            self.vx *= -1
            self.x = max(ANT_RADIUS, min(self.x, WIDTH - ANT_RADIUS))

        if self.y <= ANT_RADIUS or self.y >= HEIGHT - ANT_RADIUS:
            self.vy *= -1
            self.y = max(ANT_RADIUS, min(self.y, HEIGHT - ANT_RADIUS))

    def draw(self, screen):
        body = (int(self.x), int(self.y))
        head = (
            int(self.x + self.vx * 2),
            int(self.y + self.vy * 2)
        )

        pygame.draw.circle(screen, BROWN, body, ANT_RADIUS)
        pygame.draw.circle(screen, BROWN, head, 3)


def check_collision(ant1, ant2):
    dx = ant2.x - ant1.x
    dy = ant2.y - ant1.y
    distance = math.sqrt(dx**2 + dy**2)

    if 0 < distance < ANT_RADIUS * 2:
        # Direction between ants
        nx = dx / distance
        ny = dy / distance

        # Separate overlapping ants
        overlap = ANT_RADIUS * 2 - distance
        ant1.x -= nx * overlap / 2
        ant1.y -= ny * overlap / 2
        ant2.x += nx * overlap / 2
        ant2.y += ny * overlap / 2

        # Change velocities when ants collide
        relative_speed = (
            (ant1.vx - ant2.vx) * nx
            + (ant1.vy - ant2.vy) * ny
        )

        if relative_speed > 0:
            ant1.vx -= relative_speed * nx
            ant1.vy -= relative_speed * ny
            ant2.vx += relative_speed * nx
            ant2.vy += relative_speed * ny


# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ant Colony Simulation")
clock = pygame.time.Clock()

# Create ants
positions = [
    (x, y)
    for x in range(GRID_SIZE // 2, WIDTH, GRID_SIZE)
    for y in range(GRID_SIZE // 2, HEIGHT, GRID_SIZE)
]

starting_positions = random.sample(positions, ANT_COUNT)
ants = [Ant(x, y) for x, y in starting_positions]

running = True

while running:
    # Check if the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move ants
    for ant in ants:
        ant.move()

    # Check collisions between ants
    for i in range(len(ants)):
        for j in range(i + 1, len(ants)):
            check_collision(ants[i], ants[j])

    # Draw background
    screen.fill(WHITE)

    # Draw grid
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Draw ants
    for ant in ants:
        ant.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
