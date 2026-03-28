import pygame
import os
import time
from world_engine import GlobeGrid
from agent_manager import get_tile_image, get_character_sprite

# --- CONFIG ---
SCREEN_SIZE = 800
PLAYER_SIZE = 120

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Globe-Grid: WASD Edition")
    font = pygame.font.SysFont("Arial", 28)

    # 1. INITIAL INPUT
    theme = input("Describe your starting biome (e.g., 'Purple Alien Forest'): ")
    
    # 2. INITIAL LOADING (Hero)
    screen.fill((20, 20, 20))
    load_msg = font.render(f"Summoning Hero for {theme}...", True, (200, 200, 200))
    screen.blit(load_msg, (SCREEN_SIZE//4, SCREEN_SIZE//2))
    pygame.display.flip()
    
    get_character_sprite(theme)
    player_img = pygame.image.load("player_hero.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))

    # 3. INITIAL MAP GENERATION
    game = GlobeGrid(size=10, theme=theme)
    get_tile_image(game.get_state()['prompt'])
    map_img = pygame.image.load("current_tile.png").convert()
    map_img = pygame.transform.scale(map_img, (SCREEN_SIZE, SCREEN_SIZE))

    running = True
    while running:
        # DRAW
        screen.blit(map_img, (0, 0))
        screen.blit(player_img, (SCREEN_SIZE//2 - PLAYER_SIZE//2, SCREEN_SIZE//2 - PLAYER_SIZE//2))
        
        # UI OVERLAY
        ui_bg = pygame.Surface((300, 40))
        ui_bg.set_alpha(150)
        ui_bg.fill((0, 0, 0))
        screen.blit(ui_bg, (10, 10))
        
        stats = font.render(f"Pos: {game.x},{game.y} | Keys: {len(game.inventory)}/3", True, (255, 255, 255))
        screen.blit(stats, (20, 15))
        
        pygame.display.flip()

        # INPUT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                move = None
                if event.key == pygame.K_w: move = "north"
                elif event.key == pygame.K_s: move = "south"
                elif event.key == pygame.K_d: move = "east"
                elif event.key == pygame.K_a: move = "west"

                if move:
                    # RENDER LOADING SCREEN
                    screen.fill((10, 10, 10))
                    loading = font.render("Gemini is dreaming the next room...", True, (200, 200, 200))
                    screen.blit(loading, (SCREEN_SIZE//4, SCREEN_SIZE//2))
                    pygame.display.flip()

                    # UPDATE STATE & AI
                    state = game.move(move)
                    try:
                        get_tile_image(state['prompt'])
                        map_img = pygame.image.load("current_tile.png").convert()
                        map_img = pygame.transform.scale(map_img, (SCREEN_SIZE, SCREEN_SIZE))
                        
                        if state['item_found'] and state['item_found'] not in game.inventory:
                            print(f"Found {state['item_found']}!")
                            game.inventory.append(state['item_found'])
                    except Exception as e:
                        print(f"Quota error: {e}")
                        time.sleep(5)

        if len(game.inventory) >= 3:
            print("YOU ESCAPED!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    run_game()