from typing import List
from pydantic import BaseModel, ConfigDict
from app.user.sql_enums import GenderEnum, ProfessionEnum


class ProfilePydantic(BaseModel):
    first_name: str
    last_name: str | None
    age: int | None
    gender: GenderEnum
    profession: ProfessionEnum
    interests: List[str] | None
    contacts: dict | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserPydantic(BaseModel):
    username: str
    email: str
    profile: ProfilePydantic | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserIDPydantic(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
