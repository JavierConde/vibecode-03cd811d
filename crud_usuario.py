import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="CRUD API", version="1.0.0")

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
    

    class Config:
        orm_mode = True



class Usuario(UsuarioInDB):
    pass


@app.post("/usuarios/", response_model=Usuario, tags=["usuarios"])
async def create_usuario(usuario: UsuarioCreate):
    id = len(db) + 1
    new_usuario = UsuarioInDB(**usuario.dict(), id=id)
    db.append(new_usuario.dict())
    return new_usuario


@app.get("/usuarios/", response_model=List[Usuario], tags=["usuarios"])
async def read_usuarios():
    return db


@app.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["usuarios"])
async def read_usuario(usuario_id: int):
    for usuario in db:
        if usuario["id"] == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario not found")


@app.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["usuarios"])
async def update_usuario(usuario_id: int, usuario: UsuarioUpdate):
    for i, usuario_db in enumerate(db):
        if usuario_db["id"] == usuario_id:
            updated_usuario = UsuarioInDB(**usuario.dict(), id=usuario_id, **usuario_db)
            db[i] = updated_usuario.dict()
            return updated_usuario
    raise HTTPException(status_code=404, detail="Usuario not found")


@app.delete("/usuarios/{usuario_id}", tags=["usuarios"])
async def delete_usuario(usuario_id: int):
    for i, usuario in enumerate(db):
        if usuario["id"] == usuario_id:
            del db[i]
            return {"message": "Usuario deleted successfully"}
    raise HTTPException(status_code=404, detail="Usuario not found")