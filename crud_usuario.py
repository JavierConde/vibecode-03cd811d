import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field


app = FastAPI(title="Usuario CRUD", version="1.0.0")

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
    id: int = Field(..., ge=1)  # for clarity


@app.post("/usuarios", response_model=Usuario, status_code=201)
async def create_usuario(usuario: UsuarioCreate):
    id = len(db) + 1
    new_usuario = UsuarioInDB(**usuario.dict(), id=id)
    db.append(new_usuario.dict())
    return new_usuario


@app.get("/usuarios", response_model=List[Usuario])
async def read_usuarios():
    return db


@app.get("/usuarios/{id}", response_model=Usuario)
async def read_usuario(id: int = Path(..., gt=0)):
    usuario = [u for u in db if u["id"] == id]
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario[0]


@app.put("/usuarios/{id}", response_model=Usuario)
async def update_usuario(id: int = Path(..., gt=0), usuario: UsuarioUpdate = ...):
    usuario_index = next((i for i, item in enumerate(db) if item["id"] == id), None)
    if usuario_index is None:
        raise HTTPException(status_code=404, detail="Usuario not found")

    updated_usuario_data = usuario.dict(exclude_unset=True)
    db[usuario_index].update(updated_usuario_data)
    return db[usuario_index]


@app.delete("/usuarios/{id}", status_code=204)
async def delete_usuario(id: int = Path(..., gt=0)):
    usuario_index = next((i for i, item in enumerate(db) if item["id"] == id), None)
    if usuario_index is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    del db[usuario_index]
    return {"message": "Usuario deleted successfully"}

```

This code uses an in-memory list for simplicity.  For a production application, replace `db` with a proper database connection (e.g., using SQLAlchemy).  Also, note that password handling in this example is extremely insecure and should **never** be used in production.  Proper password hashing (e.g., using bcrypt or Argon2) is crucial.