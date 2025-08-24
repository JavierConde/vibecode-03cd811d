import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field

app = FastAPI()
router = APIRouter(prefix="/tasks", tags=["tasks"])

db = []

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
    id: uuid.UUID

    class Config:
        orm_mode = True

@router.post("/", response_model=TareaInDB, status_code=201)
async def create_tarea(tarea: TareaCreate):
    id = uuid.uuid4()
    new_tarea = TareaInDB(id=id, **tarea.dict())
    db.append(new_tarea)
    return new_tarea

@router.get("/", response_model=List[TareaInDB])
async def read_tareas():
    return db

@router.get("/{tarea_id}", response_model=TareaInDB)
async def read_tarea(tarea_id: uuid.UUID):
    tarea = next((tarea for tarea in db if tarea.id == tarea_id), None)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea not found")
    return tarea

@router.put("/{tarea_id}", response_model=TareaInDB)
async def update_tarea(tarea_id: uuid.UUID, tarea: TareaUpdate):
    tarea_index = next((i for i, tarea in enumerate(db) if tarea.id == tarea_id), None)
    if tarea_index is None:
        raise HTTPException(status_code=404, detail="Tarea not found")
    updated_tarea = TareaInDB(**db[tarea_index].dict(), **tarea.dict())
    db[tarea_index] = updated_tarea
    return updated_tarea

@router.delete("/{tarea_id}", status_code=204)
async def delete_tarea(tarea_id: uuid.UUID):
    tarea_index = next((i for i, tarea in enumerate(db) if tarea.id == tarea_id), None)
    if tarea_index is None:
        raise HTTPException(status_code=404, detail="Tarea not found")
    del db[tarea_index]

app.include_router(router)

```

This code defines the Pydantic models, the FastAPI router with endpoints for CRUD operations, and uses an in-memory list as a database.  Remember that this in-memory DB is for demonstration only and will not persist data between runs.  For a production environment, you would replace `db` with a proper database connection.  I've also corrected the `id` field to use `uuid.UUID` as requested.