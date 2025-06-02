# shot.py
import pygame
from game_objects import CircleShape # Assuming CircleShape is in game_objects.py
from constants import SHOT_RADIUS

class Shot(CircleShape):
    # containers will be set in main.py before any Shot instance is created
    # Example: Shot.containers = (shots_group, updatable_sprites, drawable_sprites)

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        # self.velocity will be set by the Player when a shot is fired.

    def draw(self, screen):
        # Draw the shot as a simple white filled circle
        pygame.draw.circle(screen, "white", self.position, self.radius) # No border, filled

    def update(self, dt):
        # Move the shot in a straight line based on its velocity
        self.position += self.velocity * dt
        # Optional: Add logic here later to remove shots that go off-screen
        # if not screen.get_rect().collidepoint(self.position):
        #     self.kill() # Removes sprite from all groups