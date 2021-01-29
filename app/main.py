import os
from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials

# initiate firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# starts server
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Gui's TODO app written with FastAPI"}
