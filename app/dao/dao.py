from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.user.models import User, Profile, Post, Comment
from sqlalchemy import select

class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict) -> User:
        """
               Добавляет пользователя и привязанный к нему профиль.

               Аргументы:
               - session: AsyncSession - асинхронная сессия базы данных
               - user_data: dict - словарь с данными пользователя и профиля

               Возвращает:
               - User - объект пользователя
               """
        user = cls.model(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        session.add(user)
        await session.flush()
        profile = Profile(
            user_id=user.id,
            first_name=user_data['first_name'],
            last_name=user_data.get('last_name'),
            age=user_data.get('age'),
            gender=user_data['gender'],
            profession=user_data.get('profession'),
            interests=user_data.get('interests'),
            contacts=user_data.get('contacts')
        )
        session.add(profile)
        await session.commit()
        return user

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)
        records = result.scalar().all()
        return records

class ProfileDAO(BaseDAO):
    model = Profile


class CommentDAO(BaseDAO):
    model = Comment


class PostDAO(BaseDAO):
    model = Post
