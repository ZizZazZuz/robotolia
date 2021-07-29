#import discord
#from discord.ext import commands
#from apiclient.discovery import build 
#import requests
#import shutil
#import os
#import subprocess
#import logging #Maybe this will fix my problems.
#import asyncio # Allows calling async w/o await
#import wikipedia
##from PIL import Image

#logging.basicConfig(level=logging.INFO)
   
## Arguments that need to passed to the build function 
#DEVELOPER_KEY = os.environ.get('YOUTUBE_DEV_KEY')
#YOUTUBE_API_SERVICE_NAME = "youtube"
#YOUTUBE_API_VERSION = "v3"
   
## creating Youtube Resource Object 
#youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
#                                        developerKey = DEVELOPER_KEY) 
#client = commands.Bot(command_prefix = '!')

## creating magik queue
#magikqueue = [] #here we will store information about file name and type for commands.
#magikrunning = False #this will tell us if the queue is being iterated through or not.

##identifies the file type of the given file. Returns a string.
#async def check_filetype(filename):
#	p = p = subprocess.run(['identify',filename], capture_output=True, text=True) #get file info
#	out = p.stdout
#	seg_out = out.split() #split into individual parts
#	return seg_out[1] #second element is file type ["JPEG","PNG","GIF"]

## performs the actual act of magiking images.
#async def magik_processor():
#	global magikrunning
#	global magikqueue
#	# This queue item should be a list of [file_name, ctx]
#	queue_item = magikqueue.pop(0)
	
#	# send a notification to the channel that requested this magik that the image is being processed
#	# await queue_item[1].send('Magiking image ' + queue_item[0])
	
#	# magiking code from below
#	p = subprocess.run(['convert',queue_item[0],'-coalesce','-liquid-rescale','50x50%',"output_"+queue_item[0]])
#	if p.returncode != 0:
#		#Something other than 0 is a nonstandard error code, just crash here. Or whatever.
#		await queue_item[1].send('Something went wrong magiking your image.')
#		os.remove(queue_item[0])
		
#		# same as block at end of function, but handled early.
#		if len(magikqueue) >= 1:
#			# await queue_item[1].send('Queue length is ' + len(magikqueue))
#			await magik_processor()
#			return
#		else:
#			magikrunning = False
#			return
	
#	p = subprocess.run(['identify','-format','%h %w ',"output_"+queue_item[0]], capture_output=True, text=True)
#	outstring = p.stdout
#	print('Outstring: %s', outstring)
#	hw = outstring.strip('"').split()
#	print('Arg 0: %s', hw[0])
#	print('Arg 1: %s', hw[1])
#	if int(hw[0]) < 400 or int(hw[1]) < 300:
#		p = subprocess.run(['convert',"output_"+queue_item[0],'-resize','200%',"output_"+queue_item[0]])
#		if p.returncode != 0:
#			#Something other than 0 is a nonstandard error code, don't crash because the og file might still be there.
#			await queue_item[1].send('Something went wrong upscaling your image.')
	
#	await queue_item[1].send(file=discord.File('output_'+queue_item[0], 'output_'+queue_item[0])) #send as described
	
#	#delete both images so we don't store them
#	os.remove(queue_item[0])
#	os.remove("output_"+queue_item[0])
	
#	# what do we do next?
#	if len(magikqueue) >= 1:
#		# continue iterating through the queue
#		# await queue_item[1].send('Queue length is ' + str(len(magikqueue)))
#		await magik_processor()
#	else:
#		# don't call recursively and set the variable to false so that enqueue_magik() can know to restart us
#		magikrunning = False
#	return
	
#async def enqueue_magik(file_url, file_name, ctx):
#	# download file from request
#	resp = requests.get(file_url, stream = True) # get the file url we found
#	local_file = open(file_name, "wb")
	
#	resp.raw.decode_content = True
#	shutil.copyfileobj(resp.raw, local_file)
	
#	del resp
#	local_file.close()
	
#	# identify the file type
#	ext = ""
#	filetype = await check_filetype(file_name)
#	if filetype == "JPEG":
#		ext = ".jpg"
#	elif filetype == "PNG":
#		ext = ".png"
#	elif filetype == "GIF":
#		ext = ".gif"
#    # ext = p.subprocess.run(['identify','-format','%[e]'])
#	else:
#		# remove file if it's not an approved type
#		os.remove(file_name)
#		await ctx.send(file_name + ' has encountered an error: Unknown filetype. (' + filetype +')')
#		return
	
#	# rename the file to include the extension
#	os.rename(file_name, file_name + ext)
#	file_name = file_name + ext
#	return file_name

#async def embed_image_parser(embed, file_name_stub, ctx, index):
#	# queue each embed in order. Name them by their message ID and the index in embeds.
#	if embed.image != discord.Embed.Empty:
#		# Naming convention: RequestMessageID_EmbedIndex_image
#		return await enqueue_magik(embed.image.url, file_name_stub+"_image", ctx)
#	elif embed.thumbnail != discord.Embed.Empty:
#		# Naming convention: RequestMessageID_EmbedIndex_thumb
#		return await enqueue_magik(embed.thumbnail.url, file_name_stub+"_thumb", ctx)
#	return
	
#@client.event
#async def on_ready():
#        print('Hello World!')

#@client.command(help='Search YouTube for a video or playlist.', usage='!yt <search terms>', aliases=['youtube','memevid'])
#async def yt(ctx, *, arg):
#        print('Call made for % s' % arg)
#        # make the request. Only allow 1 return for now because that's a pain
#        search_keyword = youtube_object.search().list(q = arg, part = "id, snippet", maxResults = 1, type = "video, playlist").execute()
#        results = search_keyword.get("items",[])
#        if len(results) == 0:
#            print('No results returned')
#            await ctx.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
#            return
#        # print(results)
#        result = results[0]
#        if result['id']['kind'] == "youtube#video":
#            print('Top result was video')
#            await ctx.send("http://www.youtube.com/watch?v=% s" % result["id"]["videoId"])
#            return
#        elif result['id']['kind'] == "youtube#playlist":
#            print('Top result was playlist')
#            await ctx.send("https://www.youtube.com/playlist?list=% s" % result["id"]["playlistId"])
#            return
#        print('Something wrong, i hold my head')
#        await ctx.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
		


#@client.command(help='Accepts 0 or 1 arguments. Argument should be URL of image.')
#async def magik(ctx, *args):
#	print('Running magik')
#	await ctx.send('Please be patient, I have a small brain.')
	
#	# loop = asyncio.get_event_loop()
	
#	tasks = [] #store tasks here
	
#	# scale_factor = 0.8
#	if len(args) != 0:
#		# Assume we have a url. This is bad practice but I don't care. This will only ever take one image at a time
#		# Naming convention: RequestMessageID
#		tasks.append(asyncio.create_task(enqueue_magik(args[0], str(ctx.message.id), ctx)))
#	else:
#		if len(ctx.message.attachments) != 0:
#			for index in range(len(ctx.message.attachments)):
#				# queue each file in order. Name them by their message ID and the index in attachments.
#				# Naming convention: RequestMessageID_AttachmentIndex
#				tasks.append(asyncio.create_task(enqueue_magik(ctx.message.attachments[index].url, str(ctx.message.id)+"_"+str(index), ctx)))
#		elif len(ctx.message.embeds) != 0:
#			for embed in range(len(ctx.message.embeds)):
#				# queue each embed in order. Name them by their message ID and the index in embeds.
#				if ctx.message.embeds[embed].image != discord.Embed.Empty:
#					# Naming convention: RequestMessageID_EmbedIndex_image
#					tasks.append(asyncio.create_task(enqueue_magik(ctx.message.embeds[embed].image.url, str(ctx.message.id)+"_"+str(embed)+"_image", ctx)))
#				elif ctx.message.embeds[embed].thumbnail != discord.Embed.Empty:
#					# Naming convention: RequestMessageID_EmbedIndex_thumb
#					tasks.append(asyncio.create_task(enqueue_magik(ctx.message.embeds[embed].thumbnail.url, str(ctx.message.id)+"_"+str(embed)+"_thumb", ctx)))
#		else:
#			print('no args, no attachments, no embeds')
			
#			# if the message we got didn't have any embeds, attachments, or urls, we assume we need to search up.
#			async for message in ctx.channel.history(limit=200):
			
#				# sometimes we get situations where the bot's search is delayed. We don't want our user's output to change based on that,
#				# so if we get messages from after the original message we ignore them.
#				if ctx.message.created_at < message.created_at:
#					continue

#				#we check messages for content with the same priority as before: attachments first, embeds second.
#				if len(message.attachments) != 0:
#					for index in range(len(message.attachments)):
#						# Naming convention: RequestMessageID_BacklogMessageID_AttachmentIndex
#						tasks.append(asyncio.create_task(enqueue_magik(message.attachments[index].url, str(ctx.message.id)+"_"+str(message.id)+"_"+str(index), ctx)))
#					break
#				elif len(message.embeds) != 0:
#					for embed in range(len(message.embeds)):
#						if message.embeds[embed].image != discord.Embed.Empty:
#							# Naming convention: RequestMessageID_BacklogMessageID_EmbedIndex_image
#							tasks.append(asyncio.create_task(enqueue_magik(message.embeds[embed].image.url, str(ctx.message.id)+"_"+str(message.id)+"_"+str(embed)+"_image", ctx)))
#					break
	
	
#	# Add to queue
#	# TODO: add support for mp4 file formats (needs additional information)
	
#	await asyncio.gather(*(tasks[index] for index in range(len(tasks)))) # run all the collected tasks
	
#	print('number of tasks queued: ' + str(len(tasks)))
#	global magikqueue
#	for index in range(len(tasks)): 
#		# see https://docs.python.org/3/library/asyncio-task.html
#		magikqueue.append([tasks[index].result(), ctx])
	
#	# move this down here so we don't run magik_processor() too many times
#	global magikrunning
#	if magikrunning == False:
#		magikrunning = True
#		await magik_processor()
#	#loop.close()
#	return

#	# If all else fails, just get the user's avatar
#	# file_url = "https://images.discordapp.net/avatars/% s/% s.jpg" % (ctx.message.author.id,ctx.message.author.avatar) # "https://images.discordapp.net/avatars/% s/% s.jpg?size=1024"
#	# await enqueue_magik(ctx.message.author.avatar_url, str(ctx.message.id)+str(ctx.author.id), ctx)
#	# return
	
#@client.command(help='Posts a file. This is a test command.')
#async def post_file_by_filename(ctx, *, arg):
#	await ctx.send(file=discord.File(arg, arg))
	
#@client.command(help='My power grows')
#async def empty_roles(ctx):
#	server = ctx.message.guild
#	empty_role_list = []
	
#	for index in range(len(server.roles)):
#		if not server.roles[index]:
#			empty_role_list.append(server.roles[index])
	
#	if not empty_role_list:
#		await ctx.send('No empty roles! Somehow.')
#		return
	
#	message = 'List of empty roles:\n'
#	for role in empty_role_list:
#		message = message + role.name + '\n'
	
#	await ctx.send(message)
	
	

#@client.command(help='Accepts a string, searches wikipedia for it, then posts the summary.')
#async def wiki(ctx, *, arg):
#	search_results = wikipedia.search(arg,results=1)
#	page = wikipedia.page(title=search_results[0])
	
#	summary = page.summary
#	if len(summary) > 1000:
#		summary = summary[:1000] + "..."
	
#	sendmsg = "**__" + page.title + "__**\n" + summary + "\n\n<" + page.url + ">"
	
#	await ctx.send(sendmsg)
#client.run(os.environ.get('DISCORD_BOT_TOKEN'))



import discord
from discord.ext import commands
#from apiclient.discovery import build 
#import requests
#import shutil
import os
import sys
#import subprocess
import logging #Maybe this will fix my problems.
import traceback
#import asyncio # Allows calling async w/o await
#import wikipedia
#from PIL import Image

logging.basicConfig(level=logging.INFO)
description = '''A bot designed to handle a specific set of needs. Those being whatever I want.'''

initial_extensions = (
	'cogs.extern',
)

def _prefix_callable(bot, msg):
	user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ', '!']
	return base

#bot = commands.Bot(command_prefix = '!', description=description, intents=intents)

class Robotolia(commands.Bot):
	def __init__(self):
		# Thanks R.Danny
		allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
		intents = discord.Intents(
			guilds=True,
			members=True,
			bans=True,
			emojis=True,
			voice_states=True,
			messages=True,
			reactions=True,
		)
		super().__init__(command_prefix=_prefix_callable, description=description,
                         pm_help=None, help_attrs=dict(hidden=True),
                         fetch_offline_members=False, heartbeat_timeout=150.0,
                         allowed_mentions=allowed_mentions, intents=intents)

		for extension in initial_extensions:
			try:
				self.load_extension(extension)
			except Exception as e:
				printf(f'Failed to load extension {extension}.', file=sys.stderr)
				traceback.print_exc()

	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.NoPrivateMessage):
			await ctx.author.send('This command cannot be used in private messages.')
		elif isinstance(error, commands.DisabledCommand):
			await ctx.author.send('This command is disabled and cannot be used.')
		elif isinstance(error, commands.CommandInvokeError):
			original = error.original
			if not isinstance(original, discord.HTTPException):
				print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
				traceback.print_tb(original.__traceback__)
				print(f'{original__class__.__lame__}: {original}', file=sys.stderr)
		elif isinstance(error, commands.ArgumentParsingError):
			await ctx.author.send(error)

	async def close(self):
		await super().close()
		#await self.session.close()

	def run(self):
		try:
			super().run(s.environ.get('DISCORD_BOT_TOKEN'), reconnect=True)

bot = Robotolia()
@bot.event
async def on_ready():
	print(f'Logged in as {bot.user} (ID: {bot.user.id})')
	print('-------')

bot.run()


# Arguments that need to passed to the build function 
#DEVELOPER_KEY = os.environ.get('YOUTUBE_DEV_KEY')
#YOUTUBE_API_SERVICE_NAME = "youtube"
#YOUTUBE_API_VERSION = "v3"
   
# creating Youtube Resource Object 
#youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY) 
