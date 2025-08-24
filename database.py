This code uses Pydantic for data modeling and an in-memory database for demonstration purposes.  For a production environment, you would replace the in-memory database with a persistent database like PostgreSQL, MySQL, or SQLite and use an appropriate ORM (like SQLAlchemy).

```python
from typing import List, Optional
from pydantic import BaseModel, Field

# In-memory database simulation (replace with a real database in production)
class InMemoryDatabase:
    def __init__(self):
        self.usuarios = {}
        self.tareas = {}
        self.next_usuario_id = 1
        self.next_tarea_id = 1

    def add_usuario(self, usuario):
        usuario.id = self.next_usuario_id
        self.usuarios[usuario.id] = usuario
        self.next_usuario_id += 1
        return usuario

    def get_usuario(self, usuario_id):
        return self.usuarios.get(usuario_id)

    def add_tarea(self, tarea):
        tarea.id = self.next_tarea_id
        self.tareas[tarea.id] = tarea
        self.next_tarea_id += 1
        return tarea

    def get_tareas_by_usuario(self, usuario_id):
        return [tarea for tarea in self.tareas.values() if tarea.usuario_id == usuario_id]


# Pydantic models
class Usuario(BaseModel):
    id: int = Field(..., ge=1)  # ge=1 ensures ID is at least 1
    email: str
    password: str
    nombre: str

    class Config:
        orm_mode = True #Enable ORM mode for easy database interaction


class Tarea(BaseModel):
    id: int = Field(..., ge=1)
    titulo: str
    descripcion: Optional[str] = None
    completada: bool
    usuario_id: int

    class Config:
        orm_mode = True

# Example usage
db = InMemoryDatabase()

# Create a user
nuevo_usuario = Usuario(email="test@example.com", password="password123", nombre="Test User")
usuario_creado = db.add_usuario(nuevo_usuario)
print(f"Usuario creado: {usuario_creado}")

# Create tasks for the user
tarea1 = Tarea(titulo="Tarea 1", descripcion="Descripción de la tarea 1", completada=False, usuario_id=usuario_creado.id)
tarea2 = Tarea(titulo="Tarea 2", completada=True, usuario_id=usuario_creado.id)

db.add_tarea(tarea1)
db.add_tarea(tarea2)

# Retrieve tasks for the user
tareas_usuario = db.get_tareas_by_usuario(usuario_creado.id)
print(f"Tareas del usuario {usuario_creado.id}: {tareas_usuario}")

```

Remember to replace the `InMemoryDatabase` with a proper database and ORM for a real-world application.  This example provides a basic structure and demonstrates the use of Pydantic for data validation and modeling.  The `orm_mode = True` in the Pydantic models allows for easy integration with ORMs later on.