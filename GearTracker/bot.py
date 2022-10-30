import os
from abc import ABC

import sqlalchemy as sa
import sqlalchemy.ext.asyncio
from discord.bot import Bot
from GearTracker.objects.db import metadata as meta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.sql.ddl import CreateTable


class LootBot(Bot, ABC):
    db: AsyncEngine

    def __int__(self, **kwargs):
        super(LootBot, self).__init__(**kwargs)

    async def on_ready(self):
        self.db = create_async_engine(os.environ["DATABASE_URL"], echo=True)
        async with self.db.begin() as conn:
            # await conn.run_sync(meta.drop_all)
            await conn.run_sync(meta.create_all)

        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
