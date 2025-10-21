# /auth/signup	POST	Accepts email/password, creates user, sets session cookie (HTTPOnly, Secure in prod).
# /auth/login	POST	Validates credentials, creates session, sets cookie.
# /auth/logout	POST	Requires valid session, deletes session from Redis, clears cookie.
# /auth/me	GET	Returns current user info (protected).
# /auth/change-password	POST	Requires valid CSRF token + old/new passwords; updates hash and invalidates other sessions.

# storage.py (patched)
from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse

from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError

from models import User as UserModel   # rename import to avoid shadowing
from config import app

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def post_signup(
    request: Request,
    email = Form(...),
    password = Form(...),
):
    try:
        new_user = await UserModel.create(
            email=email,
            hashed_password=bcrypt.hash(password)    # <--- use hashed_password
        )
    except IntegrityError:
        # user already exists (unique constraint)
        return JSONResponse({"error": "user already exists"}, status_code=400)
    except Exception as e:
        # log and return a 500 with a helpful message during dev
        print(f"ERROR creating user: {e}")
        return JSONResponse({"error": "failed to create user"}, status_code=500)

    # respond appropriately
    return JSONResponse({"success": True, "id": str(new_user.id)}, status_code=201)
    # or return RedirectResponse("/dash", status_code=303)

@router.get("/redis-set-test")
async def redis_ping(request: Request):
    redis_conn = app.state.kv_store
    await redis_conn.set("user:var1:2324234", "hello world")
    return {"msg": "Key successfully set"}

@router.get("/redis-get-test")
async def redis_ping(request: Request):
    redis_conn = app.state.kv_store
    list_of_keys = await redis_conn.keys("user:var1:*")
    return {"redis_keys": list_of_keys}

@router.get("/me")
async def get_me_info(request: Request):
    return {"msg": "TODO4"}

@router.get("/logout")
async def get_me_info(request: Request):
    return {"msg": "TODO5"}

@router.get("/change-password")
async def get_me_info(request: Request):
    return {"msg": "TODO6"}

from fastapi.responses import RedirectResponse

@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    return {"success": True}