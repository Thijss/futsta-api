"""Main entrypoint for the application."""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.routers import goals, matches, opponents, players, stats
from app.settings.api import get_api_settings


def get_app() -> FastAPI:
    """Create the FastAPI application."""
    api_settings = get_api_settings()
    server = FastAPI(title=api_settings.project_name)

    server.include_router(goals.router, prefix="/goals")
    server.include_router(stats.router, prefix="/stats")
    server.include_router(matches.router, prefix="/matches")
    server.include_router(opponents.router, prefix="/opponents")
    server.include_router(players.router, prefix="/players")

    server.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.http_allowed_origins,
        allow_credentials=True,
        allow_methods=api_settings.http_allowed_methods,
        allow_headers=api_settings.http_allowed_headers,
    )
    return server


app = get_app()

handler = Mangum(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
