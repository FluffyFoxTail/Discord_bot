# Discord bot on Python 

## Motivations

This bot was created for my own needs, 
and for the purpose of practicing programming in Python

## Features:

* Add music to queue
* Joins in voice channel and playing music
* Support Pause/Resume and Skip functions
* Some system commands like clear off text chat, kick or ban/unban chanel member

  ### Comands:
    * **[prefix]** play
    * **[prefix]** add [your request]
    * **[prefix]** pause
    * **[prefix]** resume
    * **[prefix]** skip
    * **[prefix]** clear [number of messages to delete]
    * **[prefix]** kick [username#discriminator]
    * **[prefix]** ban [username#discriminator]
    * **[prefix]** unban [username#discriminator]

## Dependencies:

All dependencies in **requirements.txt**  
Use: 
```console
python -m pip install -r requirements.txt
```
Also you need have installed **ffmpeg** 
```console
apt-get install -y ffmpeg
```
And set environment variable - your discord bot token
```console
export TOKEN=your_token
```

## Usage
Run bot.py
```console
python bot.py
```
Or run using docker
```console
docker build -t [your tag_name for image] .

docker run -e TOKEN=your_token
```
