import os
import asyncio
from dotenv import load_dotenv
from world_engine import GlobeGrid
# Assuming you put the API functions in ai_manager.py
from agent_manager import get_tile_image, get_background_music

load_dotenv()

async def play_game():
    # 1. Initialize the World
    theme = os.getenv("GAME_THEME", "Bioluminescent Deep Sea")
    game = GlobeGrid(size=10, theme=theme)
    
    print(f"--- Welcome to Globe-Grid: {theme} ---")
    print("Commands: north, south, east, west, quit")

    # 2. Start the Music (Lyria 3)
    get_background_music(theme) 

    while len(game.inventory) < 3:
        action = input(f"\n[Pos: {game.x},{game.y}] Where to? ").lower()
        
        if action == 'quit':
            break
        
        if action in ["north", "south", "east", "west"]:
            # Move on the Globe
            state = game.move(action)
            
            # 3. Generate the Image (Nano Banana 2)
            print(f"Generating view for {state['pos']}...")
            img = get_tile_image(state['prompt'])
            img.show() # This opens the photo on your Mac/Windows automatically
            
            # 4. Check for Items
            if state['item'] and state['item'] not in game.inventory:
                print(f"✨ FOUND ARTIFACT: {state['item']}!")
                game.inventory.append(state['item'])
                print(f"Inventory: {len(game.inventory)}/3")
        else:
            print("Invalid direction. Use north/south/east/west.")

    if len(game.inventory) == 3:
        print("\n🎉 ALL ARTIFACTS COLLECTED!")
        print("Generating Veo Escape Cinematic...")
        # get_victory_video(theme)

if __name__ == "__main__":
    asyncio.run(play_game())