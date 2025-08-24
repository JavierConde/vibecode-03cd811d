from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None  # Optional for creating new users
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=8, description="Contraseña del usuario (mínimo 8 caracteres)")
    nombre: str = Field(..., description="Nombre del usuario")

    class Config:
        orm_mode = True # Enable ORM mode if using with databases like SQLAlchemy


class Tarea(BaseModel):
    id: Optional[int] = None  # Optional for creating new tasks
    titulo: str = Field(..., description="Título de la tarea")
    descripcion: Optional[str] = None  # Optional description
    completada: bool = Field(False, description="Indica si la tarea está completada")
    usuario_id: int = Field(..., description="ID del usuario al que pertenece la tarea")

    class Config:
        orm_mode = True

# Ejemplo de uso:
# usuario = Usuario(email="test@example.com", password="password123", nombre="Test User")
# tarea = Tarea(titulo="Tarea 1", usuario_id=1)

# print(usuario.model_dump_json())
# print(tarea.model_dump_json())
```

Este código define dos modelos Pydantic, `Usuario` y `Tarea`, basados en su especificación.  He incluido:

* **`Optional[int]` para `id`:**  Esto permite crear nuevos objetos sin proporcionar un ID, que generalmente es auto-incremental en una base de datos.
* **`Field(...)`:**  Se utiliza para agregar metadatos como descripciones a los campos.  Esto es útil para la documentación automática de la API.
* **`EmailStr` para `email`:**  Valida que el email sea una dirección de correo electrónico válida.
* **`min_length=8` para `password`:**  Impone una restricción de longitud mínima para la contraseña.
* **`orm_mode = True`:** Esta configuración permite que estos modelos se mapeen directamente con objetos de bases de datos (ORMs) como SQLAlchemy, facilitando la interacción con la base de datos.


Recuerda instalar Pydantic: `pip install pydantic`

Este código proporciona una base sólida para formularios.  Puedes extenderlo añadiendo validaciones adicionales, campos opcionales o tipos de datos más complejos según sea necesario.