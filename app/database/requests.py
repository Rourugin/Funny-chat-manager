from sqlalchemy import select

from app.database.models import async_session
from app.database.models import Chat, User


async def set_user(chat_name: str, chat_id: int):
    obj = Chat(
        name=chat_name,
        chat_id=chat_id
    )
    async with async_session() as session:
        session.add(obj)
        await session.commit()