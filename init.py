import asyncio
import os
import sys

from discord import Intents

from GearTracker.bot import LootBot

# Because Windows is terrible
if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# bot = LootBot(auto_sync_commands=True,
#               intents=Intents.default(),
#               debug_guilds=[os.environ.get("TEST_GUILD", [])])

bot = LootBot(auto_sync_commands=True,
              intents=Intents.default())

for filename in os.listdir('GearTracker/cogs'):
    if filename.endswith('.py'):
        bot.load_extensions()
        bot.load_extension(f'GearTracker.cogs.{filename[:-3]}')

bot.run(os.environ.get("BOT_TOKEN"))
