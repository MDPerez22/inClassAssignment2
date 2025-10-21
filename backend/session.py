import json
import uuid
from datetime import datetime, timezone

class Session: 
    def __init__ (self, sid: str, data: dict):
        self.id = sid
        self.data = data

    @property
    def user_id(self):
        return self.data.get("user_id")
    
    @property
    def csrf_tokens(self):
        return self.data.setdefault("csrf_tokens", [])
    
    def to_json(self):
        return json.dumps(self.data)
    
class SessionManager:
    def __init__(self, redis, ttl=604800):
        self.redis = redis
        self.ttl = ttl

    async def create_session(self, user_id=None):
        sid = str(uuid.uuid4())
        data = {"user_id": str(user_id) if user_id else None, "created_at": datetime.now(timezone.utc).isoformat(), "csrf_tokens": []}
        await self.redis.set(sid, json.dumps(data), ex=self.ttl)
        return Session(sid, data)

    async def get_session(self, sid):
        raw = await self.redis.get(sid)
        if not raw:
            return None
        data = json.loads(raw)
        return Session(sid, data)

    async def save_session(self, session: Session):
        await self.redis.set(session.id, session.to_json(), ex=self.ttl)

    async def delete_session(self, sid):
        await self.redis.delete(sid)