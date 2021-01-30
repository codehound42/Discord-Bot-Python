# Discord Python Bot

A custom Discord bot with various features implemented using the [discord.py](https://github.com/Rapptz/discord.py) API wrapper for Discord. You are welcome to use the source code of this project, but I would appreciate it if you give some attribution by linking to my GitHub page or YouTube channel :-)

## Installation
Create a virtual environment (optional) and activate it:
```bash
python -m venv venv
source venv/bin/activate # Linux/macOS
```

Install requirements:
```bash
pip install -r requirements.txt
```

Create an ``.env`` file and define a ``TOKEN`` constant to be your Discord bot token. Throughout the project a number of extra keys and folders have also been added. Refer to my [tutorial videos on YouTube](https://www.youtube.com/playlist?list=PLoNbvI5hV5uO4YoSZp3dlJ0fz_8ssn1FX) or study the code for what to add to your environment in order to use the various commands. Refer to the .env.example file for the keys to fill out.

## Running the Bot
```bash
python bot.py
```