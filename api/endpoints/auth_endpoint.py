from fastapi import APIRouter,Depends, HTTPException, status
from dependencies import get_session
from api.endpoints import endpoint_helper
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from schemas.userSchema import Token

router = APIRouter()

# AUTH START
# pip install python-jose[cryptography] pip install passlib[bcrypt]  
# run "openssl rand -hex 32"  to generate SECRET_KEY
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),  session: async_sessionmaker = Depends(get_session)):
    user = await endpoint_helper.authenticate_user(form_data.username, form_data.password, session)
    if user["req_status"] == "nok":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=user, headers= {"www-Authenticate": "Bearer"})

    return {"access_token": user["token"], "token_type": "bearer"}
