import time
import os
from agent_manager import generate_level_from_visual

GODOT_PROJECT_DIR = "dungeon-gemini--game-3d"
PROMPT_FILE = os.path.join(GODOT_PROJECT_DIR, "next_prompt.txt")

def main():
    print("========================================")
    print("🧙‍♂️ GEMINI WORLD-PAINTER (V2) 🧙‍♂️")
    print("========================================")
    
    theme = input("\nEnter Initial Theme: ").strip()
    generate_level_from_visual(theme)
    
    print("\n📡 Listening for requests from Godot...")

    while True:
        if os.path.exists(PROMPT_FILE):
            with open(PROMPT_FILE, "r") as f:
                new_theme = f.read().strip()
            
            if new_theme:
                print(f"✨ Generating: {new_theme}")
                if generate_level_from_visual(new_theme):
                    os.remove(PROMPT_FILE)
            else:
                os.remove(PROMPT_FILE)
        time.sleep(1)

if __name__ == "__main__":
    main()