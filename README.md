# Discord Python Bot

A custom Discord bot with various features implemented using the [discord.py](https://github.com/Rapptz/discord.py) API wrapper for Discord.

## Installation
Create a virtual environment (optional) and activate it:
```bash
python -m venv venv
source venv/bin/activate # Linux/macOS
```

Create a ``keys.py`` file and define a ``TOKEN`` constant to be your Discord bot token:
```bash
echo "TOKEN = <SECRET_TOKEN_HERE>" > keys.py
```

Install requirements:
```bash
pip install -r requirements.txt
```

## Running the Bot
```bash
python bot.py
```