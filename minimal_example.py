import discord
from discord.ext import commands
import dotenv
import os


dotenv.load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot initialising...")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command()
async def ping(ctx):
    await ctx.send("pong!")


bot.run(os.getenv("TOKEN"))
