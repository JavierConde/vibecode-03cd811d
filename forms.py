from pydantic import BaseModel, Field
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None  # Optional for creation
    email: str = Field(..., min_length=5, max_length=100) # ... indicates required field
    password: str = Field(..., min_length=8)
    nombre: str = Field(..., max_length=100)


class Tarea(BaseModel):
    id: Optional[int] = None  # Optional for creation
    titulo: str = Field(..., max_length=255)
    descripcion: Optional[str] = None
    completada: bool = False
    usuario_id: int = Field(..., ge=1) # ge=1 ensures a positive integer


class TareaCreate(BaseModel): # Separate model for creation to omit id
    titulo: str = Field(..., max_length=255)
    descripcion: Optional[str] = None
    completada: bool = False
    usuario_id: int = Field(..., ge=1)


class UsuarioUpdate(BaseModel): #Model for partial updates, all fields are optional
    email: Optional[str] = None
    password: Optional[str] = None
    nombre: Optional[str] = None

class TareaUpdate(BaseModel): #Model for partial updates, all fields are optional
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None


```

This code defines several Pydantic models:

* **`Usuario`:**  Represents a user with `id`, `email`, `password`, and `nombre` fields.  `id` is optional (for creating new users).  Email and password have basic validation.

* **`Tarea`:** Represents a task with `id`, `titulo`, `descripcion`, `completada`, and `usuario_id` fields.  `id` is optional.  `usuario_id` is validated to be a positive integer.

* **`TareaCreate`:** A separate model for creating tasks. This omits the `id` field as it's automatically generated.

* **`UsuarioUpdate` and `TareaUpdate`:**  Models specifically for partial updates. All fields are optional, allowing updates of only specific attributes.


This approach improves code organization and clarity, especially when handling create and update operations separately.  The validation built into Pydantic enhances data integrity. Remember to install Pydantic:  `pip install pydantic`