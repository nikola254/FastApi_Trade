from sqlalchemy import MetaData, String, Integer, TIMESTAMP, ForeignKey, Column, Table, JSON, Boolean
from datetime import datetime

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permission", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("role.id")),
    Column("is_active", Boolean,default=True, nullable=False),
    Column("is_superuser", Boolean,default=False, nullable=False),
    Column("is_verified", Boolean,default=False, nullable=False),
)