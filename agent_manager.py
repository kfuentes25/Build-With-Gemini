import os
import json
from io import BytesIO
from PIL import Image, ImageFilter
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

GODOT_FOLDER = "dungeon-gemini--game-3d" 

def get_level_music(theme):
    os.makedirs(GODOT_FOLDER, exist_ok=True)
    filename = os.path.join(GODOT_FOLDER, "level_music.mp3")
    music_prompt = f"Atmospheric loop for {theme}. Include sounds of water, wind, or nature. Gritty and moody."
    try:
        res = client.models.generate_content(
            model="lyria-3-clip-preview",
            contents=[music_prompt],
            config=types.GenerateContentConfig(response_modalities=["AUDIO"])
        )
        for part in res.parts:
            if part.inline_data:
                with open(filename, "wb") as f:
                    f.write(part.inline_data.data)
                return True
        return False
    except: return False

def generate_level_from_visual(theme): 
    os.makedirs(GODOT_FOLDER, exist_ok=True)
    concept_path = os.path.join(GODOT_FOLDER, "concept_art.jpg")
    layout_path = os.path.join(GODOT_FOLDER, "layout.json")
    
    print(f"🖼️  Artist: Painting '{theme}'...")
    # Dynamic prompt: Bold, no volcanoes unless requested.
    artist_prompt = f"A strictly top-down 2D pixel-art map of {theme}. Solid chunky colors. 16:9 ratio. NO borders, NO text. High-contrast colors."
    
    try:
        image_res = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[artist_prompt],
            config=types.GenerateContentConfig(response_modalities=["Image"])
        )
        img_data = image_res.candidates[0].content.parts[0].inline_data.data
        with open(concept_path, "wb") as f:
            f.write(img_data)
        
        print(f"🗺️  Architect: Identifying terrain heights...")
        # RESTORED: Your original height mapping logic
        architect_prompt = f"""Identify the colors in this map. 
        Assign heights: Water=1, Sand=1, Floor=2, Forests=4, Mountain=6, Peak=8.
        Output ONLY raw JSON list: [{{"hex": "#color", "h": height}}]
        """

        res = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[types.Part.from_bytes(data=img_data, mime_type="image/jpeg"), architect_prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        legend = json.loads(res.text[res.text.find('['):res.text.rfind(']')+1])
        image = Image.open(BytesIO(img_data)).filter(ImageFilter.MedianFilter(size=5))
        
        GRID_W = 60 
        small_img = image.resize((GRID_W, int(GRID_W * 0.56)), Image.Resampling.NEAREST).convert("RGB")
        pixels = small_img.load()
        
        grid_array = []
        for y in range(small_img.height):
            row = []
            for x in range(small_img.width):
                r, g, b = pixels[x, y]
                min_dist, best_h, best_hex = float('inf'), 2, f"#{r:02x}{g:02x}{b:02x}"
                for item in legend:
                    lr, lg, lb = tuple(int(item["hex"].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                    dist = (r-lr)**2 + (g-lg)**2 + (b-lb)**2
                    if dist < min_dist:
                        min_dist, best_h, best_hex = dist, item.get("h", 2), item.get("hex")
                row.append([best_h, best_hex])
            grid_array.append(row)

        with open(layout_path, "w") as f:
            json.dump({"grid": grid_array}, f)
            
        get_level_music(theme)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False