import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field


app = FastAPI(title="CRUD Usuario", version="1.0.0")

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


class UsuarioResponse(BaseModel):
    id: int
    email: str
    password: str
    nombre: str


@app.post("/usuarios", response_model=UsuarioResponse, status_code=201, tags=["usuarios"])
async def create_usuario(usuario: UsuarioCreate):
    new_id = len(db) + 1
    new_usuario = UsuarioInDB(id=new_id, email=usuario.email, password=usuario.password, nombre=usuario.nombre)
    db.append(new_usuario.dict())
    return UsuarioResponse(**db[-1])


@app.get("/usuarios", response_model=List[UsuarioResponse], tags=["usuarios"])
async def get_usuarios():
    return [UsuarioResponse(**usuario) for usuario in db]


@app.get("/usuarios/{id}", response_model=UsuarioResponse, tags=["usuarios"])
async def get_usuario(id: int = Path(...)):
    for usuario in db:
        if usuario["id"] == id:
            return UsuarioResponse(**usuario)
    raise HTTPException(status_code=404, detail="Usuario not found")


@app.put("/usuarios/{id}", response_model=UsuarioResponse, tags=["usuarios"])
async def update_usuario(id: int = Path(...), usuario: UsuarioUpdate = ...):
    for i, u in enumerate(db):
        if u["id"] == id:
            updated_usuario = UsuarioInDB(**u, **usuario.dict(exclude_unset=True))
            db[i] = updated_usuario.dict()
            return UsuarioResponse(**db[i])
    raise HTTPException(status_code=404, detail="Usuario not found")


@app.delete("/usuarios/{id}", response_model=None, status_code=204, tags=["usuarios"])
async def delete_usuario(id: int = Path(...)):
    for i, u in enumerate(db):
        if u["id"] == id:
            del db[i]
            return
    raise HTTPException(status_code=404, detail="Usuario not found")