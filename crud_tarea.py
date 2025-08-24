import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field


app = FastAPI()
router = APIRouter(prefix="/tasks", tags=["tasks"])

db: List[dict] = []


class TareaBase(BaseModel):
    titulo: str
    descripcion: str
    completada: bool
    usuario_id: int


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None
    usuario_id: Optional[int] = None


class TareaInDB(TareaBase):
    id: int

    class Config:
        orm_mode = True


@router.post("/", response_model=TareaInDB)
async def create_tarea(tarea: TareaCreate):
    id = len(db) + 1
    new_tarea = TareaInDB(**tarea.dict(), id=id)
    db.append(new_tarea.dict())
    return new_tarea


@router.get("/", response_model=List[TareaInDB])
async def read_tareas():
    return db


@router.get("/{tarea_id}", response_model=TareaInDB)
async def read_tarea(tarea_id: int):
    for tarea in db:
        if tarea["id"] == tarea_id:
            return TareaInDB(**tarea)
    raise HTTPException(status_code=404, detail="Tarea not found")


@router.put("/{tarea_id}", response_model=TareaInDB)
async def update_tarea(tarea_id: int, tarea: TareaUpdate):
    for i, tarea_db in enumerate(db):
        if tarea_db["id"] == tarea_id:
            tarea_db.update(tarea.dict(exclude_unset=True))
            return TareaInDB(**tarea_db)
    raise HTTPException(status_code=404, detail="Tarea not found")


@router.delete("/{tarea_id}")
async def delete_tarea(tarea_id: int):
    for i, tarea in enumerate(db):
        if tarea["id"] == tarea_id:
            del db[i]
            return {"message": "Tarea deleted successfully"}
    raise HTTPException(status_code=404, detail="Tarea not found")

app.include_router(router)