# game_objects.py
import pygame

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # Sub-classes must override
        pass

    def update(self, dt):
        # Sub-classes must override
        pass

    def collides_with(self, other_shape):
        """
        Checks if this CircleShape collides with another CircleShape.
        :param other_shape: Another CircleShape object.
        :return: True if they collide, False otherwise.
        """
        if not isinstance(other_shape, CircleShape): # Optional: type check for safety
            return False
            
        distance = self.position.distance_to(other_shape.position)
        return distance <= (self.radius + other_shape.radius)