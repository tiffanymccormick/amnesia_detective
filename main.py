import sys
import pygame
import os

# Try to keep localSetUp if your env needs it; ignore if missing
try:
    import localSetUp  # noqa
except Exception:
    pass

# --------------- Config ---------------
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = (128, 128)
PLAYER_SPEED = 5
TEXT_BOX_HEIGHT = 100               # UI text area height
TOP_OF_TEXT_Y = HEIGHT - TEXT_BOX_HEIGHT
ABOVE_TEXT_BOX_HEIGHT = 20          # collision strip just above the text box
END_BOX_WIDTH = 40                  # left/right teleport boxes width

# --------------- Helpers ---------------
def load_scaled_image_any(name_no_ext, screen_size):
    """Tries .jpg then .png for base name; returns scaled Surface or None."""
    jpg = f"{name_no_ext}.jpg"
    png = f"{name_no_ext}.png"
    surf = None
    if os.path.exists(jpg):
        surf = pygame.image.load(jpg).convert()
    elif os.path.exists(png):
        surf = pygame.image.load(png).convert_alpha()
    if surf:
        surf = pygame.transform.scale(surf, screen_size)
    return surf

def draw_text(surface, text, pos, font, color=(255, 255, 255)):
    txt = font.render(text, True, color)
    surface.blit(txt, pos)

# --------------- Main ---------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WASD Image Movement + Text Box")
    clock = pygame.time.Clock()

    # Scenes:
    #  1  = bedroom (WASD)
    # -1  = hall1 (A/D only)
    #  2  = placeholder (WASD)
    scene_num = 1

    # Assets
    bg_bedroom = load_scaled_image_any("bedroom", (WIDTH, HEIGHT))
    bg_hall1   = load_scaled_image_any("hall1", (WIDTH, HEIGHT))

    player_img = pygame.image.load("test.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, PLAYER_SIZE)
    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    font = pygame.font.Font(None, 36)
    texts = [
        "**Victor Hyde:** wakes in his gothic castle.",
        "**Butler:** enters the bedroom a bloody mess and says Opheila was murdered.",
        "**Victor Hyde:** rage quits and the butler rushes out.",
        "**Narrator:** there is a knock on the door; Hyde opens it.",
        "**Mailman:** has a letter for Opheila. It is the PDF."
    ]
    text_index = 0

    # Collision geometry
    # Strip directly above the text box (this is what should trigger hall scene)
    above_text_rect = pygame.Rect(0, TOP_OF_TEXT_Y - ABOVE_TEXT_BOX_HEIGHT, WIDTH, ABOVE_TEXT_BOX_HEIGHT)
    # End teleport boxes for the hall scene (-1)
    left_end_box  = pygame.Rect(0, 0, END_BOX_WIDTH, TOP_OF_TEXT_Y - ABOVE_TEXT_BOX_HEIGHT)
    right_end_box = pygame.Rect(WIDTH - END_BOX_WIDTH, 0, END_BOX_WIDTH, TOP_OF_TEXT_Y - ABOVE_TEXT_BOX_HEIGHT)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and scene_num == 1:
                    text_index = (text_index + 1) % len(texts)
                # DEBUG quick scene switches (optional)
                elif event.key == pygame.K_1:
                    scene_num = 1
                elif event.key == pygame.K_MINUS:  # '-' key
                    scene_num = -1
                elif event.key == pygame.K_2:
                    scene_num = 2

        # --- Movement ---
        keys = pygame.key.get_pressed()
        if scene_num == -1:
            # HALL: A/D only
            if keys[pygame.K_a]:
                player_rect.x -= PLAYER_SPEED
            if keys[pygame.K_d]:
                player_rect.x += PLAYER_SPEED
        else:
            # Other scenes: WASD
            if keys[pygame.K_w]:
                player_rect.y -= PLAYER_SPEED
            if keys[pygame.K_s]:
                player_rect.y += PLAYER_SPEED
            if keys[pygame.K_a]:
                player_rect.x -= PLAYER_SPEED
            if keys[pygame.K_d]:
                player_rect.x += PLAYER_SPEED

        # Keep on screen
        player_rect.clamp_ip(screen.get_rect())

        # --- Scene-specific collisions ---
        if scene_num == 1:
            # TOUCH THE STRIP ABOVE THE TEXT BOX -> go to HALL (-1)
            if player_rect.colliderect(above_text_rect):
                scene_num = -1
                # Place player near center-bottom of hall
                player_rect.midbottom = (WIDTH // 2, TOP_OF_TEXT_Y - 2)
                print("Entered Hall (-1) from bedroom.")
        elif scene_num == -1:
            # Left end -> scene 1; right end -> scene 2
            if player_rect.colliderect(left_end_box):
                scene_num = 1
                player_rect.midbottom = (WIDTH - END_BOX_WIDTH - 20, TOP_OF_TEXT_Y - 2)
                print("Teleport: left end -> Scene 1")
            elif player_rect.colliderect(right_end_box):
                scene_num = 2
                player_rect.midbottom = (END_BOX_WIDTH + 20, TOP_OF_TEXT_Y - 2)
                print("Teleport: right end -> Scene 2")

        # --- DRAW ---
        if scene_num == 1:
            # BEDROOM
            if bg_bedroom:
                screen.blit(bg_bedroom, (0, 0))
            else:
                screen.fill((30, 30, 30))

            # Player
            screen.blit(player_img, player_rect)

            # Text box UI
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)

            # The strip above the text box (collision trigger to hall)
            pygame.draw.rect(screen, (0, 0, 0), above_text_rect)

            # Current line
            draw_text(screen, texts[text_index], (20, TOP_OF_TEXT_Y + 30), font)

        elif scene_num == -1:
            # HALL 1 (A/D only)
            if bg_hall1:
                screen.blit(bg_hall1, (0, 0))
            else:
                screen.fill((20, 20, 25))

            # End boxes (left & right) – teleport triggers
            pygame.draw.rect(screen, (0, 0, 0), left_end_box)
            pygame.draw.rect(screen, (0, 0, 0), right_end_box)

            # Strip above text box (visual consistency)
            pygame.draw.rect(screen, (0, 0, 0), above_text_rect)

            # Player
            screen.blit(player_img, player_rect)

            # Text box UI
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Hall 1: A/D to move. Left box -> 1 | Right box -> 2", (20, TOP_OF_TEXT_Y + 30), font)

        else:
            # SCENE 2 (placeholder)
            screen.fill((15, 15, 20))

            # Strip above text box
            pygame.draw.rect(screen, (0, 0, 0), above_text_rect)

            # Player
            screen.blit(player_img, player_rect)

            # Text box UI
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Scene 2 (placeholder). Press ESC to quit.", (20, TOP_OF_TEXT_Y + 30), font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
