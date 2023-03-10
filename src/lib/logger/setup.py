from logging.config import dictConfig

from src.lib.logger.config import get_logger_config


def setup_logging():
    dictConfig(get_logger_config())
