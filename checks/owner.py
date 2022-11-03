#!/usr/bin/python
# Copyright 2022 TDS (TheReddDragon)
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
def isowner(ctx):
    return ctx.message.author.id == 653787366548570123
def isowner_slash(ctx):
    return ctx.user.id == 653787366548570123