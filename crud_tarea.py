import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tarea CRUD", version="1.0.0")

db = []

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

    class Config:
        orm_mode = True


@app.post("/tareas/", response_model=TareaInDB, tags=["tareas"])
async def create_tarea(tarea: TareaCreate):
    id = len(db) + 1
    new_tarea = TareaInDB(**tarea.dict(), id=id)
    db.append(new_tarea)
    return new_tarea


@app.get("/tareas/", response_model=List[TareaInDB], tags=["tareas"])
async def read_tareas():
    return db


@app.get("/tareas/{tarea_id}", response_model=TareaInDB, tags=["tareas"])
async def read_tarea(tarea_id: int):
    tarea = next((tarea for tarea in db if tarea.id == tarea_id), None)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea not found")
    return tarea


@app.put("/tareas/{tarea_id}", response_model=TareaInDB, tags=["tareas"])
async def update_tarea(tarea_id: int, tarea: TareaUpdate):
    tarea_index = next((i for i, tarea in enumerate(db) if tarea.id == tarea_id), None)
    if tarea_index is None:
        raise HTTPException(status_code=404, detail="Tarea not found")
    tarea_data = tarea.dict(exclude_unset=True)
    updated_tarea = db[tarea_index].copy(update=tarea_data)
    db[tarea_index] = updated_tarea
    return updated_tarea


@app.delete("/tareas/{tarea_id}", tags=["tareas"])
async def delete_tarea(tarea_id: int):
    tarea_index = next((i for i, tarea in enumerate(db) if tarea.id == tarea_id), None)
    if tarea_index is None:
        raise HTTPException(status_code=404, detail="Tarea not found")
    del db[tarea_index]
    return {"message": "Tarea deleted successfully"}