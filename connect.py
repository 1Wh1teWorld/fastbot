import discord
from discord import message
import os
from discord.ext.commands.core import command
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

load_dotenv()
bot_token = os.getenv("DISCORD_TOKEN")

@bot.command()
async def print(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response)

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def makepoll(ctx, poll_type, poll_title, *options):
	
	user_nick = ctx.message.author.nick
	poll = discord.Embed(title=poll_title, description=f"Poll created by {user_nick}")

	if poll_type == "multi-choice":

		reactions = ["1️⃣", "1️⃣"]

		for num, option in enumerate(options):
			poll.add_field(name=f"Option {num+1}" , value=option, inline=False)
		
		emoji = get(ctx.guild.emojis, name=":one:")
		await ctx.channel.send(emoji)
		
		
		msg = await ctx.channel.send(embed=poll)

	elif poll_type == "tf":

		if len(options) != 1:
			await ctx.channel.send("True or False polls may only have 1 question.")
		else:
			reactions = ["✅", "❌"]

			poll.add_field(name=f"True or False?", value=options, inline=False)
			await ctx.message.add_reaction(reactions[0])
			await ctx.message.add_reaction(reactions[1])

			await ctx.channel.send(embed=poll)


@bot.event
async def on_ready():
   print("Bot is online")

def start():
	bot.run(bot_token)


def main():
	start()

main()