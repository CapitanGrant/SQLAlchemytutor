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
        # Создаем запрос для выбора всех пользоваетелей
        query = select(cls.model)
        # Выполняем запрос и получаем результат
        result = await session.execute(query)
        # Извлекаем записи как объекты моделей
        records = result.scalars().all()
        # Возвращаем список всех пользователей
        return records

    @classmethod
    async def get_username_id(cls, session: AsyncSession):
        # Создаем запрос для выборки id и username всех пользователей
        query = select(cls.model.id, cls.model.username) # Указываем конкретные колонки
        print(query) # Выводим запрос для отладки
        result = await session.execute(query) # Выполняем асинхронный запрос
        records = result.all() # Получаем все результаты
        return records # Возвращаем список записей

    @classmethod
    async def get_user_info(cls, session: AsyncSession, user_id: int):
        # Создаем запрос для выьорки по id
        query = select(cls.model).filter_by(id=user_id)
        print(query)
        # Выполняем асинхронный запрос
        result = await session.execute(query)
        user_info = result.scalar_one_or_none() # Получаем значение либо None
        return user_info # Возвращаем запись

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        records = result.scalars().all()
        return records
class ProfileDAO(BaseDAO):
    model = Profile


class CommentDAO(BaseDAO):
    model = Comment


class PostDAO(BaseDAO):
    model = Post
