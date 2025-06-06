import asyncio
from typing import Dict, Optional, Any

class InMemorySessionService:
    def __init__(self):
        self.sessions = {}

    async def create_session(self, app_name: str, user_id: str, session_id: str, state: Optional[Dict] = None) -> Any:
        class Session:
            def __init__(self, app_name, user_id, session_id, state):
                self.app_name = app_name
                self.user_id = user_id
                self.session_id = session_id
                self.state = state or {}
                self.last_update_time = asyncio.get_event_loop().time()
            def as_dict(self): return vars(self)

        self.sessions.setdefault(app_name, {}).setdefault(user_id, {})[session_id] = Session(app_name, user_id, session_id, state)
        return self.sessions[app_name][user_id][session_id]
