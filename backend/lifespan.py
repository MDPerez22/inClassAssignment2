import os
import ssl
from contextlib import asynccontextmanager
# import aioredis

from fastapi import FastAPI
from tortoise import Tortoise
from redis_client import RedisAdapter
from session import SessionManager

@asynccontextmanager
async def keiser_lifespan(app: FastAPI):
    try: 
        await Tortoise.init(
            db_url=f"postgres://{os.getenv('USER')}:{os.getenv('PASSWORD')}@localhost:5432/mydb",
            modules={"models": ["models"]}, 
        )   
        await Tortoise.generate_schemas()
    except Exception as e:
        print(f"\033[1;31mERROR: failed to initialize database ({e})\033[0m")
    
    redis_conn = RedisAdapter()
    app.state.kv_store = redis_conn
    app.state.session_manager = SessionManager(redis_conn)

    yield
    
    await redis_conn.flush()
    await redis_conn.close()
    await Tortoise.close_connections()