import discord.utils
from discord.ext import commands

import os
from dotenv import load_dotenv
import music_cogs

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

cogs = [music_cogs]

for i in range(len(cogs)):
    cogs[i].setup(bot)

load_dotenv()
bot_token = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
   print("Bot is online")
   print(f"Successfully logged in as {bot.user}")
   
   await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Being Built"))

@bot.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        await ctx.channel.send("`Invalid Command.\n Use !help to show list of commands`")

def start(bot, token):
	bot.run(token)

start(bot, bot_token)