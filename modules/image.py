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

#THIS IS LEGACY CODE I DON'T UNDERSTAND
import discord,math
from discord.ext import commands
import asyncio,random
import aiohttp,logging
from io import BytesIO
import pgmagick,async_timeout

aiohttp.Timeout = async_timeout.timeout
class imageDefs(commands.Cog):
    def apiget(self,url,endpoint):
        try:
            import requests
            r = requests.get(url)
            return r.json()[endpoint]
        except:
            return False
            traceback.print_exc()
    def ___init___(self,bot):
        self.bot = bot
    
    @discord.app_commands.command(name="plode",description="Implode an image, or explode it!")
    async def doimplosion(self,ctx,size: float):
        """IMPLODE"""
        doexit = False
        async with ctx.channel.typing():
            messages = [message async for message in ctx.channel.history(limit=100)]
            myLastMessage = discord.utils.find(lambda m: m.attachments != None and m.guild == ctx.guild and m.attachments != [], messages)
            if myLastMessage is None:
                await ctx.response.send_message("**Error. Could not find an image!**")
                return False
            #check if image
            myfiname = myLastMessage.attachments[0].filename.split(".")
            acceptableFiles = ["png","jpg","jpeg"]
            try:
                if not myfiname[len(myfiname) - 1] in acceptableFiles:
                    await ctx.response.send_message("**Error! Not a valid image.**")
            except:
                await ctx.response.send_message("**Error! Not a valid image.**")
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
                await ctx.response.send_message("**Error. Could not fetch latest image!**")
                doexit = True
            blob = pgmagick.Blob(imageBinary)
            myimg = pgmagick.Image(blob)
            if size >= 1:
                size = 1
            myimg.implode(size)
            myfi = pgmagick.Blob()
            myimg.write(myfi)
            myImgTest = BytesIO(myfi.data)
            myDiscordFile = discord.File(myImgTest,filename='result.png')
        if doexit is True:
            return False
        logging.info("User {0}#{1} (<@{2}>) ploded image in guild {3}".format(ctx.user.name,ctx.user.discriminator,ctx.user.id,ctx.guild.id))
        await ctx.response.send_message("I did it! Ploded image with size of {0}".format(size),file=myDiscordFile)
        
    @discord.app_commands.command(name="swirl",description="Give an image a SWIIIIIIRL")
    async def doswirl(self,ctx,factor:int = 180):
        """do a curl, do a swirl"""
        if factor == 0:
            await ctx.response.send_message("Can't do a swirl with a factor of 0 :(")
            return
        doexit = False
        async with ctx.channel.typing():
            messages = [message async for message in ctx.channel.history(limit=100)]
            myLastMessage = discord.utils.find(lambda m: m.attachments != None and m.guild == ctx.guild and m.attachments != [], messages)
            if myLastMessage is None:
                await ctx.response.send_message("**Error. Could not find an image!**")
                return False
            #check if image
            myfiname = myLastMessage.attachments[0].filename.split(".")
            acceptableFiles = ["png","jpg","jpeg"]
            try:
                if not myfiname[len(myfiname) - 1] in acceptableFiles:
                    await ctx.response.send_message("**Error! Not a valid image.**")
            except:
                await ctx.response.send_message("**Error! Not a valid image.**")
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
                await ctx.response.send_message("**Error. Could not fetch latest image!**")
                doexit = True
            blob = pgmagick.Blob(imageBinary)
            myimg = pgmagick.Image(blob)
            myimg.swirl(factor)
            myfi = pgmagick.Blob()
            myimg.write(myfi)
            mydata = BytesIO(myfi.data)
            myDiscordFile = discord.File(mydata,filename='result.png')
        if doexit is True:
            return False
        logging.info("User {0}#{1} (<@{2}>) swirled image in guild {3}".format(ctx.user.name,ctx.user.discriminator,ctx.user.id,ctx.guild.id))
        await ctx.response.send_message("I did it! Swirled image by factor of {0}".format(factor),file=myDiscordFile)

    @discord.app_commands.command(name="deepfry")
    async def deepfryimage(self,ctx,type:int = 1):
        doexit = False
        async with ctx.channel.typing():
            messages = [message async for message in ctx.channel.history(limit=100)]
            myLastMessage = discord.utils.find(lambda m: m.attachments != None and m.guild == ctx.guild and m.attachments != [], messages)
            if myLastMessage is None:
                await ctx.response.send_message("**Error. Could not find an image!**")
                return False
            #check if image
            myfiname = myLastMessage.attachments[0].filename.split(".")
            acceptableFiles = ["png","jpg","jpeg"]
            try:
                if not myfiname[len(myfiname) - 1] in acceptableFiles:
                    await ctx.response.send_message("**Error! Not a valid image.**")
            except:
                await ctx.response.send_message("**Error! Not a valid image.**")
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
                await ctx.response.send_message("**Error. Could not fetch latest image!**")
                doexit = True
            noisetype = pgmagick.NoiseType
            if type == 0:
                noisetype = pgmagick.NoiseType.UniformNise
            elif type == 1:
                noisetype = pgmagick.NoiseType.GaussianNoise
            elif type == 2:
                noisetype = pgmagick.NoiseType.MultiplicativeGaussianNoise
            elif type == 3:
                noisetype = pgmagick.NoiseType.ImpulseNoise
            elif type == 4:
                noisetype = pgmagick.NoiseType.LaplassianNoise
            elif type == 5:
                noisetype = pgmagick.NoiseType.PoissonNoise
            await ctx.response.send_message("Thinking... Please be patient")
            blob = pgmagick.Blob(imageBinary)
            myimg = pgmagick.Image(blob)
            myimg.equalize()
            myGeo = pgmagick.Geometry("99%")
            myimg.extent(myGeo)
            myGeo = pgmagick.Geometry("1%")
            myimg.border(myGeo)
            myimg.gamma(0.7)
            myimg.gamma(1.3)
            myimg.reduceNoise()
            myimg.modulate(120,40,100)
            myimg.modulate(100,150,100)
            myimg.modulate(100,150,90)
            myimg.normalize()
            myimg.contrast(50)
            myimg.addNoise(noisetype)
            myGeo = pgmagick.Geometry("109%x91%")
            myimg.resize(myGeo)
            myGeo = pgmagick.Geometry("90%x110%")
            myfi = pgmagick.Blob()
            myimg.write(myfi)
            mydata = BytesIO(myfi.data)
            myDiscordFile = discord.File(mydata,filename='result.png')
            if doexit is True:
                return False
            logging.info("User {0}#{1} (<@{2}>) deepfried image in guild {3}".format(ctx.user.name,ctx.user.discriminator,ctx.user.id,ctx.guild.id))
            await ctx.channel.send("I did it! Deepfried image! ",file=myDiscordFile)
                
async def setup(bot):
    bot = bot
    await bot.add_cog(imageDefs(bot))