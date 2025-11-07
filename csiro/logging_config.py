import logging
import logging.config
import sys


def setup_logging(log_level: str = "INFO") -> None:
    # setup console handlers
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "simple",
            "level": log_level,
        }
    }

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(levelname)s - %(message)s",
            },
        },
        "handlers": handlers,
        "root": {
            "level": log_level,
            "handlers": list(handlers.keys()),
        },
        "loggers": {
            "src": {
                "level": log_level,
                "handlers": list(handlers.keys()),
                "propagate": False,
            },
            "PIL": {
                "level": "WARNING",
            },
            "matplotlib": {
                "level": "WARNING",
            },
        },
    }

    # apply config
    logging.config.dictConfig(config)

    # log the setup
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Level: {log_level}")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
