from pydantic import BaseModel, EmailStr, constr,field_validator
from pydantic.types import SecretStr
from schemas.helperSchema import Gender
from datetime import datetime



class UserSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str


    @field_validator('password')
    def password_length_check(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

class ReturnSignUpUser(BaseModel):
    email: EmailStr
    password: SecretStr
    gender : str
    status: str
    user_type : str 

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
    user_type: str
    gender: str
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



class AuthUser(BaseModel):
    email : EmailStr
    user_type: str
    gender: str


class ResponseToken(BaseModel):
    access_token: str
    token_type: str
    user : AuthUser




class LoginUser(BaseModel):
    email: EmailStr
    password: str
