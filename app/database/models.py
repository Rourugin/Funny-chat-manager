import os
from dotenv import load_dotenv
from typing import Annotated, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
async_session = async_sessionmaker(engine)
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[intpk]
    name: Mapped[str]
    chat_id: Mapped[int]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    user_id: Mapped[int]
    chat_id: Mapped[int]
    health: Mapped[int]
    happiness: Mapped[int]
    fatigue: Mapped[int]
    money: Mapped[int]
    rate: Mapped[int]
    suit: Mapped[Optional[str]]
    nation: Mapped[Optional[str]]
    gender: Mapped[Optional[str]]
    city: Mapped[Optional[str]]


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[intpk]
    user_id: Mapped[int]
    chat_id: Mapped[int]
    scooby_snack: Mapped[int]
    five_for_threehundred: Mapped[int]
    latex_suit: Mapped[bool]
    crusader_suit: Mapped[bool]
    clown_suit: Mapped[bool]


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)