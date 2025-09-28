import sys
import pygame
import os

# Try to keep localSetUp if your env needs it; ignore if missing
try:
    import localSetUp  # noqa
except Exception:
    pass

# --------------- Config ---------------
WIDTH, HEIGHT = 600, 600
FPS = 60
PLAYER_SIZE = (128, 128)
PLAYER_SIZE_INCR = (250, 250)
PLAYER_SPEED = 2
TEXT_BOX_HEIGHT = 100               # UI text area height
TOP_OF_TEXT_Y = HEIGHT - TEXT_BOX_HEIGHT
ABOVE_TEXT_BOX_HEIGHT = 20          # collision strip just above the text box
END_BOX_WIDTH = 40                  # left/right teleport boxes width
BOARD_DIMENSIONS = (300, 150, 200, 100)
STICKY_WIDTH = 100
STICKY_HEIGHT = 100
STICKY_X_POS = 75
STICKY_Y_POS = 215

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
    # -1  = hall1 (A/D only, hub)
    #  2  = letter_room (WASD)
    #  3  = portrait (placeholder)
    #  4  = scene4 (placeholder)
    #  5  = scene5 (placeholder)
    scene_num = 1

    # Assets
    bg_bedroom     = load_scaled_image_any("bedroom", (WIDTH, HEIGHT))
    bg_hall1       = load_scaled_image_any("hall1", (WIDTH, HEIGHT))
    bg_letter_room = load_scaled_image_any("letter_room", (WIDTH, HEIGHT))
    bg_portrait    = load_scaled_image_any("portrait", (WIDTH, HEIGHT))
    bg_office      = load_scaled_image_any("office", (WIDTH, HEIGHT))
    bg_corkboard  = load_scaled_image_any("corkboard", (WIDTH, HEIGHT))
    bg_scene5      = load_scaled_image_any("scene5", (WIDTH, HEIGHT))   # NEW placeholder

    player_img = pygame.image.load("test.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, PLAYER_SIZE)
    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    font = pygame.font.Font('antiquity-print.ttf', 18)
    texts = [
        "**Victor Hyde:** wakes in his gothic castle.".lower(),
        "**Butler:** enters the bedroom a bloody mess and says Opheila was murdered.".lower(),
        "**Victor Hyde:** rage quits and the butler rushes out.".lower(),
        "**Narrator:** there is a knock on the door; Hyde opens it.".lower(),
        "**Mailman:** has a letter for Opheila. It is the PDF.".lower()
    ]
    text_index = 0

    # Collision geometry
    above_text_rect = pygame.Rect(0, TOP_OF_TEXT_Y - ABOVE_TEXT_BOX_HEIGHT, WIDTH, ABOVE_TEXT_BOX_HEIGHT)
    left_end_box  = pygame.Rect(0, 0, END_BOX_WIDTH, TOP_OF_TEXT_Y - ABOVE_TEXT_BOX_HEIGHT)
    right_end_box = pygame.Rect(WIDTH - END_BOX_WIDTH, 0, END_BOX_WIDTH, TOP_OF_TEXT_Y - ABOVE_TEXT_BOX_HEIGHT) 
    board_box = pygame.Rect(BOARD_DIMENSIONS)
    sticky_rect = pygame.Rect(STICKY_X_POS, STICKY_Y_POS, STICKY_WIDTH, STICKY_HEIGHT)

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
                # DEBUG quick scene switches
                elif event.key == pygame.K_1:
                    scene_num = 1
                elif event.key == pygame.K_MINUS:  # '-' key
                    scene_num = -1
                elif event.key == pygame.K_2:
                    scene_num = 2
                elif event.key == pygame.K_3:
                    scene_num = 3
                elif event.key == pygame.K_4:
                    scene_num = 4
                elif event.key == pygame.K_5:
                    scene_num = 5

        # --- Movement ---
        keys = pygame.key.get_pressed()
        if scene_num == -1:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_rect.x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_rect.x += PLAYER_SPEED
        else:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_rect.y -= PLAYER_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_rect.y += PLAYER_SPEED
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_rect.x -= PLAYER_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_rect.x += PLAYER_SPEED

        # Keep on screen
        player_rect.clamp_ip(screen.get_rect())

        # --- Scene-specific collisions ---
        if scene_num == 1:
            if player_rect.colliderect(above_text_rect):
                scene_num = -1
                player_rect.midbottom = (WIDTH // 2, TOP_OF_TEXT_Y - 2)
                print("Entered Hall (-1) from bedroom.")
        elif scene_num == -1:
            # left -> scene 1, right -> scene 2
            if player_rect.colliderect(left_end_box):
                scene_num = 1
                player_rect.midbottom = (WIDTH - END_BOX_WIDTH - 20, TOP_OF_TEXT_Y - 2)
                print("Teleport: left end -> Scene 1")
            elif player_rect.colliderect(right_end_box):
                scene_num = 2
                player_rect.midbottom = (END_BOX_WIDTH + 20, TOP_OF_TEXT_Y - 2)
                print("Teleport: right end -> Scene 2")
        elif scene_num == 2:
            # enter hall again via strip
            if player_rect.colliderect(above_text_rect):
                scene_num = 3
                player_rect.midbottom = (WIDTH // 2, TOP_OF_TEXT_Y - 2)
                print("Went to hall 3 from Scene 2")
        elif scene_num == 3:
            # move right -> scene 4
            if player_rect.colliderect(right_end_box):
                scene_num = 4
                player_rect.midbottom = (END_BOX_WIDTH + 20, TOP_OF_TEXT_Y - 2)
                print("Teleport: Scene 3 -> Scene 4")
            # move left -> hall
            elif player_rect.colliderect(left_end_box):
                scene_num = 2
                player_rect.midbottom = (WIDTH - END_BOX_WIDTH - 20, TOP_OF_TEXT_Y - 2)
                print("Teleport: Scene 3 -> 2")
        elif scene_num == 4:
            # move right -> scene 5
            if player_rect.colliderect(right_end_box):
                scene_num = 5
                player_rect.midbottom = (END_BOX_WIDTH + 20, TOP_OF_TEXT_Y - 2)
                print("Teleport: Scene 4 -> Scene 5")
            elif player_rect.colliderect(board_box):
                scene_num = 10


        # --- DRAW ---
        if scene_num == 1:
            if bg_bedroom:
                screen.blit(bg_bedroom, (0, 0))
            else:
                screen.fill((30, 30, 30))
            screen.blit(player_img, player_rect)
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            pygame.draw.rect(screen, (0, 0, 0), above_text_rect)
            draw_text(screen, texts[text_index], (20, TOP_OF_TEXT_Y + 30), font)

        elif scene_num == -1:
            if bg_hall1:
                screen.blit(bg_hall1, (0, 0))
            else:
                screen.fill((20, 20, 25))
            pygame.draw.rect(screen, (0, 0, 0), left_end_box)
            pygame.draw.rect(screen, (0, 0, 0), right_end_box)
            pygame.draw.rect(screen, (0, 0, 0), above_text_rect)
            screen.blit(player_img, player_rect)
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Hall 1: Left->1 | Right->2. (Extra exits lead to 4/5).", (20, TOP_OF_TEXT_Y + 30), font)

        elif scene_num == 2:
            if bg_letter_room:
                screen.blit(bg_letter_room, (0, 0))
            else:
                screen.fill((20, 20, 25))
            pygame.draw.rect(screen, (0, 0, 0), above_text_rect)
            screen.blit(player_img, player_rect)
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Scene 2 (letter room). Walk up to return to hall.", (20, TOP_OF_TEXT_Y + 30), font)

        elif scene_num == 3:
            if bg_portrait:
                screen.blit(bg_portrait, (0, 0))
            else:
                screen.fill((20, 20, 25))
            pygame.draw.rect(screen, (0, 0, 0), above_text_rect)
            screen.blit(player_img, player_rect)
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Scene 3 (portrait). Placeholder text.", (20, TOP_OF_TEXT_Y + 30), font)

        elif scene_num == 4:
            if bg_office:
                screen.blit(bg_office, (0, 0))
            else:
                screen.fill((25, 15, 35))
            pygame.draw.rect(screen, (0, 0, 0), left_end_box)
            pygame.draw.rect(screen, (0, 0, 0), right_end_box)
            pygame.Rect(BOARD_DIMENSIONS)
            screen.blit(player_img, player_rect)
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Scene 4. Left->Hall | Right->5", (20, TOP_OF_TEXT_Y + 30), font)
            player_img = pygame.transform.scale(player_img, PLAYER_SIZE_INCR)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if board_box.collidepoint(event.pos):
                    print("Box clicked! Switching scene...")
                    scene_num = 10
                
        # Scence after coarkboard is clicked (click sticky to exit)
        elif scene_num == 10:
            if bg_office:
                screen.blit(bg_corkboard, (0, 0))
            else:
                screen.fill((35, 20, 20))
            above_text_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Interact with the sticky note.", (20, TOP_OF_TEXT_Y + 30), font)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if  sticky_rect.collidepoint(event.pos):
                    print("Box clicked! Switching scene...")
                    scene_num = 4


        elif scene_num == 5:
            if bg_scene5:
                screen.blit(bg_scene5, (0, 0))
            else:
                screen.fill((35, 20, 20))
            pygame.draw.rect(screen, (0, 0, 0), left_end_box)
            screen.blit(player_img, player_rect)
            text_box_rect = pygame.Rect(0, TOP_OF_TEXT_Y, WIDTH, TEXT_BOX_HEIGHT)
            pygame.draw.rect(screen, (0, 0, 0), text_box_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_box_rect, 2)
            draw_text(screen, "Scene 5. Final scene.", (20, TOP_OF_TEXT_Y + 30), font)
            player_img = pygame.transform.scale(player_img, PLAYER_SIZE)
        


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
