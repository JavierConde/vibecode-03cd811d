from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

users = {
    "johndoe": {"password": pwd_context.hash("password"), "id": 1}
}

class User(BaseModel):
    id: int
    username: str

class UserInDB(BaseModel):
    password: str
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = None
    for user_dict in users.values():
        if verify_password(token, user_dict["password"]):
            user = User(id=user_dict["id"], username="johndoe")
            break
    if user is None:
        raise credentials_exception
    return user

def get_user(username: str):
    for user_dict in users.values():
        if user_dict["username"] == username:
            return user_dict
    return None


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user("johndoe")  # Simplified for demo
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = "test_token" # Replace with actual JWT generation
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

```

This code provides a basic authentication system.  Remember to replace `"test_token"` with actual JWT generation using a library like `PyJWT`.  Also, this uses an in-memory database; for a production system, you'll need a persistent database.  Error handling could also be improved for a production-ready application.