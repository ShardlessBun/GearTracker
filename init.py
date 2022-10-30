import asyncio
import os
import sys
from abc import ABC

import sqlalchemy as sa
from discord.bot import Bot
from discord import Intents
from discord.ext import commands
from sqlalchemy.schema import CreateTable

from GearTracker.bot import LootBot

# Because Windows is terrible
if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# bot = LootBot(auto_sync_commands=True,
#               intents=Intents.default(),
#               debug_guilds=[os.environ.get("TEST_GUILD", [])])

bot = LootBot(auto_sync_commands=True,
              intents=Intents.default())

bot.run(os.environ.get("BOT_TOKEN"))
