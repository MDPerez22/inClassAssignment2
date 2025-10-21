from starlette.requests import Request
from fastapi import Depends, HTTPException
from starlette.requests import Request
from tortoise.exceptions import DoesNotExist

from redis_client import RedisAdapter
from session import SessionManager, Session
from models import User
from context import UserCtx, AdminCtx


def get_kv_store(request: Request) -> RedisAdapter:
    return request.app.state.kv_store


def get_session_manager(request: Request) -> SessionManager:
    return request.app.state.session_manager


# dependencies.py (patched)
async def get_session(
    request: Request, session_manager: SessionManager = Depends(get_session_manager)
) -> Session:
    # Check if the request already has a session stored
    if not hasattr(request.state, "session"):
        # Check if a session cookie exists
        sid = request.cookies.get("sid")
        if sid:
            session = await session_manager.get_session(sid)
        else:
            session = await session_manager.create_session()
        request.state.session = session
    return request.state.session


async def get_current_user(request: Request, session: Session = Depends(get_session)):
    await session.load()
    if not session.data or not session.data.get("user_id"):
        raise HTTPException(status_code=303, headers={"location": "/"})

    try:
        user = await user.get(user_id=session.data["user_id"])
        user = UserCtx(user, session)

    except DoesNotExist as e:
        raise HTTPException(status_code=303, headers={"location": "/"}) from e
    return user


def get_admin(request: Request, ctx: UserCtx = Depends(get_current_user)):
    try:
        admin = AdminCtx(ctx.user, ctx.session)
    except PermissionError as e:
        raise HTTPException(status_code=401, detail="Not authenticated") from e
    return admin