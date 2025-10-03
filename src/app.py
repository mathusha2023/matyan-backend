import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.database.core.db_session import AsyncPostgresClient
from src.api import main_router
from src.settings import settings


class App(FastAPI):
    def __init__(self):
        super().__init__(title="Matyan", lifespan=App.lifespan, debug=settings.debug)
        super().include_router(main_router)
        super().add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        await AsyncPostgresClient.init_postgres(settings.postgres_url)
        logging.info("All resources have been successfully initialized")

        yield

        await AsyncPostgresClient.close_postgres()
        logging.info("All resources have been successfully closed")
