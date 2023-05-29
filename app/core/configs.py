from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Goods and Trucks"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = '/docs'

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_URL: str
    POSTGRES_PORT: int

    MAXIMUM_CAPASITY = 1000
    MINIMUM_CAPASITY = 1

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        v: str | List[str]
    ) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


tags_metadata = [
    {
        "name": "Truck",
        "description":
            "Manage Trucks.<br>"
            "Some text will be added here soon",

    },
    {
        "name": "Cargo",
        "description":
            "Manage Cargo.<br>"
            "Some text will be added here soon",
    },
]

settings = Settings()
