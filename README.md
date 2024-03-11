# ConverterBot

Due to _.webm_ files not being rendered on discord mobile, I created this bot for me and my friends so that files would automatically be converted to _.mp4_ files.

The bot looks for any message with a _.webm_ file and uses moviepy to convert it to a _.mp4_ file. 


## Usage

If you want to use this bot, you will need to create a bot on the discord developer portal and add it to your server.

I included a `Dockerfile` so that you can easily run the bot in a container. Just remember to add you __DISCORD_TOKEN__ to the environment variables.

You would probably also change the response messages from the bot to fit your needs.
