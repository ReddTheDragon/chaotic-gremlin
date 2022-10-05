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
from pymal.client import Client, BadRequestException
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
    @discord.app_commands.command(name="anime")
    async def AniGrab(self,ctx,id: str):
        await ctx.response.send_message("One moment...")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Anime Query",description="**ID: " + str(id) + "**")
        myAnime = ""
        myAnime = self.client.get_anime(id,fields="alternative_titles,nsfw,rating,media_type,start_season,status,synopsis,mean,num_list_users,num_scoring_users,genres,num_episodes,studios,genres")
        if myAnime.nsfw.nsfw_id == 1 or myAnime.nsfw.nsfw_id == 0:
            if ctx.channel.nsfw == False:
                tag = ""
                if myAnime.nsfw.nsfw_id == 1:
                    tag = "potential NSFW"
                elif myAnime.nsfw.nsfw_id == 0:
                    tag = "NSFW"
                else:
                    tag = "<<<THERE HAS BEEN AN ERROR PLEASE CONTACT BOT DEV>>>"
                    logging.critical(f"<<<BUG ALERT>>> Anime {myAnime.title} (id {myAnime.id}) has NSFW ID of {myAnime.nsfw.nsfw_id}.")
                em.description = em.description + f"\nSorry, but I cannot display {tag} anime in this chat. Please try again in an age-restricted channel."
                em.color=discord.Color.red()
                await mymsg.edit(content="Error retrieving anime...",embed=em)
                return
        em.description = em.description + f"\n**Name:** {myAnime.title}\n**Media Type:** {myAnime.media_type}\n**Mean Rating:** {myAnime.mean}\n**Number of Episodes:** {myAnime.num_episodes}\n**Status:** {myAnime.status.readable_status.capitalize()}\n"
        if myAnime.start_season is not None:
            em.description = em.description + f"**Start Season:** {myAnime.start_season.season.capitalize()} {myAnime.start_season.year}\n**Rated {myAnime.rating.human_rating} - {myAnime.rating.rating_desc}**\n"
        em.description = em.description + f"**Safety:** *{myAnime.nsfw.isnsfw.capitalize()}*"
        akaData = ""
        studiosData = ""
        if myAnime.alternative_titles.synonyms is not None:
            for i in myAnime.alternative_titles.synonyms:
                akaData = akaData + f"{i}\n"
            em.add_field(name=f"Also Known As",value=f"{akaData}",inline=False)
        if myAnime.alternative_titles.en != '':
            em.add_field(name=f"English Name",value=f"{myAnime.alternative_titles.en}",inline=False)
        if myAnime.alternative_titles.ja != '':
            em.add_field(name=f"Japanese Name",value=f"{myAnime.alternative_titles.ja}",inline=False)
        if myAnime.studios is not None:
            studiosData = ""
            for i in myAnime.studios.studios:
                studiosData = studiosData + f"{i.name}\n"
            em.add_field(name=f"Studios",value=f"{studiosData}",inline=False)
        if myAnime.genres is not None:
            genresData = ""
            for i in myAnime.genres.genres:
                genresData = genresData + f"{i.name}\n"
            em.add_field(name=f"Genres",value=f"{genresData}",inline=False)
        em.set_image(url=myAnime.main_picture)
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        if myAnime.synopsis is not None:
            if len(myAnime.synopsis) > 950:
                em.add_field(name="Synopsis",value=f"||{myAnime.synopsis[0:950]}... View the rest on MAL.||",inline=False)
            else:
                em.add_field(name="Synopsis",value=f"||{myAnime.synopsis}||",inline=False)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) anime-grabbed {myAnime.id} ({myAnime.title}) in guild {ctx.guild_id}")
        await mymsg.edit(content="I found your anime!",embed=em)


    def handleReturnText(self,anime,embed):
        myReturnText = "**Also Known As: **\n"
        if anime.alternative_titles.synonyms is not None:
            for entry in anime.alternative_titles.synonyms:
                myReturnText = myReturnText + entry + "\n"
            myReturnText = myReturnText + "\n"
        if anime.alternative_titles.en != None:
            myReturnText = myReturnText + "**English Name:** " + anime.alternative_titles.en + "\n"
        if anime.alternative_titles.ja != None:
            myReturnText = myReturnText + "**Japanese Name:** " + anime.alternative_titles.ja + "\n"
        myReturnText = myReturnText + f"\n**Rating:** {anime.rating.human_rating} - {anime.rating.rating_desc}\n\n"
        if anime.start_season is not None:
            myReturnText = myReturnText + f"**Season: **{anime.start_season.season.capitalize()} {anime.start_season.year}"
        if anime.media_type != "":
            embed.add_field(name=f"{anime.media_type.capitalize()}: {anime.title}",value=f"ID: {anime.id}\n{myReturnText}")
        else:
            embed.add_field(name=f"Entry: {anime.title}",value=f"ID: {anime.id}\n{myReturnText}")
        return anime, embed

    @discord.app_commands.command(name="search")
    async def AniSearch(self,ctx,name: str):
        await ctx.response.send_message("One moment... Searching...  If this takes more than a few seconds, please try again with a longer search string.")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Anime Search",description="**Query: " + name + "**")
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        # lazy code
        pageData, myAnimes = self.client.searchAnime(name,20,fields="alternative_titles,source,rating,media_type,start_season,nsfw")
        # set the thumbnail if it is safe for work
        for i in myAnimes:
            if i.nsfw.nsfw_id == 2:
                em.set_thumbnail(url=i.main_picture)
        totalAnimesListed = 0
        while totalAnimesListed < 5:
            for myAnime in myAnimes:
                totalAnimesListed = totalAnimesListed + 1
                if totalAnimesListed == 6:
                    break
                if myAnime.nsfw.nsfw_id == 1 or myAnime.nsfw.nsfw_id == 0:
                    if ctx.channel.nsfw == True:
                        myAnime, em = self.handleReturnText(myAnime, em)
                    else:
                        totalAnimesListed = totalAnimesListed - 1
                else:
                    myAnime, em = self.handleReturnText(myAnime, em)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) anime-searched for \"{name}\" in guild {ctx.guild_id}")
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        await mymsg.edit(content="Search Complete!",embed=em)
tree = ""
async def setup(bot):
    bot = bot
    tree = bot.tree
    logging.info("Anime module activated.")
    await bot.add_cog(Anime(bot))