from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    api_port: int = Field(8000, env="API_PORT")
    sql_conn_uri: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:8087/develop",
        alias="SQLALCHEMY_CONN_URI"
    )
