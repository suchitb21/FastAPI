from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": False
            }
        }

class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    is_active: bool

    class Config:
        from_attributes = True # Enable ORM mode for serialization
     
class Settings(BaseModel):
    authjwt_secret_key:str='919be2e183128bafc3cd51c806b29f9f1d85630c4c58e6a114abb20cadf9e167'

class LoginModel(BaseModel):
    username:str
    password:str
    
class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    user_id:Optional[int]


    class Config:
        from_attributes=True
        json_schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }
