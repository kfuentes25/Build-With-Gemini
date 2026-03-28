import os, io
from google import genai
from google.genai import types
from PIL import Image, ImageOps, ImageFilter
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_maze_assets(theme, room_data):
    for (x, y), r_type in room_data.items():
        name = "Key Room" if r_type == 1 else ("Portal" if r_type == 2 else "Hallway")
        prompt = f"Isometric 3D dungeon {name} made of {theme}. High-angle overhead view, stone floor, four walls, no characters."
        
        res = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[prompt],
            config=types.GenerateContentConfig(response_modalities=["Image"])
        )
        img_bytes = res.candidates[0].content.parts[0].inline_data.data
        with open(f"room_{x}_{y}.png", "wb") as f: f.write(img_bytes)

def get_hero(theme):
    prompt = f"2D top-down RPG hero for a {theme} world. Saturated colors, white background."
    res = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["Image"])
    )
    img = Image.open(io.BytesIO(res.candidates[0].content.parts[0].inline_data.data)).convert("RGBA")
    
    # Transparency + Glow
    datas = img.getdata()
    newData = [ (0,0,0,0) if d[0]>210 and d[1]>210 and d[2]>210 else d for d in datas ]
    img.putdata(newData)
    
    alpha = img.getchannel('A')
    mask = ImageOps.expand(alpha, border=4, fill=0).filter(ImageFilter.GaussianBlur(1))
    glow = Image.new("RGBA", (img.size[0]+8, img.size[1]+8), (255, 255, 0, 255))
    glow.putalpha(mask)
    glow.paste(img, (4, 4), img)
    glow.save("player_hero.png")