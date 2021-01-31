from fastapi import FastAPI

from .routers import users

# starts server
app = FastAPI()

# include the routers
app.include_router(users.router)


# root
@app.get("/")
async def root():
    return {"message": "Welcome to Gui's TODO app written with FastAPI"}
