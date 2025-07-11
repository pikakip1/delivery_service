from uuid import uuid4
from fastapi import Request, Response

SessionCookieName = "delivery_session"


def get_session_id(request: Request, response: Response) -> str:
    session_id: str | None = request.session.get("session_id")

    if not session_id:
        session_id = uuid4().hex
        request.session["session_id"] = session_id

    return session_id
