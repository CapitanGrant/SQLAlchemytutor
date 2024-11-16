from app.dao.dao import UserDAO
from app.user.schemas import UserPydantic, UserIDPydantic
from database import connection
from asyncio import run


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)


# all_users = run(select_all_users())
# for i in all_users:
#     user_pydantic = UserPydantic.from_orm(i)
#     print(user_pydantic.dict())
#
@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)


# rez = run(select_username_id())
# for user in rez:
#     data = UserIDPydantic.from_orm(user)
#     print(data.dict())
#
@connection
async def select_username_filter_by_id(session, user_id):
    rez = await UserDAO.get_user_info(session=session, user_id=user_id)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


# rez = run(select_username_filter_by_id(user_id=1))
# print(rez)

@connection
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


@connection
async def select_full_user_info_email(session, user_id: int, email: str):
    rez = await UserDAO.find_one_or_none(session=session, id=user_id, email=email)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}
