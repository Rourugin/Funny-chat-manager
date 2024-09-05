from sqlalchemy import select

from app.database.models import async_session
from app.database.models import Chat, User


async def set_user(chat_name: str, chat_id: int, user_id: int):
    obj_chat = Chat(
        name=chat_name,
        chat_id=chat_id
    )
    obj_user = User(
        user_id=user_id,
        chat_id=chat_id,
        health=100,
        happiness=100,
        fatigue=0,
        gender=None,
        city=None
    )
    async with async_session() as session:
        session.add(obj_chat)
        session.add(obj_user)
        await session.commit()


async def get_user(user_id: int) -> list:
    async with async_session() as session:
        stats = []
        query = select(User)
        result = await session.execute(query)
        for res in result.scalars():
            if res.id == user_id:
                stats = result.scalars()

    return stats
