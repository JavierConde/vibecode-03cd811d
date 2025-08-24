from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from datetime import timedelta
from jose import JWTError, jwt
from typing import Optional

# Settings
SECRET_KEY = "secret_key"  # Replace with a strong, randomly generated key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database (in-memory for demonstration)
users_db = {
    "testuser": {"password": "hashed_password", "username": "testuser"}  # Replace with hashed password
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(BaseModel):
    username: str

class UserInDB(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in users_db:
        return users_db[username]
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


# FastAPI app
app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

from datetime import datetime

#  Populate the database with a hashed password (do this only once!)

# Example: Hashing the password "testpassword"
hashed_password = pwd_context.hash("testpassword")
users_db["testuser"]["password"] = hashed_password

```

Remember to replace `"secret_key"` and `"hashed_password"` with appropriately secure values.  This example uses `passlib` for password hashing; install it with `pip install passlib`. Also install `python-jose` with `pip install python-jose`.  This code provides a basic authentication system;  consider adding more robust error handling and security measures for a production environment.