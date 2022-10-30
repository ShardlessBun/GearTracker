from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Column, Integer, BigInteger, DateTime, null, BOOLEAN, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ENUM

from GearTracker.objects.enums import EventType, ItemType, SourceType, StaticRole

db = declarative_base()
metadata = sa.MetaData()

# id_pk_column = Column("id", Integer, primary_key=True, autoincrement='auto')
item_type_enum = ENUM(ItemType, name="item_type")
source_type_enum = ENUM(SourceType, name="source_type")
static_role_enum = ENUM(StaticRole, name="static_role")
event_type_enum = ENUM(EventType, name="event_type")


statics_table = sa.Table(
    "statics",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("name", String, nullable=False),
    Column("description", Text),
    Column("created_ts", DateTime, default=datetime.utcnow(), nullable=False)
)

player_prefs_table = sa.Table(
    "player_prefs",
    metadata,
    Column("discord_id", BigInteger, primary_key=True),
    Column("active_static_id", None, ForeignKey("statics.id"), nullable=False)
)

jobs_table = sa.Table(
    "jobs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("abbrev", String(3), nullable=False),
    Column("name", String, nullable=False)
)

gearsets_table = sa.Table(
    "gearsets",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("etro_uuid", String, nullable=False),
    # Column("static_member_id", None, ForeignKey("static_members.id"), nullable=False),
    Column("last_synced", DateTime, default=datetime.utcnow(), nullable=False)
)

gearset_items_table = sa.Table(
    "gearset_items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("gearset_id", None, ForeignKey("gearsets.id"), nullable=False),
    Column("etro_id", Integer, nullable=False),
    Column("type", item_type_enum, nullable=False),
    Column("source", source_type_enum, nullable=False),
    Column("name", String),
    Column("upgraded", BOOLEAN, default=null())
)

static_members_table = sa.Table(
    "static_members",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("static_id", None, ForeignKey("statics.id")),
    Column("discord_id", BigInteger, nullable=False),
    Column("nickname", String),
    Column("role", static_role_enum, default=StaticRole.MEMBER),
    Column("job_id", None, ForeignKey("jobs.id"), nullable=True),
    Column("bis_id", None, ForeignKey("gearsets.id"), nullable=True)
)

item_events_table = sa.Table(
    "item_events",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("logged_at", DateTime, default=datetime.utcnow()),
    Column("logged_by", BigInteger, nullable=False),
    Column("static_player_id", None, ForeignKey("static_members.id"), nullable=False),
    Column("job_id", None, ForeignKey("jobs.id"), nullable=False),
    Column("event_type", event_type_enum, nullable=False),
    Column("type", item_type_enum, nullable=False),
    Column("source", source_type_enum, nullable=False)
)
