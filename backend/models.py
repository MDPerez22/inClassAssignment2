from tortoise import fields, models
import enum
import uuid
from pydantic import BaseModel

class roleEnum (str, enum.Enum):
    user = "user"
    admin = "admin"

class loginRequest (BaseModel):
    email:str
    password:str

class User (models.Model):
    id = fields.UUIDField(pk = True, default = uuid.uuid4)
    email = fields.CharField(max_length = 255, unique = True)
    hashed_password = fields.CharField(max_length = 255)
    is_active = fields.BooleanField(default = True)
    role = fields.CharEnumField(roleEnum, default=roleEnum.user)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"