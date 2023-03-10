import dataclasses


@dataclasses.dataclass(frozen=True)
class PostgresData:
    user: str
    password: str
    host: str
    port: int
    db: str


@dataclasses.dataclass(frozen=True)
class TelegramData:
    log_chat: int
    debug_chat: int
    bot_token: str


@dataclasses.dataclass(frozen=True)
class ApplicationData:
    api_key: str
    production: bool
    host: str


@dataclasses.dataclass(frozen=True)
class Config:
    postgres: PostgresData
    telegram: TelegramData
    application: ApplicationData
