import datetime
from typing import Dict, Tuple, NamedTuple, Any, List, Sequence

import discord
import sqlalchemy.exc
from discord import ApplicationContext, AutocompleteContext
from discord.commands import SlashCommandGroup, OptionChoice
from discord.ext import commands
from sqlalchemy import CursorResult
from timeit import default_timer as timer

from GearTracker.bot import LootBot
from GearTracker.objects.embeds import ErrorEmbed
from GearTracker.objects.enums import StaticRole
from GearTracker.queries import create_static, get_player_prefs_by_discord_id, create_player_pref, \
    create_static_player, get_statics_by_static_member_discord_id, update_active_static_id, get_static_by_static_id


class SimpleCache(object):
    data: Any
    _expires: datetime.datetime

    def __init__(self, data):
        self.data = data
        self._expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)

    @property
    def expired(self) -> bool:
        return datetime.datetime.utcnow() > self._expires


class StaticsCog(commands.Cog):
    bot: LootBot

    # --------------
    # Init Stuff
    # --------------

    def __init__(self, bot):
        self.bot = bot
        self.cache = dict()

    static_commands = SlashCommandGroup("static", "Commands which deal with creation or administration of statics.")

    # --------------
    # Autocompletes
    # --------------

    async def static_switch_autocomplete(self, ctx: AutocompleteContext):

        # Get statics for which this discord User is a member
        async with self.bot.db.begin() as conn:
            results = await conn.execute(get_statics_by_static_member_discord_id(ctx.interaction.user.id))
            choices = results.all()

        # Now filter and sort the results
        if choices:
            ret = []
            for choice in choices:
                if ctx.value.lower() in str(choice.name).lower():
                    ret.append(OptionChoice(choice.name, choice.id))
            ret.sort(key=lambda x: x.name.lower())
            return first_x(ret, 20)
        return choices

    # --------------
    # Slash Commands
    # --------------

    @static_commands.command(
        name="create",
        description="Creates a new static"
    )
    async def static_create(self, ctx: ApplicationContext,
                            name: discord.Option(str, "The name of the static", required=True),
                            description: discord.Option(str, "A more detailed description of the static",
                                                        required=False)):
        """
        Slash Command to create a new static.

        :param ctx: The context of the invoked command
        :param name: The name of the static
        :param description: A more detailed description of the static. This is currently a Text field in the database.
        """

        db_start = timer()
        async with self.bot.db.begin() as trans:
            try:
                cs_result: CursorResult = await trans.execute(create_static(name, description=description))
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
                print(sae)
                # Give some error response & probably log it
                await ctx.respond("Database error, rip")
                return
            else:
                await trans.commit()

        db_end = timer()

        embed = discord.Embed(
            color=discord.Colour.random(),
            title="Static Created",
            description=f"**Name:** {name}\n"
                        f"**Owner:** {ctx.author.mention}",
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text=f"Completed in {db_end - db_start:.4f}s",
                         icon_url=self.bot.user.avatar.url)

        await ctx.respond(embed=embed)

    @static_commands.command(
        name="switch",
        description="Switch your active static"
    )
    async def static_switch(self, ctx: ApplicationContext,
                            static_id: discord.Option(int, "Choose the static to switch to",
                                                      autocomplete=static_switch_autocomplete)):

        start = timer()
        async with self.bot.db.connect() as conn:
            try:
                update_result = await conn.execute(update_active_static_id(ctx.author.id, static_id))
                pref_row = update_result.one()
                get_result = await conn.execute(get_static_by_static_id(pref_row.active_static_id))
                get_row = get_result.one()
            except sqlalchemy.exc.SQLAlchemyError as sae:
                print(f"Error: {sae}")
                await ctx.respond(embed=ErrorEmbed(title="Unable to update active static"))
                return
            else:
                await conn.commit()
        end = timer()

        embed = discord.Embed(title=f"Static Switched",
                              colour=discord.Color.random(),
                              timestamp=discord.utils.utcnow())
        embed.add_field(name=get_row.name,
                        value=get_row.description)
        embed.set_footer(text=f"Completed in {end - start:.4f}s",
                         icon_url=self.bot.user.avatar.url)

        await ctx.respond(embed=embed)


def first_x(item_list: Sequence[Any], x: int) -> Sequence[Any]:
    """
    Returns the first x items in the sequence, or the entire list if there are x or fewer items

    :param item_list: The sequence to truncate
    :param x: The number of items to preserve
    :return: The truncated sequence
    """
    if len(item_list) <= x:
        return item_list
    return item_list[:x]


def setup(bot: discord.Bot):
    bot.add_cog(StaticsCog(bot))
