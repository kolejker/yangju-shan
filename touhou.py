import discord
import random
import os
import requests

GELBOORU_API_URL = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=hijiri_byakuren"

async def handle_touhou(message):
    await message.channel.send("downloading   touhous")

    try:
        response = requests.get(GELBOORU_API_URL)
        response.raise_for_status()
        data = response.json()

        posts = data.get("post", [])
        if not posts:
            await message.channel.send("fucking fuck")
            return

        random_post = random.choice(posts)
        image_url = random_post.get("file_url")

        if not image_url:
            await message.channel.send("fuck")
            return

        image_data = requests.get(image_url).content
        with open("temp_image.jpg", "wb") as f:
            f.write(image_data)

        await message.channel.send(
            "here woman",
            file=discord.File("temp_image.jpg")
        )

        os.remove("temp_image.jpg")

    except Exception as e:
        await message.channel.send(f"my mother once said: {str(e)}")
