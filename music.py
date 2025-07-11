import discord
import yt_dlp
import asyncio

async def handle_music(message):
    query = message.content.split("play", 1)[1].strip()
    await message.channel.send(f"look: `{query}`")

    try:
        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send("why arent u on call")
            return

        voice_channel = message.author.voice.channel

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch1',
            'skip_download': True,  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
            audio_url = None
            if 'entries' in info:
                audio_url = info['entries'][0]['url']
                title = info['entries'][0]['title']
            else:
                audio_url = info['url']
                title = info['title']

        vc = await voice_channel.connect()

        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'  
        }

        vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts), 
               after=lambda e: print("Finished playing."))
        
        await message.channel.send(f"play for you my love: **{title}**")

        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

    except Exception as e:
        await message.channel.send(f"my mother once said: {str(e)}")