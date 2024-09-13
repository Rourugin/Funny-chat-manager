from typing import Any
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.database.models import async_session
from app.database.models import Chat, User, Item


async def set_chat(chat_name: str, chat_id: int) -> Any:
    query = select(Chat).where(Chat.chat_id == chat_id)
    async with async_session() as session:
        result = await session.execute(query)
        chat = result.scalar()
        if chat is not None:
            return None
        obj_chat = Chat(
            name=chat_name,
            chat_id=chat_id
        )
        session.add(obj_chat)
        await session.commit()


async def set_user(chat_id: int, user_id: int) -> Any:
    query = select(User).where(User.user_id == user_id)
    async with async_session() as session:
        result = await session.execute(query)
        user = result.scalar()
        if user is not None:
            return None
        obj_user = User(
            user_id=user_id,
            chat_id=chat_id,
            health=100,
            happiness=100,
            fatigue=0,
            money=1000,
            rate=0,
            bet=0,
            suit=None,
            nation=None,
            gender=None,
            city=None
        )
        session.add(obj_user)
        await session.commit()


async def set_item(chat_id: int, user_id: int) -> Any:
    query = select(Item).where(Item.user_id == user_id)
    async with async_session() as session:
        result = await session.execute(query)
        item = result.scalar()
        if item is not None:
            return None
        obj_item = Item(
            user_id=user_id,
            chat_id=chat_id,
            scooby_snack=0,
            five_for_threehundred=0,
            latex_suit=False,
            crusader_suit=False,
            clown_suit=False
        )
        session.add(obj_item)
        await session.commit()


async def get_user(user_id: int) -> User | None:
    query = select(User).where(User.user_id == user_id)
    async with async_session() as session:
        result = await session.execute(query)
        try:
            return result.scalar()
        except NoResultFound:
            return None


async def get_item(user_id: int) -> Item | None:
    query = select(Item).where(Item.user_id == user_id)
    async with async_session() as session:
        result = await session.execute(query)
        try:
            return result.scalar()
        except NoResultFound:
            return None