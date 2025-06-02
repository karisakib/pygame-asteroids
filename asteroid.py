# asteroid.py
import pygame
import random # Import the random module
from game_objects import CircleShape
from constants import ASTEROID_MIN_RADIUS # Import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    # Asteroid.containers will be set in main.py

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # self.velocity is inherited from CircleShape and set by AsteroidField or when splitting

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        """
        Splits the asteroid into two smaller asteroids or destroys it if it's too small.
        """
        self.kill() # This asteroid is always destroyed when split is called.

        # If the asteroid is already the minimum size, it just disappears (already killed).
        if self.radius <= ASTEROID_MIN_RADIUS:
            # print(f"Small asteroid {id(self)} destroyed, no split.") # For debugging
            return

        # Calculate properties for the new smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS # Or self.radius / 2, depending on desired game feel
                                                      # The prompt says "old_radius - ASTEROID_MIN_RADIUS"
        if new_radius < ASTEROID_MIN_RADIUS: # Ensure new radius is not too small
            new_radius = ASTEROID_MIN_RADIUS


        # Generate a random angle for splitting direction
        # random.uniform(min, max) gives a float
        split_angle_offset = random.uniform(20, 50) # degrees

        # Create two new velocity vectors
        # Start with the current asteroid's velocity
        base_velocity = self.velocity.copy() # Important to copy if you modify it directly

        # Velocity for the first new asteroid
        velocity1 = base_velocity.rotate(split_angle_offset)
        velocity1 *= 1.2 # Make it move faster

        # Velocity for the second new asteroid
        velocity2 = base_velocity.rotate(-split_angle_offset) # Rotate in the opposite direction
        velocity2 *= 1.2 # Make it move faster

        # Create two new Asteroid objects at the current asteroid's position
        # They will be automatically added to the groups defined in Asteroid.containers (main.py)
        
        # print(f"Splitting asteroid {id(self)} (r={self.radius}) at {self.position}") # Debug
        # print(f"  New radius: {new_radius}") # Debug
        # print(f"  Vel1: {velocity1}, Vel2: {velocity2}") # Debug

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2