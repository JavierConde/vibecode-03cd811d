from pydantic import BaseModel, Field, EmailStr


class UsuarioBase(BaseModel):
    email: EmailStr
    password: str
    nombre: str

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


class TareaCreate(TareaBase):
    pass


class Tarea(TareaBase):
    id: int

    class Config:
        orm_mode = True

```

This code defines Pydantic models for `Usuario` and `Tarea`.  Note the following:

* **`UsuarioBase` and `TareaBase`:** These are base models containing only the fields needed for creating a new user or task.  `orm_mode = True` is crucial for easy integration with ORMs like SQLAlchemy.

* **`UsuarioCreate` and `TareaCreate`:** These models inherit from their respective base models and are used specifically for creating new instances.  This allows you to enforce validation rules only needed during creation.

* **`Usuario` and `Tarea`:** These models include the `id` field, representing the database ID, which is typically automatically generated and not part of user input. They inherit from their respective base models and are used to represent existing entities.

* **Data Types:**  Pydantic automatically handles type validation. `EmailStr` ensures a valid email format.

This separation allows for better code organization and clear separation of concerns between creating and updating entities.  You can easily adapt this structure for other entities in your application.  Remember to install `pydantic` using `pip install pydantic`.