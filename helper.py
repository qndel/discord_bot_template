import os
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta

def isHost():
    return os.path.exists("./hostPC")
#############################ERRORS AND EVENTS
async def setBotVariable(b):
    global bot
    bot = b

async def handleErrors(ctx,error):
    ignored = (commands.CommandNotFound, commands.UserInputError, commands.CheckFailure)
    error = getattr(error, 'original', error)
    if isinstance(error, ignored):
        return
    print(ctx.author.name)
    print(ctx.message)
    print(ctx.message.content)
    print(error)