import pygame
import random
import sys
import math
from PIL import Image, ImageSequence  # Import ImageSequence to handle GIFs

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Elon's Journey to Mars")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load images for different screens and backgrounds
start_image = pygame.image.load("start_screen.png")  # Start screen image
end_image = pygame.image.load("end_screen.png")      # End screen image
backgrounds = [
    pygame.image.load("galaxy1.png"),
    pygame.image.load("galaxy2.png"),
    pygame.image.load("galaxy3.png"),
    pygame.image.load("galaxy4.png")
]

victory_sound = pygame.mixer.Sound("victory_sound.wav")


# Load images for spacecraft (GIF)
def load_gif(filename, scale_factor=0.5):
    frames = []
    with Image.open(filename) as img:
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("RGBA")  # Ensure it has an alpha channel
            frame = frame.resize((int(frame.width * scale_factor), int(frame.height * scale_factor)), Image.LANCZOS)
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
    return frames

spaceship_frames = load_gif("spaceship.gif", scale_factor=0.4)
current_frame = 0

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = spaceship_frames
        self.image = self.frames[current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 60)
        self.speed = 5

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Loop back if spaceship goes out of bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        # Update spaceship animation
        global current_frame
        current_frame = (current_frame + 1) % len(self.frames)
        self.image = self.frames[current_frame]

# Load junk images
junk_images = [
    pygame.image.load("junk1.png"),
    pygame.image.load("junk2.png"),
    pygame.image.load("junk3.png"),
    pygame.image.load("junk4.png")
]

# Define the space junk class
class SpaceJunk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(random.choice(junk_images), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self, speed=2):
        self.rect.y += speed
        if self.rect.top > screen_height:
            self.kill()

# Display the start menu
def show_start_menu():
    font_title = pygame.font.SysFont(None, 72)
    font_start = pygame.font.SysFont(None, 48)
    blinking = True
    start_time = pygame.time.get_ticks()

    while True:
        screen.blit(start_image, (0, 0))

        # Pulsing title text
        time_passed = pygame.time.get_ticks() - start_time
        pulse_scale = 1.1 + 0.1 * math.sin(time_passed * 0.005)
        title_surface = font_title.render("Elon's Journey to Mars", True, WHITE)
        title_scaled = pygame.transform.scale(title_surface, (int(title_surface.get_width() * pulse_scale), int(title_surface.get_height() * pulse_scale)))
        screen.blit(title_scaled, (screen_width // 2 - title_scaled.get_width() // 2, screen_height // 3))

        # Blinking "Press ENTER to Start" text
        if blinking:
            start_surface = font_start.render("Press ENTER to Start", True, GREEN)
            screen.blit(start_surface, (screen_width // 2 - start_surface.get_width() // 2, screen_height * 2 // 3))

        if pygame.time.get_ticks() % 1000 < 500:
            blinking = not blinking

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Game over screen
# Game over screen
def show_game_over(survival_time, won=False):
    font_title = pygame.font.SysFont(None, 72)
    font_message = pygame.font.SysFont(None, 48)
    font_restart_quit = pygame.font.SysFont("comicsansms", 48)

    messages = [
        "Well, Elon... almost made it!",
        "Ah, next time, Elon!",
        "Better luck dodging next time!",
        "Almost there, just a few more space junk!"
    ]
    message = random.choice(messages) if not won else "Elon!! You finally did it!"

    # If won, stop the background music and play the victory sound
    if won:
        pygame.mixer.music.stop()  # Stop the background music
        victory_sound.play()  # Play the victory sound

    blink_time = pygame.time.get_ticks()
    while True:
        screen.blit(end_image, (0, 0))
        game_over_surface = font_title.render("Game Over" if not won else "Victory!", True, (255, 215, 0))
        message_surface = font_message.render(message, True, WHITE)

        current_time = pygame.time.get_ticks()
        if (current_time - blink_time) % 1000 < 500:
            restart_surface = font_restart_quit.render("Press R to Restart", True, (0, 200, 0))
            quit_surface = font_restart_quit.render("Press Q to Quit", True, (200, 0, 0))
        else:
            restart_surface = font_restart_quit.render("Press R to Restart", True, (0, 150, 0))
            quit_surface = font_restart_quit.render("Press Q to Quit", True, (150, 0, 0))

        screen.blit(game_over_surface, (screen_width // 2 - game_over_surface.get_width() // 2, screen_height // 4 - 40))
        screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height // 4 + 10))
        survival_time_surface = font_message.render(f"Survival Time: {survival_time // 1000} seconds", True, (173, 216, 230))
        screen.blit(survival_time_surface, (screen_width // 2 - survival_time_surface.get_width() // 2, screen_height // 4 + 70))
        screen.blit(restart_surface, (screen_width // 2 - restart_surface.get_width() // 2, screen_height * 3 // 4 - 20))
        screen.blit(quit_surface, (screen_width // 2 - quit_surface.get_width() // 2, screen_height * 3 // 4 + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if won:  # If the game was won, restart the background music
                        pygame.mixer.music.play(-1)  # Restart background music
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Reset game variables
# Define constants at the top
level_message_display_time = 2000  # Duration for displaying level message in milliseconds

# Reset game variables
def reset_game():
    global level, survival_time, junk_speed, level_message, level_message_start_time, show_level_message
    level = 0
    survival_time = 0
    junk_speed = 2
    level_message_display_time = 2000
    level_message = ""
    level_message_start_time = 0
    show_level_message = False

# Main game function
def main():
    global level, survival_time, junk_speed, level_message, level_message_start_time, show_level_message

    reset_game()

    # Define level progression interval (30 seconds per level)
    level_duration_ms = 30000

    all_sprites = pygame.sprite.Group()
    junk_group = pygame.sprite.Group()

    clock = pygame.time.Clock()

    # Load and play background music
    pygame.mixer.music.load("space-ranger.mp3")  # Ensure you have the right file name
    pygame.mixer.music.play(-1)  # Play the music indefinitely

    # Load collision sound
    collision_sound = pygame.mixer.Sound("collision_sound.wav")  # Make sure this file exists

    while True:
        show_start_menu()
        player = Player()
        all_sprites.add(player)

        start_time = pygame.time.get_ticks()  # Track start time for level progression

        while True:
            # Randomly spawn space junk
            if random.random() < 0.02:
                junk = SpaceJunk()
                all_sprites.add(junk)
                junk_group.add(junk)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            all_sprites.update()

            # Check for collisions and play sound
            if pygame.sprite.spritecollideany(player, junk_group):
                collision_sound.play()  # Play collision sound
                break  # End the game loop if player collides with junk

            survival_time += clock.get_time()

            # Level progression every 30 seconds
            elapsed_level_time = pygame.time.get_ticks() - start_time
            if elapsed_level_time > level_duration_ms and level < 3:  # Limit levels to 4
                level += 1
                start_time = pygame.time.get_ticks()  # Reset start time for new level
                junk_speed += 1  # Increase junk speed each level
                # Update level message with names
                level_message = f"Level {level + 1}: " + ["Ignition Lift-Off", "Lunar Ascent", "Marsbound Orbit", "Mars Landing"][level]
                show_level_message = True
                level_message_start_time = pygame.time.get_ticks()  # Track level message start time

            # Render the current level background (up to level 3)
            screen.blit(backgrounds[level], (0, 0))
            all_sprites.draw(screen)

            # Display survival time
            font = pygame.font.SysFont(None, 36)
            survival_text = font.render(f"Time: {survival_time // 1000} s", True, WHITE)
            screen.blit(survival_text, (10, 10))

            # Display level message with left-to-right float effect
            if show_level_message:
                if pygame.time.get_ticks() - level_message_start_time < level_message_display_time:
                    # Calculate horizontal position for floating effect
                    message_position_x = (pygame.time.get_ticks() - level_message_start_time) // 5 % screen_width
                    level_surface = font.render(level_message, True, BLUE)
                    screen.blit(level_surface, (message_position_x, screen_height // 4))
                else:
                    show_level_message = False

            pygame.display.flip()
            clock.tick(60)

        # Check if all levels are complete
        won = level >= 3
        if show_game_over(survival_time, won):
            reset_game()
            all_sprites.empty()
            junk_group.empty()

if __name__ == "__main__":
    main()


