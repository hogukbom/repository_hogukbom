from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
db = {}
current_id = 1

class User(BaseModel):
    id: int | None = None
    name: str
    email: str

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in db: raise HTTPException(status_code=404, detail="User not found")
    return db[user_id]

@router.post("/users", response_model=User, status_code=201)
def create_user(user: User):
    global current_id
    user.id = current_id
    db[current_id] = user
    current_id += 1
    return user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    if user_id not in db: raise HTTPException(status_code=404, detail="User not found")
    user.id = user_id
    db[user_id] = user
    return user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in db: raise HTTPException(status_code=404, detail="User not found")
    del db[user_id]
    return None
