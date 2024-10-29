import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_KINDS, ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS, ASTEROID_SPAWN_RATE, PLAYER_RADIUS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def draw_text(screen, text, size, color, x, y):
    """Helper function to display text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def start_screen(screen):
    """Displays the start screen and waits for player input."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: 
                waiting = False

        # Fill the screen with black and display the start message
        screen.fill("black")
        draw_text(screen, "Press any key to start", 50, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.flip()

def game_over_screen(screen):
    """Displays the game over screen and waits for player input."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return event.key  

        screen.fill("black")
        draw_text(screen, "Game Over!", 80, (255, 0, 0), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
        draw_text(screen, "Press R to Restart or Q to Quit", 50, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        pygame.display.flip()


def main_game(screen):
    running = True
    clock = pygame.time.Clock()
    dt = 0

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updateable, drawable)
    AsteroidField.containers = (updateable)
    Asteroid.containers = (asteroids, updateable, drawable)
    Player.containers = (updateable, drawable)

    p = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    af = AsteroidField()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for item in updateable:
            item.update(dt)

        for asteroid in asteroids:
            if asteroid.collided(p):
                return "GAME_OVER" 

            for bullet in shots:
                if asteroid.collided(bullet):
                    asteroid.split()
                    bullet.kill()

        screen.fill("black")
        for item in drawable:
            item.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print('Starting asteroids!')

    while True:
        start_screen(screen)  # Show the start screen

        game_state = main_game(screen)  # Run the main game
        if game_state == "GAME_OVER":
            key = game_over_screen(screen)  # Show game over screen and wait for input

            if key == pygame.K_r:  # Restart the game
                continue
            elif key == pygame.K_q:  # Quit the game
                break

    pygame.quit()


if __name__ == "__main__":
    main()