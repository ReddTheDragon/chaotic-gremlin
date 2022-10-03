import discord
from discord.ext import commands
import asyncio,random
def isowner():
    async def predicate(ctx):
        if isinstance(ctx,discord.Interaction):
            if ctx.user.id == 653787366548570123:
                return True
            return False
        else:
            if ctx.author.user.id == 653787366548570123:
                return True
            return False