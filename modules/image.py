# #Copyright 2022 Thomas D. Streiff
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import discord
from discord.ext import commands
import asyncio,random
import aiohttp
from io import BytesIO
import pgmagick,async_timeout

aiohttp.Timeout = async_timeout.timeout
class imageDefs:
    def apiget(self,url,endpoint):
        try:
            import requests
            r = requests.get(url)
            return r.json()[endpoint]
        except:
            return False
            traceback.print_exc()
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name="implode")
    @commands.cooldown(rate=2,per=120,type=commands.BucketType.guild)
    async def doimplosion(self,ctx):
        """IMPLODE"""
        doexit = False
        async with ctx.channel.typing():
            messages = await ctx.channel.history().flatten()
            myLastMessage = discord.utils.find(lambda m: m.attachments != None and m.guild == ctx.guild and m.attachments != [], messages)
            if myLastMessage is None:
                await ctx.send("**Error. Could not find an image!**")
                return False
            #check if image
            myfiname = myLastMessage.attachments[0].filename.split(".")
            acceptableFiles = ["png","jpg","jpeg"]
            try:
                if not myfiname[len(myfiname) - 1] in acceptableFiles:
                    await ctx.send("**Error! Not a valid image.**")
            except:
                await ctx.send("**Error! Not a valid image.**")
                doexit = True
            try:
                url = myLastMessage.attachments[0].url
            except:
                import traceback
                traceback.print_exc()
                del traceback
            try:
                imageBinary = ""
                async with aiohttp.ClientSession() as session:
                    with aiohttp.Timeout(5):
                        async with session.get(url) as resp:
                            data = await resp.read()
                            b = BytesIO(data)
                            b.seek(0)
                            imageBinary = b.read()
                    
            except:
                await ctx.send("**Error. Could not fetch latest image!**")
                doexit = True
            blob = pgmagick.Blob(imageBinary)
            myimg = pgmagick.Image(blob)
            myimg.implode(.3)
            myfi = pgmagick.Blob()
            myimg.write(myfi)
            print(myfi.data)
            myDiscordFile = discord.File(myfi.data,filename='result.png')
        if doexit is True:
            return False
        await ctx.send(file=myDiscordFile)    
    @commands.command(name="explode")
    @commands.cooldown(rate=2,per=120,type=commands.BucketType.guild)
    async def doexplosion(self,ctx):
        """BOOM"""
        doexit = False
        async with ctx.channel.typing():
            messages = await ctx.channel.history().flatten()
            myLastMessage = discord.utils.find(lambda m: m.attachments != None and m.guild == ctx.guild and m.attachments != [], messages)
            if myLastMessage is None:
                await ctx.send("**Error. Could not find an image!**")
                return False
            #check if image
            myfiname = myLastMessage.attachments[0].filename.split(".")
            acceptableFiles = ["png","jpg","jpeg"]
            try:
                if not myfiname[len(myfiname) - 1] in acceptableFiles:
                    await ctx.send("**Error! Not a valid image.**")
            except:
                await ctx.send("**Error! Not a valid image.**")
                doexit = True
            try:
                url = myLastMessage.attachments[0].url
            except:
                import traceback
                traceback.print_exc()
                del traceback
            try:
                imageBinary = ""
                async with aiohttp.ClientSession() as session:
                    with aiohttp.Timeout(5):
                        async with session.get(url) as resp:
                            data = await resp.read()
                            b = BytesIO(data)
                            b.seek(0)
                            imageBinary = b.read()
                    
            except:
                await ctx.send("**Error. Could not fetch latest image!**")
                doexit = True
            blob = pgmagick.Blob(imageBinary)
            myimg = pgmagick.Image(blob)
            myimg.implode(-2)
            myfi = pgmagick.Blob()
            myimg.write(myfi)
            print(myfi.data)
            myDiscordFile = discord.File(myfi.data,filename='result.png')
        if doexit is True:
            return False
        await ctx.send(file=myDiscordFile)
        
    @commands.command(name="swirl")
    @commands.cooldown(rate=2,per=120,type=commands.BucketType.guild)
    async def doswirl(self,ctx):
        """do a curl, do a swirl"""
        doexit = False
        async with ctx.channel.typing():
            messages = await ctx.channel.history().flatten()
            myLastMessage = discord.utils.find(lambda m: m.attachments != None and m.guild == ctx.guild and m.attachments != [], messages)
            if myLastMessage is None:
                await ctx.send("**Error. Could not find an image!**")
                return False
            #check if image
            myfiname = myLastMessage.attachments[0].filename.split(".")
            acceptableFiles = ["png","jpg","jpeg"]
            try:
                if not myfiname[len(myfiname) - 1] in acceptableFiles:
                    await ctx.send("**Error! Not a valid image.**")
            except:
                await ctx.send("**Error! Not a valid image.**")
                doexit = True
            try:
                url = myLastMessage.attachments[0].url
            except:
                import traceback
                traceback.print_exc()
                del traceback
            try:
                imageBinary = ""
                async with aiohttp.ClientSession() as session:
                    with aiohttp.Timeout(5):
                        async with session.get(url) as resp:
                            data = await resp.read()
                            b = BytesIO(data)
                            b.seek(0)
                            imageBinary = b.read()
                    
            except:
                await ctx.send("**Error. Could not fetch latest image!**")
                doexit = True
            blob = pgmagick.Blob(imageBinary)
            myimg = pgmagick.Image(blob)
            myimg.swirl(180)
            myfi = pgmagick.Blob()
            myimg.write(myfi)
            print(myfi.data)
            myDiscordFile = discord.File(myfi.data,filename='result.png')
        if doexit is True:
            return False
        await ctx.send(file=myDiscordFile)
                            
                
def setup(bot):
    bot.add_cog(imageDefs(bot))