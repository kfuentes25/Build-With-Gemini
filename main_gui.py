import os, warnings, pygame, sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

from world_engine import MazeEngine
from agent_manager import generate_maze_assets, get_hero, client
from sound_manager import generate_music, play_bgm
from animation_manager import Animator

SCREEN = 800
def run():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN, SCREEN))
    font = pygame.font.SysFont("Courier", 32, bold=True)

    theme = input("Dungeon Theme: ")
    game = MazeEngine()
    
    # 1. SETUP PHASE
    screen.fill((20,20,20))
    screen.blit(font.render("ARCHITECTING MAZE...", 1, (255,255,255)), (200, 400))
    pygame.display.flip()

    generate_maze_assets(theme, game.rooms)
    get_hero(theme)
    play_bgm(generate_music(client, theme))

    hero = pygame.transform.scale(pygame.image.load("player_hero.png"), (150, 150))

    while True:
        # 2. RENDER ROOM
        room_img = pygame.image.load(f"room_{game.x}_{game.y}.png")
        screen.blit(pygame.transform.scale(room_img, (SCREEN, SCREEN)), (0, 0))
        
        # 3. ANIMATED HERO
        screen.blit(hero, (SCREEN//2 - 75, SCREEN//2 - 75 + Animator.get_bob()))

        # HUD
        txt = font.render(f"KEYS: {len(game.inventory)}/3", 1, (255, 215, 0))
        screen.blit(txt, (300, 20))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                move = {pygame.K_w:"north", pygame.K_s:"south", pygame.K_a:"west", pygame.K_d:"east"}.get(e.key)
                if move and game.move(move):
                    if game.rooms[(game.x, game.y)] == 1 and (game.x, game.y) not in game.inventory:
                        game.inventory.append((game.x, game.y))

        if game.x == 2 and game.y == 2 and len(game.inventory) >= 3:
            print("VICTORY!"); break

if __name__ == "__main__": run()