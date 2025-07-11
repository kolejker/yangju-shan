import discord
import yt_dlp
import random
import os
import subprocess
from utils import get_random_video_url, download_and_compress

CHANNELS = [
    'https://www.youtube.com/@LeKaiJumpen',
    'https://www.youtube.com/@chanjunshan',
    'https://www.youtube.com/@terrorjump',
    'https://www.youtube.com/@pyo666',
    'https://www.youtube.com/@dezenaamniet',
    'https://www.youtube.com/@StarkOwnStyle',
    'https://www.youtube.com/@GoShowtek',
    'https://www.youtube.com/@madawards09',
    'https://www.youtube.com/@JumpstyleIsHoly',
    'https://www.youtube.com/@xBeStDeViLx',
    'https://www.youtube.com/@shahjumper',
    'https://www.youtube.com/@ZeroJump4Life'
]

async def handle_jumpstyle(message):
    await message.channel.send("jumpstyle loading plz , processing powered by AMD GX-217GA, thank you lisa su", file=discord.File("image.jpg"))
    
    try:
        video_url = await get_random_video_url(CHANNELS)
        filename = await download_and_compress(video_url)
        
        if filename:
            await message.channel.send(file=discord.File(filename))
            os.remove(filename)
        else:
            await message.channel.send("fuck")
    except Exception as e:
        await message.channel.send(f"my mother once said: {str(e)}")