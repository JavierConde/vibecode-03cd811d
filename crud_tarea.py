import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field


class TareaBase(BaseModel):
    titulo: str
    descripcion: str
    completada: bool
    usuario_id: int


class TareaCreate(TareaBase):
    pass


class TareaUpdate(TareaBase):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None
    usuario_id: Optional[int] = None


class TareaInDB(TareaBase):
    id: int


class Tarea(TareaInDB):
    pass


router = APIRouter(prefix="/tareas", tags=["tareas"])

db: List[TareaInDB] = []
next_id = 1


@router.post("/", response_model=Tarea)
async def create_tarea(tarea: TareaCreate):
    new_tarea = TareaInDB(**tarea.dict(), id=next_id)
    db.append(new_tarea)
    global next_id
    next_id += 1
    return new_tarea


@router.get("/", response_model=List[Tarea])
async def read_tareas():
    return db


@router.get("/{tarea_id}", response_model=Tarea)
async def read_tarea(tarea_id: int):
    tarea = find_tarea(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.put("/{tarea_id}", response_model=Tarea)
async def update_tarea(tarea_id: int, tarea: TareaUpdate):
    tarea_in_db = find_tarea(tarea_id)
    if tarea_in_db is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea_data = tarea.dict(exclude_unset=True)
    updated_tarea = TareaInDB(**tarea_in_db.dict(), **tarea_data)
    db[db.index(tarea_in_db)] = updated_tarea
    return updated_tarea


@router.delete("/{tarea_id}", response_model=None)
async def delete_tarea(tarea_id: int):
    tarea_in_db = find_tarea(tarea_id)
    if tarea_in_db is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.remove(tarea_in_db)
    return None



def find_tarea(tarea_id: int):
    for tarea in db:
        if tarea.id == tarea_id:
            return tarea
    return None

app = FastAPI()
app.include_router(router)