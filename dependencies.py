
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import jwt
import models

from database import get_db
from auth import SECRET_KEY, ALGORITHM

# tokenUrl tells Swagger UI where the token can be obtained. It does not itself perform login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

print("oauth2_scheme: ",oauth2_scheme)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    current_user = db.query(models.User).filter(
        models.User.id == int(user_id)
    ).first()

    if current_user is None:
        raise credentials_exception

    return current_user
