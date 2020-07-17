import discord
from discord.ext import commands
import keys

client = discord.Client()
client = commands.Bot(command_prefix='!')
is_client_running = False


@client.event
async def on_ready():
    global is_client_running

    if not is_client_running:
        is_client_running = True
        await init()


async def init():
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
    
    # Process command
    if not message.content.startswith('!'):
        return
    await message.channel.trigger_typing()
    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send("pong!")


@client.command(aliases=['youHaveBeenTerminated'])
async def terminate(ctx):
    await ctx.send("Terminating...")
    await client.logout()


client.run(keys.TOKEN)