import pygame, os
from google import genai

def generate_music(client, theme):
    try:
        res = client.models.generate_content(
            model="lyria-3-clip-preview",
            contents=[f"Dark atmospheric dungeon synth for {theme}."],
            config=types.GenerateContentConfig(response_modalities=["AUDIO"])
        )
        with open("music.mp3", "wb") as f: 
            f.write(res.candidates[0].content.parts[0].inline_data.data)
        return "music.mp3"
    except: return None

def play_bgm(file):
    if file and os.path.exists(file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)