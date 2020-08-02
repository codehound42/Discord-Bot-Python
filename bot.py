import discord
from discord.ext import commands
import keys
from datetime import datetime
import random
from functools import reduce
import requests
import json


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
    string_to_output = reduce(lambda acc, x: acc+x+' ', args, "")
    post_data_to_webhook(keys.GENERAL_CHAT_WEBHOOK, string_to_output)
    

###########################
# Run Client
###########################

if __name__ == "__main__":
    client.run(keys.TOKEN)