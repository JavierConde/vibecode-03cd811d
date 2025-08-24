import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field

app = FastAPI()
router = APIRouter(prefix="/users", tags=["users"])

db: List[dict] = []


class UsuarioBase(BaseModel):
    email: str
    password: str
    nombre: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(UsuarioBase):
    email: Optional[str] = None
    password: Optional[str] = None
    nombre: Optional[str] = None


class UsuarioInDB(UsuarioBase):
    id: int


class Usuario(UsuarioInDB):
    pass


@router.post("/", response_model=Usuario)
async def create_user(user: UsuarioCreate):
    id = len(db) + 1
    new_user = UsuarioInDB(**user.dict(), id=id)
    db.append(new_user.dict())
    return new_user


@router.get("/", response_model=List[Usuario])
async def read_users():
    return db


@router.get("/{user_id}", response_model=Usuario)
async def read_user(user_id: int):
    for user in db:
        if user["id"] == user_id:
            return Usuario(**user)
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/{user_id}", response_model=Usuario)
async def update_user(user_id: int, user: UsuarioUpdate):
    for i, user_db in enumerate(db):
        if user_db["id"] == user_id:
            update_data = user.dict(exclude_unset=True)
            db[i] = {**user_db, **update_data}
            return Usuario(**db[i])
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", response_model=None)
async def delete_user(user_id: int):
    for i, user in enumerate(db):
        if user["id"] == user_id:
            del db[i]
            return
    raise HTTPException(status_code=404, detail="User not found")

app.include_router(router)