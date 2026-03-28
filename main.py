import os
import time
from world_engine import GlobeGrid
from agent_manager import get_tile_image, get_character_sprite, get_background_music

def run_game():
    print("\n🌟 --- THE ADAPTIVE GENERATIVE GLOBE --- 🌟")
    
    current_theme = input("Describe your starting biome: ")
    
    while True: # Master World Loop
        # 1. GENERATE THE ADAPTIVE HERO
        try:
            hero_img = get_character_sprite(current_theme)
            hero_img.show()
            print(f"✅ An explorer of the {current_theme} has appeared!")
            print("⏳ Cooling down AI for 10 seconds...")
            time.sleep(10) # Prevent 429 error before first move
        except Exception as e:
            print(f"⚠️ Hero generation failed: {e}")

        game = GlobeGrid(size=10, theme=current_theme)
        print(f"\n🌍 --- ENTERING: {current_theme} --- 🌍")
        
        # 2. GENERATE MUSIC
        try:
            get_background_music(current_theme)
        except:
            pass

        # 3. NAVIGATION LOOP
        while len(game.inventory) < 3:
            print(f"\n📍 Position: ({game.x}, {game.y}) | Keys Found: {len(game.inventory)}/3")
            move = input("Move (north, south, east, west) or 'quit': ").lower()

            if move == 'quit': return
            if move in ["north", "south", "east", "west"]:
                state = game.move(move)
                try:
                    img = get_tile_image(state['prompt'])
                    img.show()
                    
                    if state['item_found']:
                        print(f"🔑 YOU FOUND A KEY: {state['item_found']}!")
                        game.inventory.append(state['item_found'])
                except Exception as e:
                    print(f"⚠️ AI Quota Hit. Wait 15s. Error: {e}")
                    time.sleep(15)
            else:
                print("Invalid command.")

        # 4. WIN & RESET
        print(f"\n🎉 ALL KEYS COLLECTED! You have escaped the {current_theme}!")
        choice = input("Enter a new biome? (y/n): ")
        if choice.lower() == 'y':
            current_theme = input("Describe the next biome: ")
        else:
            print("Safe travels, hero.")
            break

if __name__ == "__main__":
    run_game()