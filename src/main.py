from fastapi import Depends, FastAPI
import uvicorn

from src.core.logging import setup_logging
from src.core.config import settings
from starlette.middleware.sessions import SessionMiddleware
from src.utils.session import get_session_id, SessionCookieName
from src.api.v1.endpoints import router as api_v1_router

# from app.logging_config import setup_logging

from src.api.v1.dependencies.redis import init_redis_pool, close_redis_pool

setup_logging()

SECRET_KEY = "SECRET_KEY"


def create_app() -> FastAPI:
    application = FastAPI(
        title='International Delivery Service',
        version='0.1.0',
    )
    application.add_middleware(
        SessionMiddleware,
        secret_key=settings.session_secret_key,
        session_cookie=SessionCookieName,
        max_age=60 * 60 * 24 * 30,
        same_site='lax',
        https_only=False,           
    )
    
    application.add_event_handler("startup", init_redis_pool)
    application.add_event_handler("shutdown", close_redis_pool)

    application.include_router(api_v1_router, prefix="/api/v1")
    
    @application.get('/whoami')
    async def whoami(session_id: str = Depends(get_session_id)) -> dict[str, str]:
        """Returns the caller’s anonymous session id (debug aid)."""
        return {'session_id': session_id}

    # Future routers go here …

    return application
    # Placeholder for future routers:
    # from app.api.v1.router import router as api_router
    # application.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        factory=True,
    )
    