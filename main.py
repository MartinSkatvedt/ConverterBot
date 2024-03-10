import os
import discord
from dotenv import load_dotenv
from moviepy.editor import *
import requests

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


def convert_webm_to_mp4(filename: str, webm_file_url: str) -> str:
    print(f"Converting {filename} to mp4...")

    # download the webm file
    r = requests.get(webm_file_url, allow_redirects=True)

    file_folder_name = filename.split(".")[0]
    os.makedirs(f"./files/{file_folder_name}", exist_ok=True)
    open(f"./files/{file_folder_name}/input.webm", "wb").write(r.content)

    # Replace 'input.webm' with your actual input file path

    input_file = f"./files/{file_folder_name}/input.webm"
    output_file = f"./files/{file_folder_name}/output.mp4"

    # Load the .webm file
    clip = VideoFileClip(input_file)

    # Write the clip to an .mp4 file
    clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # Close the clip
    clip.close()

    return output_file


class MartinBot(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def send_file(self, file_path, message):
        file = discord.File(file_path)
        await message.channel.send(
            file=file,
            content="Je så at du sendte en slik .webm fil, så je konverterte den til en .mp4 fil for deg uwu <3",
        )

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.attachments:
            for attachment in message.attachments:
                if ".webm" in attachment.url:
                    filename = convert_webm_to_mp4(attachment.filename, attachment.url)
                    await self.send_file(filename, message)


intents = discord.Intents.default()
intents.message_content = True
client = MartinBot(intents=intents)
client.run(DISCORD_TOKEN)
