# player.py
import pygame
from constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN # Import the new cooldown constant
)
from game_objects import CircleShape
from shot import Shot

class Player(CircleShape):
    # Player.containers will be set in main.py

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown_timer = 0.0 # Initialize the shoot cooldown timer

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt, direction):
        self.rotation += PLAYER_TURN_SPEED * dt * direction
        self.rotation %= 360

    def move(self, dt, direction_modifier):
        forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward_direction * PLAYER_SPEED * dt * direction_modifier

    def shoot(self):
        # This method is now only called if the cooldown timer is <= 0
        shot_position = self.position.copy()
        direction_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_velocity = direction_vector * PLAYER_SHOOT_SPEED

        new_shot = Shot(shot_position.x, shot_position.y)
        new_shot.velocity = shot_velocity
        
        # Reset the cooldown timer
        self.shoot_cooldown_timer = PLAYER_SHOOT_COOLDOWN
        # print(f"Shot fired! Cooldown set to: {self.shoot_cooldown_timer}") # For debugging

    def update(self, dt):
        # Decrease cooldown timer
        if self.shoot_cooldown_timer > 0:
            self.shoot_cooldown_timer -= dt
            if self.shoot_cooldown_timer < 0: # Ensure it doesn't go far negative
                self.shoot_cooldown_timer = 0.0

        keys = pygame.key.get_pressed()

        # Rotation and Movement
        if keys[pygame.K_a]:
            self.rotate(dt, -1)
        if keys[pygame.K_d]:
            self.rotate(dt, 1)
        if keys[pygame.K_w]:
            self.move(dt, 1)
        if keys[pygame.K_s]:
            self.move(dt, -1)

        # Shooting
        if keys[pygame.K_SPACE]:
            if self.shoot_cooldown_timer <= 0: # Check if cooldown has elapsed
                self.shoot()