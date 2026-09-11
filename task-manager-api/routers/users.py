from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Field, SQLModel, Session, select

from db import get_session
from security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str


class UserCreate(SQLModel):
    username: str
    password: str


class UserRead(SQLModel):
    id: int
    username: str


@router.post("", status_code=201, response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing is not None:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user