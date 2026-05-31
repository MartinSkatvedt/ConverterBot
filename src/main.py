import asyncio
import os
import traceback

import discord
from dotenv import load_dotenv

from utils import clean_up_files, convert_webm_to_mp4, get_parent_dir

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

        if not message.attachments:
            return

        for attachment in message.attachments:
            if ".webm" not in attachment.url:
                continue

            loading_message = await self.init_conversion(message)
            parent_dir = get_parent_dir(attachment.filename)
            try:
                # convert_webm_to_mp4 is synchronous and blocking; run it in a
                # worker thread so the transcode doesn't stall the asyncio event
                # loop (which would block Discord heartbeats/reconnects).
                filename, parent_dir = await asyncio.to_thread(
                    convert_webm_to_mp4, attachment.filename, attachment.url
                )
                await self.conversion_complete(loading_message, filename)
            except Exception:
                # Surface the failure instead of leaving a stuck loading message,
                # and keep the bot alive for the next message.
                traceback.print_exc()
                try:
                    await loading_message.edit(
                        content="Failed to convert this file.", attachments=[]
                    )
                except discord.HTTPException:
                    pass
            finally:
                # Always clean up so failed/partial conversions don't accumulate
                # on disk over time.
                clean_up_files(parent_dir)


intents = discord.Intents.default()
intents.message_content = True

client = ConverterBot(intents=intents)
client.run(DISCORD_TOKEN)
