from passlib.context import CryptContext
from fastapi import Depends, status
from fastapi import  HTTPException
from datetime import datetime,timedelta
from sqlalchemy.ext.asyncio import async_sessionmaker
from services import admin_service
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from dependencies import get_session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def get_current_user(token: str = Depends(oauth2_scheme),  session: async_sessionmaker = Depends(get_session)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", 
                                         headers= {"www-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, "cd03aff8a2d3041e594dad10d5032985d1cc2fd831826b26ac6f987ab4d31a61", algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
    except:
        raise credential_exception
    user = await admin_service.get_user_4_auth_by_email_service(email, session)
    if user is None:
        raise credential_exception
    return user



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=int(expires_delta))
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,"cd03aff8a2d3041e594dad10d5032985d1cc2fd831826b26ac6f987ab4d31a61",algorithm="HS256")
    return encoded_jwt


def get_password_hashed(password):
    return pwd_context.hash(password)

def verify_password(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass,hashed_pass)



def build_response_dict_for_null_response(schema):
    response_dict = {}
    try:
        for field_name in schema.__fields__.keys():
            response_dict[field_name] = ""
    except KeyError:
        raise HTTPException(status_code=400, detail= "Error from catch for null formatting ...")
    else:
        return response_dict



async def authenticate_user(email:str, password:str,  session: async_sessionmaker):
    user = await admin_service.get_user_4_auth_by_email_service(email, session)
    if not user[0]:
        return False, {"message": f"User with the email {email} does not exist in our database"}
    user = user[1]
    if not verify_password(password, user["password"]):
        return False,{"message": "Invalid Email/Password supplied!"}
    user.update({"token": create_access_token(data={"sub":user["email"]},expires_delta=30)})
    return True,user 


