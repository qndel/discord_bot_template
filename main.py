#!/usr/bin/env python3
import sys
import helper
import discord
import asyncio
import traceback
import importlib
from discord.ext import commands
from discord.ext.commands import has_permissions
init = 1
######CONFIG##################
admins = ["Qndel#2237"]
allowed_channels = ["bot-commands"]
######END_CONFIG##############


bot = commands.Bot(command_prefix='!')   
######################################################################################################USER_COMMANDS####
#EXAMPLE
#async def commandHelp(ctx) in helper.py - handle the command there - it will allow you to edit existing commands and reload them dynamically without restarting the bot with !reload command
#@bot.command(name='test')
#async def commandHelp(ctx):
#    helper.commandHelp(ctx)
######################################################################################################END_USER_COMMANDS
async def updateStatus():
    activity = discord.Activity(name='Servers: '+str(len(bot.guilds)), type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    
@bot.check
async def filter_channels(ctx):
    return ctx.guild is None or ctx.channel.name in allowed_channels
  
@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound, commands.UserInputError, commands.CheckFailure)
    error = getattr(error, 'original', error)
    if isinstance(error, ignored):
        return
    print(ctx.author.name)
    print(ctx.message)
    print(ctx.message.content)
    print(error)
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
bot.remove_command("help")
@bot.command(name='help', hidden=True)
async def commandHelp(ctx):
    cmdList = []
    for y in bot.walk_commands():
        if not y.cog_name and not y.hidden:
            cmdList.append(y.name)
    await ctx.send('**Commands:**\n> '+bot.command_prefix+("\n> "+bot.command_prefix).join(cmdList)+'\nWrite command without arguments to see more info.')  
                 
@bot.command(name='reload', hidden=True)
async def commandReload(ctx, *, arg=None):
    if str(ctx.message.author) not in admins:
        await ctx.send("You don't have the permission to do this.")
        return
    importlib.reload(helper)
    if not (ctx.guild is None):
        await ctx.message.delete()
        await ctx.send("Data reloaded.", delete_after=10.0)
    else:
        await ctx.send("Data reloaded.")

@bot.command(name='announce', hidden=True)     
async def commandAnnounce(ctx,arg):
    if str(ctx.author) not in admins:
        await ctx.send("You don't have the permission to do this.")
        return
    for x in bot.guilds:
        if len(x.text_channels) > 0:
            for y in x.text_channels:
                if y.name in allowed_channels:
                    try:
                        await y.send(arg)
                    except Exception as err:
                        await ctx.send("Error! Check the log!")
                        return
    await ctx.send("Announced successfully.")

@bot.command(name='howtoadd')
async def commandHowToAdd(ctx):
    await ctx.send('To add the bot to a discord server, the server admin must visit\n<'+discord.utils.oauth_url(bot.user.id)+'>\nand choose the server.') 

@bot.command(name='info')
async def commandInfo(ctx):
    await ctx.send('Created by **Qndel#2237**\n**discord.py**: v'+discord.__version__) 
    
@bot.event
async def on_guild_join(guild):
    await updateStatus()
    
@bot.event
async def on_guild_remove(guild):
    await updateStatus()
    
@bot.event
async def on_ready():
    global init
    print('We have logged in as {0.user}'.format(bot))
    if init == 1:
        #prevent firing this multiple times as on_ready can trigger whenever discord lags or something - would cause unexpected behavior if this place was used to run a script in the background
        await helper.setBotVariable(bot)
        init = 0
    await updateStatus()

with open(("token_remote","token_host")[helper.isHost()], 'r') as file:
    bot.run(file.read())