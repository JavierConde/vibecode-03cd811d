This code uses Pydantic for data modeling and an in-memory database for simplicity.  For a production environment, you would replace the `InMemoryDatabase` with a real database like PostgreSQL, MySQL, or SQLite and an appropriate ORM (like SQLAlchemy or Tortoise ORM).

```python
from typing import List, Optional
from pydantic import BaseModel, Field

# In-memory database simulation (replace with a real database in production)
class InMemoryDatabase:
    def __init__(self):
        self.usuarios = []
        self.tareas = []
        self.next_usuario_id = 1
        self.next_tarea_id = 1

    def add_usuario(self, usuario):
        usuario.id = self.next_usuario_id
        self.next_usuario_id += 1
        self.usuarios.append(usuario)
        return usuario

    def get_usuario(self, usuario_id):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def add_tarea(self, tarea):
        tarea.id = self.next_tarea_id
        self.next_tarea_id +=1
        self.tareas.append(tarea)
        return tarea

    def get_tareas_by_usuario(self, usuario_id):
        return [tarea for tarea in self.tareas if tarea.usuario_id == usuario_id]


# Pydantic Models
class Usuario(BaseModel):
    id: int = Field(..., alias="_id") #alias para evitar conflicto con id de la base de datos.
    email: str
    password: str
    nombre: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class Tarea(BaseModel):
    id: int = Field(..., alias="_id")
    titulo: str
    descripcion: str
    completada: bool
    usuario_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Example Usage
db = InMemoryDatabase()

# Crear usuarios
usuario1 = Usuario(email="test@example.com", password="password123", nombre="Usuario 1")
usuario1 = db.add_usuario(usuario1) #guarda en la base de datos
usuario2 = Usuario(email="test2@example.com", password="password456", nombre="Usuario 2")
usuario2 = db.add_usuario(usuario2)

# Crear tareas
tarea1 = Tarea(titulo="Tarea 1", descripcion="Descripción de la tarea 1", completada=False, usuario_id=usuario1.id)
tarea1 = db.add_tarea(tarea1)
tarea2 = Tarea(titulo="Tarea 2", descripcion="Descripción de la tarea 2", completada=True, usuario_id=usuario2.id)
tarea2 = db.add_tarea(tarea2)

# Obtener tareas de un usuario
tareas_usuario1 = db.get_tareas_by_usuario(usuario1.id)
print(f"Tareas de Usuario 1: {tareas_usuario1}")

# Obtener un usuario
usuario_obtenido = db.get_usuario(usuario1.id)
print(f"Usuario obtenido: {usuario_obtenido}")

```

Remember to replace the `InMemoryDatabase` with a proper database and ORM for a production-ready application.  This example provides a basic structure to get started.  Error handling and more sophisticated database interactions should be added for robustness.