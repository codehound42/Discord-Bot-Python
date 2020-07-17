import discord
from discord.ext import commands
import keys

client = discord.Client()
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f"Bot {client.user.name} initialising...")


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send("pong!")


@client.command()
async def terminate(ctx):
    await ctx.send("Terminating...")
    await client.logout()


client.run(keys.TOKEN)