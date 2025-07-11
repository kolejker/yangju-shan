import discord
import yt_dlp
import random
import asyncio
import json
import os
import subprocess

TOKEN = 'no'
CHANNEL_ID = no
CHANNELS = [
    'https://www.youtube.com/@LeKaiJumpen',
    'https://www.youtube.com/@chanjunshan',
]

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class MyClient(discord.Client):
    async def setup_hook(self):
        self.random_msg_task = self.loop.create_task(self.send_random_message())

    async def on_ready(self):
        print(f'welcome to the experience')

    async def send_random_message(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)

        if channel is None:
            return

        with open('strings.json', 'r') as f:
            strings = json.load(f)

        while not self.is_closed():
            message = random.choice(strings)
            await channel.send(message)
            await asyncio.sleep(1000)  

    async def on_message(self, message):
        if message.author.bot:
            return

        if self.user in message.mentions:
            if "jumpstyle" in message.content.lower():
                await message.channel.send("jumpstyle loading plz , processing powered by AMD GX-217GA, thank you lisa su", file=discord.File("image.jpg"))
                try:
                    video_url = await self.get_random_video_url()
                    filename = await self.download_and_compress(video_url)
                    if filename:
                        await message.channel.send(file=discord.File(filename))
                        os.remove(filename)
                    else:
                        await message.channel.send("fuck")
                except Exception as e:
                    await message.channel.send(f"my mother once said: {str(e)}")
            elif "neofetch" in message.content.lower():
                await message.channel.send(f"""\
                                              byakuren@server 
                             ....             --------------- 
              .',:clooo:  .:looooo:.          OS: Red Star OS x86_64 
           .;looooooooc  .oooooooooo'         Host: HP t420 Dual Core TC 
        .;looooool:,''.  :ooooooooooc         Kernel: 3.6.9-63-salakau 
       ;looool;.         'oooooooooo,         Uptime: 1 decade 
      ;clool'             .cooooooc.  ,,      Packages: 897 (pingas)
         ...                ......  .:oo,     Shell: discord 1.1.1
  .;clol:,.                        .loooo'    Terminal: /dev/pts/1 
 :ooooooooo,                        'ooool    CPU: AMD GX-217GA SOC (2) @ 1.6GHz 
'ooooooooooo.                        loooo.   GPU: ATI Radeon HD 8280E 
'ooooooooool                         coooo.   Memory: 0.60 GiB / 128 GiB (0%) 
 ,loooooooc.                        .loooo.   Network: 10 Gbps 
   .,;;;'.                          ;ooooc    BIOS: China Telecom 2.9 (05/04/2015) 
       ...                         ,ooool. 
    .cooooc.              ..',,'.  .cooo.                             
      ;ooooo:.           ;oooooooc.  :l.                              
       .coooooc,..      coooooooooo.       
         .:ooooooolc:. .ooooooooooo'       
           .':loooooo;  ,oooooooooc        
               ..';::c'  .;loooo:'         
                             .             
""")
            elif "play " in message.content.lower():
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
            else:
                await message.channel.send(f"Hello {message.author.mention},   youre a   狗娘养的吃 penis")

    async def get_random_video_url(self):
        channel_url = random.choice(CHANNELS)

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)

        video_entries = info.get('entries', [])
        if not video_entries:
            raise Exception("No videos found")

        video = random.choice(video_entries)
        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        return video_url

    async def download_and_compress(self, video_url):
        temp_filename = 'video.mp4'
        compressed_filename = 'compressed_video.mp4'

        ydl_opts = {
            'format': 'bestvideo[height<=240]+bestaudio/best[height<=240]/best[height<=240]/best',
            'outtmpl': temp_filename,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        size_bytes = os.path.getsize(temp_filename)
        if size_bytes <= 10 * 1024 * 1024:
            return temp_filename

        ydl_opts_info = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(video_url, download=False)
        duration = info.get('duration', 60)
        target_bitrate = (10 * 1024 * 1024 * 8) / duration
        target_bitrate_k = target_bitrate / 1000

        cmd = [
            'ffmpeg', '-y', '-i', temp_filename,
            '-b:v', f'{int(target_bitrate_k)}k',
            '-bufsize', f'{int(target_bitrate_k)}k',
            '-maxrate', f'{int(target_bitrate_k)}k',
            compressed_filename
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(compressed_filename) and os.path.getsize(compressed_filename) <= 10 * 1024 * 1024:
            os.remove(temp_filename)
            return compressed_filename
        else:
            if os.path.getsize(temp_filename) <= 10 * 1024 * 1024:
                os.remove(compressed_filename)
                return temp_filename
            os.remove(temp_filename)
            if os.path.exists(compressed_filename):
                os.remove(compressed_filename)
            return None


async def main():
    client = MyClient(intents=intents)
    await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())