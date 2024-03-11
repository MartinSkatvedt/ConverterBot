import os
import discord
from dotenv import load_dotenv
from utils import clean_up_files, convert_webm_to_mp4

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class ConverterBot(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def edit_loading_message_and_send_file(
        self, message: discord.Message, file_path: str
    ) -> None:
        converted_file = discord.File(file_path)

        await message.edit(
            content="Sånn, nå har je konvertert filen for deg sussebassen min <3",
            attachments=[converted_file],
        )

    async def send_loading_message(self, message: discord.Message) -> discord.Message:

        loading_gif = discord.File("./assets/loading.gif")

        sent_message = await message.channel.send(
            "Je så at du lasta opp en slik .webm fil, så je driver konverterer den til en .mp4 fil for deg uwu <3",
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
                    loading_message = await self.send_loading_message(message)
                    filename, parent_dir = convert_webm_to_mp4(
                        attachment.filename, attachment.url
                    )
                    await self.edit_loading_message_and_send_file(
                        loading_message, filename
                    )

                    # clean up the files
                    clean_up_files(parent_dir)


intents = discord.Intents.default()
intents.message_content = True

client = ConverterBot(intents=intents)
client.run(DISCORD_TOKEN)
