import pygame
import random
import sys
import math  # Import Python's math module for the pulse effect

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Junk Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Backgrounds for different galaxies
backgrounds = [
    pygame.image.load("galaxy1.png"),
    pygame.image.load("galaxy2.png"),
    pygame.image.load("galaxy3.png"),
]

# Load images for spacecraft and space junk
spaceship_image = pygame.image.load("spaceship.png")
spaceship_image = pygame.transform.scale(spaceship_image, (40, 40))  # Resize for appropriate scale

junk_images = [
    pygame.image.load("junk1.png"),
    pygame.image.load("junk2.png"),
    pygame.image.load("junk3.png"),
    pygame.image.load("junk4.png"),
]

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 60)  # Position near bottom center

    def update(self):
        # Move the player with the mouse
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()

# Define the space junk class
class SpaceJunk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(junk_images)
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize junk for consistent scale
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height  # Start above the screen

    def update(self, speed=2):
        # Move the space junk downwards
        self.rect.y += speed

        # Remove junk if it goes off the screen
        if self.rect.top > screen_height:
            self.kill()

# Function to display the start menu
def show_start_menu():
    font_title = pygame.font.SysFont(None, 72)
    font_start = pygame.font.SysFont(None, 48)
    start_time = pygame.time.get_ticks()
    blinking = True

    while True:
        screen.blit(backgrounds[0], (0, 0))  # Display the first galaxy image as background

        # Pulsing title text
        time_passed = pygame.time.get_ticks() - start_time
        pulse_scale = 1.1 + 0.1 * math.sin(time_passed * 0.005)
        title_surface = font_title.render("Space Junk Game", True, WHITE)
        title_scaled = pygame.transform.scale(title_surface, (int(title_surface.get_width() * pulse_scale), int(title_surface.get_height() * pulse_scale)))
        screen.blit(title_scaled, (screen_width // 2 - title_scaled.get_width() // 2, screen_height // 3))

        # Display spacecraft image at the center of the screen
        screen.blit(spaceship_image, (screen_width // 2 - spaceship_image.get_width() // 2, screen_height // 2 - spaceship_image.get_height() // 2))

        # Blinking "Press ENTER to Start" text
        if blinking:
            start_surface = font_start.render("Press ENTER to Start", True, GREEN)
            screen.blit(start_surface, (screen_width // 2 - start_surface.get_width() // 2, screen_height * 2 // 3))

        if pygame.time.get_ticks() % 1000 < 500:
            blinking = not blinking

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # Start the game

# Function to display the game over screen
def show_game_over(survival_time):
    font = pygame.font.SysFont(None, 48)
    while True:
        screen.fill(BLACK)
        game_over_surface = font.render("Game Over", True, WHITE)
        restart_surface = font.render("Press R to Restart or Q to Quit", True, GREEN)
        score_surface = font.render(f"Your Survival Time: {survival_time // 1000} seconds", True, WHITE)

        screen.blit(game_over_surface, (screen_width // 2 - game_over_surface.get_width() // 2, screen_height // 3))
        screen.blit(score_surface, (screen_width // 2 - score_surface.get_width() // 2, screen_height // 2 - 30))
        screen.blit(restart_surface, (screen_width // 2 - restart_surface.get_width() // 2, screen_height // 2 + 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main game function
def main():
    global level, survival_time, junk_speed, level_message, level_message_start_time, show_level_message

    level = 0
    survival_time = 0
    survival_limit = 60000  # 1 minute in milliseconds
    junk_speed = 2  # Starting speed of junk
    level_message_display_time = 2000  # Time to show level transition message (in milliseconds)
    level_message = ""
    level_message_start_time = 0
    show_level_message = False

    player = Player()

    # Create a group for all sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create a group for space junk
    space_junk_group = pygame.sprite.Group()

    # Set up the game clock
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the player and space junk
        all_sprites.update()

        # Spawn new space junk at random intervals
        if pygame.time.get_ticks() % 1000 < 20:  # Check every frame if a second has passed
            space_junk = SpaceJunk()
            space_junk_group.add(space_junk)
            all_sprites.add(space_junk)

        # Check for collision between player and space junk
        if pygame.sprite.spritecollide(player, space_junk_group, False):
            show_game_over(survival_time)  # Show game over screen if colliding
            return  # Return to start menu

        # Update survival time
        survival_time += clock.get_time()
        if survival_time >= survival_limit:
            survival_time = 0  # Reset survival time
            level += 1  # Move to the next level
            junk_speed += 1  # Increase speed of junk
            if level >= len(backgrounds):  # Check if all levels have been completed
                level = 0  # Restart from the first level

            # Show level transition message
            level_message = f"Level {level + 1} - Survive for 1 minute!"
            level_message_start_time = pygame.time.get_ticks()
            show_level_message = True

        # Draw the screen
        screen.fill(BLACK)
        screen.blit(backgrounds[level], (0, 0))  # Draw the background for the current level
        for junk in space_junk_group:
            junk.update(junk_speed)  # Update each junk with the current speed

        all_sprites.draw(screen)

        # Draw the survival timer at the top
        timer_text = f"Survival Time: {survival_time // 1000} / 60 seconds"
        font = pygame.font.SysFont(None, 36)
        timer_surface = font.render(timer_text, True, WHITE)
        screen.blit(timer_surface, (10, 10))

        # Draw level transition message if applicable
        if show_level_message:
            current_time = pygame.time.get_ticks()
            if current_time - level_message_start_time < level_message_display_time:
                message_surface = font.render(level_message, True, GREEN)
                screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height // 2))
            else:
                show_level_message = False  # Hide message after the display time

        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

# Game loop
def game_loop():
    show_start_menu()  # Display the start menu
    while True:
        main()  # Run the main game

game_loop()

# Quit pygame when the game ends
pygame.quit()
