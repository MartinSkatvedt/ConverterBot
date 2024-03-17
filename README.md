# ConverterBot

Due to _.webm_ files not being rendered on discord mobile, I created this bot for me and my friends so that files would automatically be converted to _.mp4_ files.

The bot looks for any message with a _.webm_ file and uses moviepy to convert it to a _.mp4_ file. 


## Usage

If you want to use this bot, you will need to create a bot on the discord developer portal and add it to your server.

I included a `Dockerfile` so that you can easily run the bot in a container. Or you can use the prebuilt image. There is also a `docker-compose.yml` file that you can use to run the bot with docker-compose, it also uses watchtower to automatically update the bot when a new image is available.

Remember to create a `.env` file if you are using docker-compose (see `.env.example` for reference).


### Docker compose example

1. First update the `.env` file with your bot token, and the different response messages. 
2. You can then run the bot with the following command:
```bash	
docker-compose up -d
```



