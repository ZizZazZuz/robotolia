import os
import discord
from discord.ext import commands
import logging
import traceback
import wikipedia

# Arguments that need to passed to the build function 
DEVELOPER_KEY = os.environ.get('YOUTUBE_DEV_KEY')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
   
# creating Youtube Resource Object 
#youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY) 

class Extern(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

    @commands.command(help='Search YouTube for a video or playlist.', usage='!yt <search terms>', aliases=['youtube','memevid'])
    async def yt(ctx, *, arg):
        print('Call made for % s' % arg)
        # make the request. Only allow 1 return for now because that's a pain
        search_keyword = youtube_object.search().list(q = arg, part = "id, snippet", maxResults = 1, type = "video, playlist").execute()
        results = search_keyword.get("items",[])
        if len(results) == 0:
            print('No results returned')
            await ctx.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            return
        # print(results)
        result = results[0]
        if result['id']['kind'] == "youtube#video":
            print('Top result was video')
            await ctx.send("http://www.youtube.com/watch?v=% s" % result["id"]["videoId"])
            return
        elif result['id']['kind'] == "youtube#playlist":
            print('Top result was playlist')
            await ctx.send("https://www.youtube.com/playlist?list=% s" % result["id"]["playlistId"])
            return
        print('Something wrong, i hold my head')
        await ctx.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    @client.command(help='Accepts a string, searches wikipedia for it, then posts the summary.')
    async def wiki(ctx, *, arg):
        search_results = wikipedia.search(arg,results=1)
        page = wikipedia.page(title=search_results[0])

        summary = page.summary
        if len(summary) > 1000:
            summary = summary[:1000] + "..."

        sendmsg = "**__" + page.title + "__**\n" + summary + "\n\n<" + page.url + ">"
        await ctx.send(sendmsg)

def setup(bot):
    bot.add_cog(Extern(bot))