from pydantic import BaseModel, Field, EmailStr

class UsuarioBase(BaseModel):
    email: EmailStr
    password: str
    nombre: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True


class TareaBase(BaseModel):
    titulo: str
    descripcion: str
    completada: bool = False
    usuario_id: int

class TareaCreate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int

    class Config:
        orm_mode = True

```

This code defines several Pydantic models:

* **`UsuarioBase`**:  A base model for users, containing the common fields `email`, `password`, and `nombre`.  `EmailStr` ensures email validation.

* **`UsuarioCreate`**:  Inherits from `UsuarioBase`.  Used for creating new users.  No extra fields are needed here as all fields are required for creation.

* **`Usuario`**: Inherits from `UsuarioBase` and adds an `id` field.  The `class Config: orm_mode = True` is crucial for compatibility with ORMs like SQLAlchemy, allowing direct conversion from database objects to Pydantic models.

* **`TareaBase`**: A base model for tasks, containing `titulo`, `descripcion`, `completada` (with a default value of `False`), and `usuario_id`.

* **`TareaCreate`**: Inherits from `TareaBase`. Used for creating new tasks.

* **`Tarea`**: Inherits from `TareaBase` and adds an `id` field.  `orm_mode = True` is included for ORM compatibility.


These models are designed for clear separation of concerns and efficient use with FastAPI.  `UsuarioCreate` and `TareaCreate` are specifically for creating new entries, while `Usuario` and `Tarea` are used for representing existing entries, potentially retrieved from a database.  The inclusion of `orm_mode = True` is important for seamless integration with database operations.