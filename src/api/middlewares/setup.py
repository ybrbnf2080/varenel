from typing import List

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.middlewares.auth import AuthMiddleware
from src.api.middlewares.logger import LoggingMiddleware


def setup_middlewares(
    app: FastAPI, api_key: str, allowed_paths: List[str], production: bool
) -> None:
    app.add_middleware(LoggingMiddleware)

    # app.add_middleware(
    #     AuthMiddleware,
    #     api_key=api_key,
    #     allowed_paths=allowed_paths,
    #     production=production,
    # )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
