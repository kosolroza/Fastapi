# 🚀 FastAPI Backend — Learning Notes

A personal learning project to explore **FastAPI** as a backend framework, covering routing, databases, and authentication.

---

## 📌 What is FastAPI?

FastAPI is a modern, fast Python web framework for building APIs. It's built on top of **Starlette** and **Pydantic**, and automatically generates interactive docs.

---

## 🛠️ Installation

```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt]
```

Run the server:

```bash
uvicorn main:app --reload
```

Then open: `http://127.0.0.1:8000/docs` for the auto-generated Swagger UI.

---

## 📁 Project Structure
---

## 🔀 Basics — Routing, Requests & Responses

### Basic Route

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

### Path & Query Parameters

```python
@app.get("/items/{item_id}")
def get_item(item_id: int, search: str = None):
    return {"item_id": item_id, "search": search}
```

### Request Body with Pydantic

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items/")
def create_item(item: Item):
    return item
```

### HTTP Methods

```python
@app.get("/items/")       # Read
@app.post("/items/")      # Create
@app.put("/items/{id}")   # Update
@app.delete("/items/{id}")# Delete
```

---

## 🗄️ Database Integration (SQLAlchemy)

### Setup `database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Define a Model (`models.py`)

```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
```

### DB Dependency Injection

```python
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

---

## 🔐 Authentication & Security (JWT)

### Hash Passwords

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
```

### Create JWT Token

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### Protect a Route

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/me")
def read_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user}
```

---

## 📖 Key Concepts Summary

| Concept | What it does |
|---|---|
| `@app.get/post/put/delete` | Define HTTP routes |
| `BaseModel` (Pydantic) | Validate request/response data |
| `Depends()` | Dependency injection (DB, auth) |
| `SQLAlchemy` | ORM for database operations |
| `JWT` | Stateless authentication tokens |
| `passlib` | Secure password hashing |

---

## 🔗 Useful Links

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [JWT Info](https://jwt.io/)
