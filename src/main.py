import os
import discord
from dotenv import load_dotenv
from utils import clean_up_files, convert_webm_to_mp4

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LOADING_MESSAGE = os.getenv("LOADING_MESSAGE")
COMPLETE_MESSAGE = os.getenv("COMPLETE_MESSAGE")

class ConverterBot(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def conversion_complete(
        self, message: discord.Message, file_path: str
    ) -> None:

        #Load the converted file
        converted_file = discord.File(file_path)

        # Edit the message with the converted file
        await message.edit(
            content=COMPLETE_MESSAGE,
            attachments=[converted_file],
        )

    async def init_conversion(self, message: discord.Message) -> discord.Message:

        # Load the loading gif
        loading_gif = discord.File("./assets/loading.gif")

        # Send the loading message
        sent_message = await message.channel.send(
            content=LOADING_MESSAGE,
            file=loading_gif
        )

        return sent_message

    async def on_message(self, message: discord.Message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.attachments:
            for attachment in message.attachments:
                if ".webm" in attachment.url:
                    loading_message = await self.init_conversion(message)
                    filename, parent_dir = convert_webm_to_mp4(
                        attachment.filename, attachment.url
                    )
                    await self.conversion_complete(
                        loading_message, filename
                    )

                    # clean up the files
                    clean_up_files(parent_dir)


intents = discord.Intents.default()
intents.message_content = True

client = ConverterBot(intents=intents)
client.run(DISCORD_TOKEN)
