from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine

def get_db() -> Generator[Session, None, None]:
    db = Session(engine)  # Create a session
    try:
        yield db  # Yield the session to the caller
    finally:
        db.close()  # Ensure the session is closed after use

SessionDep = Annotated[Session, Depends(get_db)]
