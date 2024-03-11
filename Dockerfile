FROM python:3.9

ARG DISCORD_TOKEN_ARG
ENV DISCORD_TOKEN $DISCORD_TOKEN_ARG

# Create app directory
WORKDIR /app

# Install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

EXPOSE 8080
CMD [ "python", "main.py" ]