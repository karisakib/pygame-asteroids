import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid # Make sure Asteroid is imported
from asteroidfield import AsteroidField
from shot import Shot
# from game_objects import CircleShape

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids - Splitting Action!")

    print("Starting Asteroids!")
    # ... (other print statements)

    clock = pygame.time.Clock()

    # --- Create Sprite Groups ---
    updatable_sprites = pygame.sprite.Group()
    drawable_sprites = pygame.sprite.Group()
    asteroids_group = pygame.sprite.Group() # Crucial for managing all asteroids
    shots_group = pygame.sprite.Group()

    # --- Set Class Containers (MUST be done BEFORE creating instances) ---
    Player.containers = (updatable_sprites, drawable_sprites)
    # This ensures new asteroids (including split ones) are added to these groups
    Asteroid.containers = (asteroids_group, updatable_sprites, drawable_sprites)
    AsteroidField.containers = (updatable_sprites,)
    Shot.containers = (shots_group, updatable_sprites, drawable_sprites)

    # --- Instantiate Game Objects ---
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        dt = clock.tick(60) / 1000.0

        # --- Update Game State ---
        updatable_sprites.update(dt)

        # --- Collision Detection ---

        # 1. Player vs Asteroids
        # Using list() for asteroids_group in case player collision modifies it (e.g., game over)
        for asteroid in list(asteroids_group):
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()

        # 2. Shots vs Asteroids
        # Iterate over copies because groups will be modified (shot killed, asteroid split/killed)
        for shot in list(shots_group):
            # Check collision for this shot against all current asteroids
            collided_asteroid = None
            for asteroid in list(asteroids_group): # Iterate copy of asteroids for current shot
                if shot.collides_with(asteroid):
                    collided_asteroid = asteroid
                    break # Found an asteroid this shot hit

            if collided_asteroid:
                shot.kill() # Remove the shot
                collided_asteroid.split() # Call the new split method on the asteroid
                # No need to check this shot against other asteroids now.
                # The outer loop will get the next shot.
    
        # --- Render to Screen ---
        screen.fill("black")

        for sprite in drawable_sprites:
            sprite.draw(screen)

        pygame.display.flip()

    pygame.quit()
    print("Game Exited")

if __name__ == "__main__":
    main()