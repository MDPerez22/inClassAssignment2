# Python native
import os
import random

# Dependency library
from fastapi import FastAPI, Form, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

# Application Code

from config import app

from models import User
from routers import (
    storage,
    protected    
)

app.include_router(storage.router)
app.include_router(protected.router)

origins = [
    "http://localhost:5173",  # The URL where your React app is running
    # You can add other origins here, like production domains
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/react-demo")
async def react_endpoint(request: Request, current_user = None):
    # posts = current_user.posts
    posts = []
    return JSONResponse({"hello": "My name is slim shady", "posts": posts})

@app.get("/user")
async def get_users(request: Request):
    users = await user.all()
    
    users_response = []
    for user in users:    
        users_response.append({"username": user.username})
        
    return JSONResponse(users_response)