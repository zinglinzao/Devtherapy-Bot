from sqlalchemy import Column, Integer, String, Select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import typing

# Define the database
engine = create_async_engine(
    "sqlite+aiosqlite:///users.db", echo=False
)  # enable if you need logs
Base = declarative_base()

# Define the User table
class User(Base):
    __tablename__ = "records"
    discord_id = Column(Integer, primary_key=True)
    api_key = Column(String, nullable=False)
    llm_model = Column(String, nullable=False)
    prompt = Column(String, nullable=False)

db_factory = async_sessionmaker(engine, expire_on_commit=False)

async def add_record(record: typing.Type[Base]) -> None:
    """
    record should be inherited object from Base
    :param record:
    :return:
    """
    async with db_factory() as session:
        session.add(record)
        await session.commit()


async def update_record(statement) -> None:
    async with db_factory() as session:
        res = await session.execute(statement)
        if res.rowcount == 0:
            raise Exception("No rows were affected")
        await session.commit()

async def query_record(sql_statement) -> typing.Any | None:
    """
    useful for single return statements
    """
    async with db_factory() as session:
        return (await session.execute(sql_statement)).scalar_one_or_none()
