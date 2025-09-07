import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(app):
    if not app.debug:
        Path("logs").mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            "logs/microblog.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Microblog startup")
