This code uses Pydantic for data modeling and an in-memory database for demonstration purposes.  For a production environment, you'd replace `InMemoryDatabase` with a proper database driver like SQLAlchemy or Tortoise ORM.

```python
from typing import List, Optional
from pydantic import BaseModel, Field
from typing_extensions import Annotated

# Simulate an in-memory database (replace with a real database in production)
class InMemoryDatabase:
    def __init__(self):
        self.usuarios = {}
        self.tareas = {}
        self.next_usuario_id = 1
        self.next_tarea_id = 1

    def add_usuario(self, usuario):
        usuario.id = self.next_usuario_id
        self.next_usuario_id += 1
        self.usuarios[usuario.id] = usuario
        return usuario

    def get_usuario(self, usuario_id):
        return self.usuarios.get(usuario_id)

    def add_tarea(self, tarea):
        tarea.id = self.next_tarea_id
        self.next_tarea_id += 1
        self.tareas[tarea.id] = tarea
        return tarea

    def get_tareas_by_usuario(self, usuario_id):
        return [tarea for tarea in self.tareas.values() if tarea.usuario_id == usuario_id]


# Pydantic Models
class Usuario(BaseModel):
    id: Annotated[int, Field(ge=1)] = None  #ge=1 en Annotated para evitar 0 como id
    email: str
    password: str
    nombre: str

    class Config:
        orm_mode = True


class Tarea(BaseModel):
    id: Annotated[int, Field(ge=1)] = None #ge=1 en Annotated para evitar 0 como id
    titulo: str
    descripcion: Optional[str] = None
    completada: bool
    usuario_id: int

    class Config:
        orm_mode = True


# Example usage
db = InMemoryDatabase()

# Create a user
usuario1 = db.add_usuario(Usuario(email="test@example.com", password="password123", nombre="Test User"))
print(f"Usuario creado: {usuario1}")

# Create tasks for the user
tarea1 = db.add_tarea(Tarea(titulo="Tarea 1", descripcion="Descripción de la tarea 1", completa:False, usuario_id=usuario1.id))
tarea2 = db.add_tarea(Tarea(titulo="Tarea 2", completa:True, usuario_id=usuario1.id))
print(f"Tareas creadas: {tarea1}, {tarea2}")

# Retrieve tasks for the user
tareas_usuario1 = db.get_tareas_by_usuario(usuario1.id)
print(f"Tareas del usuario {usuario1.id}: {tareas_usuario1}")


#Retrieve a user
retrieved_user = db.get_usuario(usuario1.id)
print(f"Usuario recuperado: {retrieved_user}")

```

Remember to install `pydantic` :  `pip install pydantic`

This example provides a basic structure. For a real-world application, you would need a persistent database (like PostgreSQL, MySQL, SQLite) and a more robust ORM (like SQLAlchemy or Tortoise ORM) to manage database interactions.  The `orm_mode = True` in the Pydantic models is crucial for easy interaction with ORMs.