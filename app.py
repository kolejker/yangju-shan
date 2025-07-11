import discord
import random
import asyncio
import json
from jumpstyle import handle_jumpstyle
from music import handle_music
from neofetch import handle_neofetch

TOKEN = 'no'
CHANNEL_ID = 1389730102627012650

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
                await handle_jumpstyle(message)
            elif "neofetch" in message.content.lower():
                await handle_neofetch(message)
            elif "play " in message.content.lower():
                await handle_music(message)
            else:
                await message.channel.send(f"Hello {message.author.mention},   youre a   狗娘养的吃 penis")

async def main():
    client = MyClient(intents=intents)
    await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())