from fastapi.security import api_key
from src.lib.config import env
from src.lib.config.entities import (
    ApplicationData,
    Config,
    PostgresData,
    TelegramData,
)


def parse_config() -> Config:
    return Config(
        postgres=PostgresData(
            user=env.str_("POSTGRES_USER"),
            password=env.str_("POSTGRES_PASSWORD"),
            host=env.str_("POSTGRES_HOST"),
            port=env.int_("POSTGRES_PORT"),
            db=env.str_("POSTGRES_DB"),
        ),
        application=ApplicationData(
            api_key=env.str_("API_KEY"),
            production=env.bool_("PRODUCTION"),
            host=env.str_("HOST"),
        ),
        telegram=TelegramData(
            log_chat=env.int_("TELEGRAM_LOG_CHAT"),
            debug_chat=env.int_("TELEGRAM_DEBUG_CHAT"),
            bot_token=env.str_("TELEGRAM_BOT_TOKEN"),
        ),
    )
