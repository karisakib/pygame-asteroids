# asteroidfield.py
import pygame
import random
from asteroid import Asteroid # Import the Asteroid class we just created
from constants import * # Import game constants

class AsteroidField(pygame.sprite.Sprite):
    # This static field will be set in main.py before an instance is created
    # containers = () # Example: AsteroidField.containers = (updatable_sprites,)

    edges = [
        [
            pygame.Vector2(1, 0), # Direction from left edge
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0), # Direction from right edge
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1), # Direction from top edge
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1), # Direction from bottom edge
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        # The Sprite.__init__ needs to be called with self.containers
        # Ensure AsteroidField.containers is set before creating an instance.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__() # Fallback if containers not set
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        # This creates an Asteroid instance.
        # Because Asteroid.containers will be set in main.py,
        # the new asteroid will automatically be added to the correct groups.
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100) # Speed of the asteroid
            velocity = edge[0] * speed      # Initial velocity based on spawn edge
            velocity = velocity.rotate(random.randint(-30, 30)) # Slight random angle
            position = edge[1](random.uniform(0, 1)) # Random position along the chosen edge
            kind = random.randint(1, ASTEROID_KINDS) # Random size for the asteroid
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)