from datetime import datetime
from typing import List

from GearTracker.objects.db import statics_table, player_prefs_table, static_members_table
from GearTracker.objects.enums import StaticRole
from sqlalchemy import null, and_, or_, join, select
from sqlalchemy.sql.selectable import FromClause, TableClause

# --------------
# Inserts
# --------------


def create_static(name: str, description: str = None):
    return statics_table.insert().values(
        name=name,
        description=description,
        created_ts=datetime.utcnow()
    )


def create_player_pref(discord_id: int, active_static_id: int = None):
    return player_prefs_table.insert().values(
        discord_id=discord_id,
        active_static_id=active_static_id
    )


def create_static_player(static_id: int, discord_id: int, nickname: str = None,
                         role: StaticRole = None, job_id: int = None, bis_id: int = None):
    return static_members_table.insert().values(
        static_id=static_id,
        discord_id=discord_id,
        nickname=nickname,
        role=role,
        job_id=job_id,
        bis_id=bis_id
    )

# --------------
# Selects
# --------------


def get_player_prefs_by_discord_id(discord_id: int):
    return player_prefs_table.select().where(player_prefs_table.c.discord_id == discord_id)


def get_statics_by_static_member_discord_id(discord_id: int):
    return select(statics_table.c.name, statics_table.c.id)\
        .join(statics_table)\
        .where(static_members_table.c.discord_id == discord_id)


def get_static_by_static_id(static_id: int):
    return statics_table.select().where(statics_table.c.id == static_id)


# --------------
# Updates
# --------------


def update_active_static_id(discord_id: int, static_id: int):
    return player_prefs_table.update()\
        .where(player_prefs_table.c.discord_id == discord_id)\
        .values(active_static_id=static_id)\
        .returning(*player_prefs_table.columns)
