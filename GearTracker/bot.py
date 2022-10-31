import os
from abc import ABC

from discord.bot import Bot
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from timeit import default_timer

from GearTracker.objects.db import metadata as meta


class LootBot(Bot, ABC):
    db: AsyncEngine

    def __int__(self, **kwargs):
        super(LootBot, self).__init__(**kwargs)

    async def on_ready(self):
        start = default_timer()
        self.db = create_async_engine(os.environ["DATABASE_URL"], echo=True)
        async with self.db.begin() as conn:
            # await conn.run_sync(meta.drop_all)
            await conn.run_sync(meta.create_all)
        end = default_timer()

        print(f"Logged in as {self.user} (ID: {self.user.id}) in {end-start:.4f}s")
        print("------")
