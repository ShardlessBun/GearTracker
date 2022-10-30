import os
from abc import ABC

import sqlalchemy as sa
import sqlalchemy.ext.asyncio
from discord.bot import Bot
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


async def create_tables(conn: sqlalchemy.ext.asyncio.AsyncConnection):
    metadata = sa.MetaData()
    await conn.run_sync(metadata.create_all)


class LootBot(Bot, ABC):
    db: AsyncEngine

    def __int__(self, **kwargs):
        super(LootBot, self).__init__(**kwargs)

    async def on_ready(self):
        self.db = create_async_engine(os.environ["DATABASE_URL"], echo=True)
        async with self.db.connect() as conn:
            await create_tables(conn)

        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
