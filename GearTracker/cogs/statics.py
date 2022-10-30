import datetime

import discord
import sqlalchemy.exc
from discord import ApplicationContext
from discord.commands import SlashCommandGroup
from discord.ext import commands
from sqlalchemy import CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection

from GearTracker.bot import LootBot
from GearTracker.objects.enums import StaticRole
from GearTracker.queries import create_static, get_player_prefs_by_discord_id, create_player_pref, create_static_player


class StaticsCog(commands.Cog):
    bot: LootBot

    def __init__(self, bot):
        self.bot = bot

    static_commands = SlashCommandGroup("static", "Commands which deal with creation or administration of statics.")

    @static_commands.command(
        name="create",
        description="Creates a new static"
    )
    async def static_create(self, ctx: ApplicationContext,
                            name: discord.Option(str, "The name of the static", required=True)):
        """
        Slash Command to create a new static.

        :param ctx: The context of the invoked command
        :param name: The name of the static
        """

        async with self.bot.db.begin() as trans:
            try:
                cs_result: CursorResult = await trans.execute(create_static(name))
                gpp_result: CursorResult = await trans.execute(get_player_prefs_by_discord_id(ctx.author.id))
                if gpp_result.first() is None:
                    await trans.execute(create_player_pref(ctx.author.id, cs_result.inserted_primary_key.id))
                await trans.execute(create_static_player(
                    static_id=cs_result.inserted_primary_key.id,
                    discord_id=ctx.author.id,
                    role=StaticRole.OWNER
                ))
            except sqlalchemy.exc.SQLAlchemyError as sae:
                await trans.rollback()
                # Give some error response & probably log it
                await ctx.respond("Database error, rip")
            else:
                await trans.commit()

        embed = discord.Embed(
            color=discord.Colour.random(),
            title="Static Created",
            description=f"**Name:** {name}\n"
                        f"**Owner:** {ctx.author.mention}"
        )
        embed.set_footer(text=f"Sent at {discord.utils.format_dt(discord.utils.utcnow())}",
                         icon_url=self.bot.user.avatar.url)

        await ctx.respond(embed=embed)




