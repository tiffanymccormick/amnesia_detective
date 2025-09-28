import sys
import pygame
import localSetUp

# set up
def main():
    # initizlie
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WASD Image Movement + Text Box")

    clock = pygame.time.Clock()

    # --- Load & Resize Image ---
    player_img = pygame.image.load("test.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (128, 128))
    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))    # --- Movement Settings ---
    
    speed = 5

    # --- storybox Setup ---
    font = pygame.font.Font(None, 36)
    text_box_height = 100
    text_index = 0

    # lines
    texts = [
        "**Victor Hyde:** wakes in his gothic castle.",
        "**Butler:** enters the bedroom a bloody mess and says Opheila was murdered.",
        "**Victor Hyde:** rage quits and the butler rushes out.",
        "**Narrator:** there is a knock on the door; Hyde opens it.",
        "**Mailman:** has a letter for Opheila. It is the PDF."
    ]    

    texts2 = ["Victor: This is where she would've been before, everything... ", "Rahhhh", "Victor: What was that?", "RAHHHHHHH", "Victor: Oh my days... that thing... that must had killed her", "Victor: Ophelias journals, what did she write about her killer?", "10/29/1897: Today lalala", "10/29/1897: Today lalala", "10/29/1897: Today lalala"]
    side2 = []

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # delta time (seconds)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    text_index = (text_index + 1) % len(texts)

        # --- Movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_rect.y -= speed
        if keys[pygame.K_s]:
            player_rect.y += speed
        if keys[pygame.K_a]:
            player_rect.x -= speed
        if keys[pygame.K_d]:
            player_rect.x += speed

        # Keep player on screen
        player_rect.clamp_ip(screen.get_rect())

        # --- Drawing ---
        screen.fill((30, 30, 30))  # background
        screen.blit(player_img, player_rect)

        # Draw text box (rectangle at bottom)
        text_box_rect = pygame.Rect(0, HEIGHT - text_box_height, WIDTH, text_box_height)
        pygame.draw.rect(screen, (0, 0, 0), text_box_rect)  # black background
        pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)  # white border

        # Draw current text
        text_surface = font.render(texts[text_index], True, (255, 255, 255))
        screen.blit(text_surface, (20, HEIGHT - text_box_height + 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
