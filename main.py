#!/usr/bin/env python3
import helper
import discord
import asyncio
import importlib
from discord.ext import commands
from discord.ext.commands import has_permissions

bot = commands.Bot(command_prefix='!')
token_host = "" #testing bot token
token_remote = "" #bot token
admins = ["Qndel#2237"]
allowed_channels = [""]
open('token_host', 'r') as file:
    token_host = file.read()
open('token_remote', 'r') as file:
    token_remote = file.read()
    
@bot.check
async def filter_channels(ctx):
    return ctx.guild is None or ctx.channel.name in allowed_channels
    
#@bot.event
#async def on_command_error(ctx, error):
#    await helper.handleErrors(ctx,error)
    
bot.remove_command("help")
@bot.command(name='help', hidden=True)
async def commandHelp(ctx):
    cmdList = []
    for y in bot.walk_commands():
        if not y.cog_name and not y.hidden:
            cmdList.append(y.name)
    await ctx.send('**Commands:**\n> '+("\n> "+bot.command_prefix).join(cmdList)+'\nWrite command without arguments to see more info.')  
                
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
    
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await helper.setBotVariable(bot)
    activity = discord.Activity(name='!help for commands', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    
if helper.isHost():
    bot.run(token_host)
else:
    bot.run(token_remote) 