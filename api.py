from fastapi import FastAPI, HTTPException
import uvicorn

from config import DBSettings
from models import *
from response_models import *

app = FastAPI(
    title="Chertila",
    description="Eto chto opisanie?!",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/users/{user_id}")
async def get_users(user_id: int):
    try:
        with DBSettings.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()

            if user is None:
                raise HTTPException(status_code=228, detail="User was not found")

            return user
    except Exception:
        raise HTTPException(status_code=228, detail="User was not found")

@app.post("/users/add", response_model=UserCreate)
async def add_user(user_name: str, user_role:str):
    user = UserCreate(name=user_name, role=user_role)
    print(f"user_name: {user_name}\nuser_role: {user_role}")

    try:
        with DBSettings.get_session() as conn:
            roleDB = conn.query(Role).filter(Role.name == user.role).first()

            if roleDB is None:
                raise HTTPException(status_code=229, detail="We haven't this role")
            else:
                new_user = User(name = user.name, role_id = roleDB.id)
                conn.add(new_user)
                conn.commit()
                print("Successfully")
                return user
    except Exception:
        raise HTTPException(status_code=230, detail="User wasn't added")

@app.put("/users/update")
async def put_user(user_id: str, user_name: str, user_role: str):
    try:
        with DBSettings.get_session() as conn:
            roleDB = conn.query(Role).filter(Role.name == user_role).first()

            if roleDB is None:
                raise HTTPException(status_code=231, detail="Role wasn't founded")
            else:
                stmt = update(User).where(User.id == user_id).values(name = user_name, role_id = roleDB.id)
                result = conn.execute(stmt)
                conn.commit()

                print(f"Updated {result.rowcount} rows")

    except Exception:
        raise HTTPException(status_code=230, detail="User wasn't updated")


@app.delete("/users/delete")
async def delete_user(user_id: int):
    try:
        with DBSettings.get_session() as conn:
            stmt = delete(User).where(User.id == user_id)
            result = conn.execute(stmt)
            conn.commit()

            print(f"Deleted {result.rowcount} rows")

    except Exception:
        raise HTTPException(status_code=232, detail="User wasn't deleted")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
