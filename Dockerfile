FROM python:3.9

# Create app directory
WORKDIR /app

# Install app dependencies
COPY src/requirements.txt ./
COPY assets ./assets

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

EXPOSE 8080
CMD [ "python", "main.py" ]