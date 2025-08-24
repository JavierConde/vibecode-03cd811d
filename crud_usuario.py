import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="CRUD Usuario", version="1.0")

db: List["UsuarioInDB"] = []


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
    

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "usuario@example.com",
                "password": "password",
                "nombre": "Usuario Ejemplo",
            }
        }
    }


@app.post("/usuarios/", response_model=UsuarioInDB, status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario: UsuarioCreate):
    db_id = len(db) + 1
    new_usuario = UsuarioInDB(id=db_id, **usuario.dict())
    db.append(new_usuario)
    return new_usuario


@app.get("/usuarios/", response_model=List[UsuarioInDB])
async def read_usuarios():
    return db


@app.get("/usuarios/{usuario_id}", response_model=UsuarioInDB)
async def read_usuario(usuario_id: int):
    usuario = next((u for u in db if u.id == usuario_id), None)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario


@app.put("/usuarios/{usuario_id}", response_model=UsuarioInDB)
async def update_usuario(usuario_id: int, usuario: UsuarioUpdate):
    usuario_index = next((i for i, u in enumerate(db) if u.id == usuario_id), None)
    if usuario_index is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    update_data = usuario.dict(exclude_unset=True)
    updated_usuario = db[usuario_index]
    updated_usuario = UsuarioInDB(**updated_usuario.dict(), **update_data)
    db[usuario_index] = updated_usuario
    return updated_usuario


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int):
    usuario_index = next((i for i, u in enumerate(db) if u.id == usuario_id), None)
    if usuario_index is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    del db[usuario_index]