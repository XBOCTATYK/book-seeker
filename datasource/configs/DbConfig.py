from typing import TypedDict


class DbConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str
    engine: str
    database: str
    scheme: str
