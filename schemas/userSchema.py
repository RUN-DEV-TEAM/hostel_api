from pydantic import BaseModel, EmailStr, constr,field_validator
from pydantic.types import SecretStr
from datetime import datetime



class UserSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


    @field_validator('password')
    def password_length_check(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

class ReturnSignUpUser(BaseModel):
    email: EmailStr
    password: SecretStr

class ProtectedRoutes(BaseModel):
    pass
  


class ListUser(BaseModel):
    id : int 
    email: EmailStr 
    status :str
    created_at : str 
    updated_at: str


class ListUser2(BaseModel):
    id : int 
    email: EmailStr 
    password: str
    status :str
    created_at : str 
    updated_at: str


class GetAuthUser(BaseModel):
    id : int 
    email: EmailStr
    token : str 
    status :str
    req_status: str | None
    created_at : str 
    updated_at: str


class Token(BaseModel):
    access_token: str
    token_type: str


