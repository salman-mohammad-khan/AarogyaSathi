import time

_TTL_SECONDS = 1800
_sessions = {}


class Session:
    def __init__(self, session_id):
        self.id = session_id
        self.state = {}
        self.updated = time.time()

    def get(self, key, default=None):
        return self.state.get(key, default)

    def set(self, key, value):
        self.state[key] = value
        self.updated = time.time()

    def clear(self):
        self.state = {}
        self.updated = time.time()

    def fresh(self):
        return time.time() - self.updated < _TTL_SECONDS


def get_session(session_id):
    now = time.time()
    for sid in list(_sessions.keys()):
        if now - _sessions[sid].updated > _TTL_SECONDS:
            del _sessions[sid]
    if not session_id:
        session_id = f"anon_{int(now * 1000)}"
    if session_id not in _sessions:
        _sessions[session_id] = Session(session_id)
    session = _sessions[session_id]
    session.updated = now
    return session
