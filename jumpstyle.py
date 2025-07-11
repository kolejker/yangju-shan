import discord
import yt_dlp
import random
import os
import subprocess
from utils import get_random_video_url, download_and_compress

CHANNELS = [
    'https://www.youtube.com/@LeKaiJumpen',
    'https://www.youtube.com/@chanjunshan',
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