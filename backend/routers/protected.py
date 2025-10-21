# Protected Resources
# Endpoint	Access	Description
# /api/private/profile	Authenticated users	Returns protected content.
# /api/admin/stats

from fastapi import APIRouter, Form, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError

from models import User
from config import app
from context import UserCtx
from dependencies import get_current_user

router = APIRouter(
    prefix="",       # All endpoints start with /users
    tags=[""],        # Shown in Swagger UI
)
@router.get("/private/profile")
async def private_profile(request: Request, ctx: UserCtx = Depends(get_current_user)):
	return {"msg": "TODO1"}

@router.get("/admin/stats")
async def private_profile(request: Request):
	return {"msg": "TODO2"}