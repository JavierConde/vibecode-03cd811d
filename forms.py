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

```

Este código define los modelos Pydantic para `Usuario` y `Tarea`.  Se incluyen tres tipos de modelos para cada entidad:

* **`UsuarioBase` / `TareaBase`:**  Estos modelos contienen los campos necesarios para crear un nuevo usuario o tarea,  omitiendo el ID,  ya que este es generado automáticamente por la base de datos.  `orm_mode = True` permite la integración directa con ORMs como SQLAlchemy.

* **`UsuarioCreate` / `TareaCreate`:**  Son prácticamente iguales a `UsuarioBase` / `TareaBase` en este ejemplo, pero podrían ser extendidos en el futuro para añadir validaciones o campos adicionales específicos para la creación.

* **`Usuario` / `Tarea`:**  Estos modelos incluyen el campo `id` para representar un usuario o tarea existente recuperado de la base de datos.

Estos modelos se pueden usar en una aplicación FastAPI para validar datos de entrada de formularios y asegurar la integridad de los datos.  Por ejemplo, `EmailStr` asegura que el correo electrónico sea válido.  Se asume que `id` es un entero autoincremental gestionado por la base de datos.  Puedes añadir más validaciones según sea necesario (longitud de cadenas, valores permitidos, etc.).