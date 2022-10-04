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
import discord,math
from discord.ext import commands
import asyncio,random,traceback
import aiohttp,logging
from pymal.client import Client
from io import BytesIO
import os

class Anime(commands.Cog):
    def __init__(self,bot):
        self.client = ""
        self.bot = bot
        self.token = ""
        token = ""
        print(os.getcwd())
        with open(os.path.join(".", "tokens","mal-client-id.txt")) as myd:
            token = myd.readlines()
            token = token[0].strip("\r").strip("\n")
            print(token)
        self.client = Client(token)
        print(self.client)


    @discord.app_commands.command(name="search")
    async def AniSearch(self,ctx,name: str):
        await ctx.response.send_message("One moment... Searching...")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Anime Search",description="**Query: " + name + "**")
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        myAnimes = self.client.searchAnime(name,5,fields="alternative_titles,source,nsfw,rating,media_type,start_season")
        em.set_thumbnail(url=myAnimes[0].main_picture)
        for myAnime in myAnimes:
            myReturnText = "**Also Known As: **\n"
            if myAnime.alternative_titles.synonyms is not None:
                for entry in myAnime.alternative_titles.synonyms:
                    myReturnText = myReturnText + entry + "\n"
                myReturnText = myReturnText + "\n"
            if myAnime.alternative_titles.en != None:
                myReturnText = myReturnText + "**English Name:** " + myAnime.alternative_titles.en + "\n"
            if myAnime.alternative_titles.ja != None:
                myReturnText = myReturnText + "**Japanese Name:** " + myAnime.alternative_titles.ja + "\n"
            myReturnText = myReturnText + f"\n**Rating:** {myAnime.rating.human_rating} - {myAnime.rating.rating_desc}\n\n**Season: **{myAnime.start_season.season.capitalize()} {myAnime.start_season.year}"
            if myAnime.media_type != "":
                em.add_field(name=f"{myAnime.media_type.capitalize()}: {myAnime.title}",value=f"ID: {myAnime.id}\n{myReturnText}",inline=True)
            else:
                em.add_field(name=f"Entry: {myAnime.title}",value=f"ID: {myAnime.id}\n{myReturnText}",inline=True)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) anime-searched for {name}")
        await mymsg.edit(content="Search Complete!",embed=em)
        
async def setup(bot):
    bot = bot
    logging.info("Anime module activated.")
    await bot.add_cog(Anime(bot))