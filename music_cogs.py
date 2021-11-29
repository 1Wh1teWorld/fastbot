import discord
from discord.ext import commands

import youtube_dl
from youtubesearchpython import VideosSearch

import music_utils

class music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search(self, ctx, search_term : str, limit : int = 4):

        video_search = VideosSearch(search_term, limit=limit)
        await ctx.send(f"Sending {limit} most relevant links")

        for i in range(limit):
            video_id = video_search.result()["result"][i]["id"]
            await ctx.send(f"https://www.youtube.com/watch?v={video_id}")

    @commands.command()
    async def join(self, ctx):

        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel")

        voice_channel = ctx.author.voice.channel

        #Connects to voice channel if not in the context's vc,
        #otherwise joins the context's vc

        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    
    @commands.command(help="""
    Play songs based on a given search.
    It is possible to play from URL too. In this case,
    leave the search_query argument as any random value

    As long as a valid search_url is specified, the bot will ignore
    the search term and play from url
    """)
    async def play(self, ctx, search_query : str, search_url : str = None):

        url = music_utils.generate_most_relevant_url(search_query)
        ctx.voice_client.stop()

        FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"
        }
        YDL_OPTIONS = {"format": "bestaudio"}
        voice_channel = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            if search_url != None:  
                info = ydl.extract_info(search_url, download=False)
            else:
                info = ydl.extract_info(url, download=False)

            url2 = info["formats"][0]["url"]
            # WTF IS THIS with the ** SHIT- below - AIOSDNOIASDOIASJNDOANSDOINDOAINSDSONDOAINSDOIASNDOAISNDOAISNDOIANSD
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            voice_channel.play(source)
    
    @commands.command()
    async def pause(self, ctx):

        await ctx.voice_client.pause()
        await ctx.send("Paused ⏸")
    
    @commands.command()
    async def resume(self, ctx):

        await ctx.voice_client.resume()
        await ctx.send("Resumed ⏯")




def setup(client):
    client.add_cog(music(client))