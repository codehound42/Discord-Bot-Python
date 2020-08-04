import discord
from discord.ext import commands
import keys
from datetime import datetime
import random
from functools import reduce
import requests
import json
import googletrans


###########################
# Globals
###########################

client = discord.Client()
client = commands.Bot(command_prefix='!')
is_client_running = False


###########################
# Events
###########################

@client.event
async def on_ready():
    global is_client_running

    if not is_client_running:
        is_client_running = True
        print(f"Bot {client.user.name} initialising...")


@client.event
async def on_message(message):
    # Avoid the bot replying to itself
    if message.author == client.user:
        return

    # Reply hello to hello messages
    if message.content.lower().startswith('hello'):
        await message.channel.send(f"Hello {message.author.mention}")
        return
    
    if not message.content.startswith('!'):
        return
        
    # Process command
    await message.channel.trigger_typing()
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    # Only show the raw error output to the discord user if it is not an internal exception
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("An error occured while processing the command, but don't worry, a team of highly trained dolphins have been dispatched and are currently looking into it.")
    else:
        await ctx.send(error)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "command exception", type(error), error)


###########################
# Utilities
###########################

def check_if_lucky(chance=0.5):
    def predicate(ctx):
        return random.random() < chance
    return commands.check(predicate)


def post_data_to_webhook(url, message):
    requests.post(url, data=json.dumps({'content': message}), headers={'Content-type': 'application/json'})


###########################
# Commands
###########################

@client.command()
@commands.dm_only()
async def ping(ctx):
    await ctx.send("pong!")


@client.command()
@commands.guild_only()
async def ding(ctx):
    await ctx.send("dong!")


@client.command()
@commands.has_permissions(manage_webhooks=True)
async def iBeDev(ctx):
    await ctx.send("you be dev")


@client.command()
@commands.has_any_role("admin", "moderator")
async def randomRange(ctx, a, b):
    result = random.randrange(int(a), int(b))
    await ctx.send(f"Random int in range [{a}; {b}[: **{result}**")


@client.command()
@check_if_lucky()
async def tryMyLuck(ctx):
    await ctx.send("You're lucky pal!!!")


@client.command(aliases=['youHaveBeenTerminated'])
@commands.is_owner()
async def terminate(ctx):
    await ctx.send("Terminating...")
    await client.logout()


@client.command()
@commands.dm_only()
@commands.is_owner()
async def echo(ctx, *args):
    post_data_to_webhook(keys.GENERAL_CHAT_WEBHOOK, ' '.join(args))


@client.command(aliases=['tr'])
async def translate(ctx, lang_to, *args):
    """Translates the given text to the language `lang_to`.
    The language translated from is automatically detected."""

    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate text to")

    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text
    await ctx.send(text_translated)


@client.command()
async def oracle(ctx, *args):
    query = '+'.join(args)
    url = f"https://api.wolframalpha.com/v1/result?i={query}%3F&appid={keys.WOLFRAM_ALPHA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 501:
        await ctx.send("Unable to process that query")
        return

    await ctx.send(response.text)


###########################
# Run Client
###########################

if __name__ == "__main__":
    client.run(keys.TOKEN)