from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from .routers import users

# initiate firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# starts server
app = FastAPI()

# include the routers
app.include_router(users.router)


# root
@app.get("/")
async def root():
    return {"message": "Welcome to Gui's TODO app written with FastAPI"}
