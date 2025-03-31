from sqlalchemy import Table, Column, Integer, String, MetaData, TIMESTAMP

meatadata = MetaData()


links = Table(
    "links",
    meatadata,
    Column("id", Integer, primary_key=True),
    Column("long_url", String, nullable=False),
    Column("short_code", String, nullable=False),
    Column("create_dt", TIMESTAMP, nullable=False),
    Column("expire_dt", TIMESTAMP, nullable=True),
    Column("last_queried_dt", TIMESTAMP, nullable=False),
    Column("user_id", String),
    Column("num_queries", Integer, nullable=False, default=0)
)