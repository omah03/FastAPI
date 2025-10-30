from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth2
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    verified = utils.verify(user_credentials.password, user.password)
    if not verified:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # # Create a token for the user
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # # return token 
    return {
        "access_token" : access_token,
        "token_type": "bearer"
    }