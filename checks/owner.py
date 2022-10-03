import discord
from discord.ext import commands
import asyncio,random
def isowner(ctx):
    return ctx.message.author.id == 653787366548570123
def isowner_slash(ctx):
    return ctx.user.id == 653787366548570123