import discord
from discord.ext import commands
import asyncio,random
def isowner(ctx):
    async def predicate(ctx):
        if isinstance(ctx,discord.Interaction):
            if ctx.user.id == 653787366548570123:
                return True
            return False
        else:
            if ctx.author.user.id == 653787366548570123:
                return True
            return False
    return commands.check(predicate)

def isowner_slash(ctx):
    async def predicate(ctx):
        if isinstance(ctx,discord.Interaction):
            if ctx.user.id == 653787366548570123:
                return True
            return False
        else:
            if ctx.author.user.id == 653787366548570123:
                return True
            return False
    return discord.app_commands.check(predicate)