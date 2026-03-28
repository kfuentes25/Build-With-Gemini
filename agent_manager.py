import os
import time
import io
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_character_sprite(theme, filename="player_hero.png"):
    print(f"🧙 Dreaming up a hero for the {theme}...")
    prompt = (
        f"A 2D top-down game sprite of a hero that belongs in a {theme}. "
        f"White background, overhead view, centered, high-detail game art."
    )
    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["Image"])
    )
    image_bytes = response.candidates[0].content.parts[0].inline_data.data
    img = Image.open(io.BytesIO(image_bytes))
    img.save(filename)
    return img

def get_tile_image(prompt, filename="current_tile.png"):
    print(f"🎨 Dreaming up the world...")
    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(response_modalities=["Image"])
    )
    image_bytes = response.candidates[0].content.parts[0].inline_data.data
    img = Image.open(io.BytesIO(image_bytes))
    img.save(filename)
    return img