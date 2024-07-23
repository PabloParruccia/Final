from fastapi import APIRouter, Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from utils.jwt_manager import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, timedelta
from fastapi.exceptions import HTTPException
from typing import Annotated

token_router = APIRouter()

@token_router.post('/token', tags=['auth'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "rol": user.rol}, 
        user_id=user.id, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}