import logging
from logging.handlers import RotatingFileHandler

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": LOG_FORMAT,
        },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "uvicorn.log",
            "mode": "a",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 3,
            "formatter": "default",
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["file"],
    },
}