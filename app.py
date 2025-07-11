import discord
import random
import asyncio
import json
import aiohttp
from jumpstyle import handle_jumpstyle
from music import handle_music
from neofetch import handle_neofetch
from touhou import handle_touhou

TOKEN = 'no'
CHANNEL_ID = no
MISTRAL_API_KEY = 'no'

SYSTEM_PROMPT = """"""

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent_id = None
        
    async def setup_hook(self):
        self.random_msg_task = self.loop.create_task(self.send_random_message())
        await self.create_agent()

    async def create_agent(self):
        url = "https://api.mistral.ai/v1/agents"
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-large-latest",
            "name": "阳具山",
            "description": "阳具山",
            "instructions": SYSTEM_PROMPT,
            "completion_args": {
                "temperature": 1,
                "max_tokens": 150
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.agent_id = result['id']
                        print(f"Agent created with ID: {self.agent_id}")
                    else:
                        print(f"Failed to create agent: {response.status}")
        except Exception as e:
            print(f"Error creating agent: {e}")

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

    async def get_mistral_response(self, user_message):
        if not self.agent_id:
            return "Agent not initialized properly"
            
        url = "https://api.mistral.ai/v1/conversations"
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "agent_id": self.agent_id,
            "inputs": user_message,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['outputs'][0]['content']
                    else:
                        return "my mother once said: no"
        except Exception as e:
            print(f"my mother once said: {e}")
            return "my mother once said: error"

    async def on_message(self, message):
        if message.author.bot:
            return
            
        if self.user in message.mentions:
            if "jumpstyle" in message.content.lower():
                await handle_jumpstyle(message)
            elif "neofetch" in message.content.lower():
                await handle_neofetch(message)
            elif "touhou" in message.content.lower():
                await handle_touhou(message)
            elif "play " in message.content.lower():
                await handle_music(message)
            else:
                user_message = message.content.replace(f'<@{self.user.id}>', '').strip()
                ai_response = await self.get_mistral_response(user_message)
                await message.channel.send(f"{message.author.mention}, {ai_response}")

async def main():
    client = MyClient(intents=intents)
    await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())