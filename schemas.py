from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


class Config:
    orm_mode = True
    schema_extra = {
        'example': {
            "username": "Gavhar",
            "email": "gavhar8730@gmail.com",
            "password": "password",
            "is_staff": False,
            "is_active": True
        }
    }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example": {
                "order_status": "PENDING"
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = 'dfbe7dc38ce9863157b8c00ac7ae09a203f8b896ace2eedfc600875ea1918fa7'


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = 'PENDING'
    pizza_size: Optional[str] = 'SMALL'
    user_id: Optional[int]
    user: Optional[int]


class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "quantity": 2,
            "pizza_size": "Large"
        }
    }
