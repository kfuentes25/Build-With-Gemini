import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load API Key with safety check
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found! Ensure .env contains GOOGLE_API_KEY=your_key")

client = genai.Client(api_key=API_KEY)

# 2. The Generation Function
def generate_game_assets(theme_text):
    """Generates 1 Theme and 4 SFX based on the input text."""
    print(f"Processing new theme: {theme_text}")
    
    # Generate Theme (using Lyria 3 Pro)
    try:
        theme_resp = client.models.generate_content(
            model="lyria-3-pro-preview",
            contents=f"Full game theme music: {theme_text}",
            config=types.GenerateContentConfig(response_modalities=["AUDIO"])
        )
        save_audio(theme_resp, f"theme_generated.mp3")
        
        # Generate 3 Goal SFX + 1 Exit SFX (using Lyria 3 Clip)
        sfx_types = ["goal 1 chime", "goal 2 chime", "goal 3 triumph", "level exit door"]
        for i, sfx_name in enumerate(sfx_types):
            sfx_resp = client.models.generate_content(
                model="lyria-3-clip-preview",
                contents=f"SFX for {sfx_name} in a {theme_text} game",
                config=types.GenerateContentConfig(response_modalities=["AUDIO"])
            )
            save_audio(sfx_resp, f"sfx_{i+1}.mp3")
            
        print("All assets generated successfully.")
    except Exception as e:
        print(f"Generation failed: {e}")

def save_audio(response, filename):
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            with open(filename, "wb") as f:
                f.write(part.inline_data.data)
            print(f"Saved {filename}")

# 3. The "Watcher" Loop and stuff
def watch_for_file(filepath):
    print(f"Watching for changes in {filepath}...")
    last_mtime = 0
     
    while True:
        if os.path.exists(filepath):
            current_mtime = os.path.getmtime(filepath)
            if current_mtime > last_mtime:
                with open(filepath, 'r') as f:
                    content = f.read().strip()
                if content:
                    generate_game_assets(content)
                last_mtime = current_mtime
        time.sleep(2) # Check every 2 seconds

if __name__ == "__main__":
    # This will wait for a file named 'input_theme.txt' to appear in your folder
    watch_for_file("input_theme.txt")