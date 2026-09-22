# logging_framework.py

import logging
from logging.handlers import (
    RotatingFileHandler,
    TimedRotatingFileHandler
)
from pathlib import Path


class LoggingFramework:
    """
    Enterprise Logging Framework
    """

    def __init__(self):

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)

        # ---------------------------
        # APPLICATION LOGGER
        # ---------------------------
        self.app_logger = logging.getLogger(
            "ApplicationLogger"
        )

        self.app_logger.setLevel(
            logging.INFO
        )

        app_handler = RotatingFileHandler(
            "logs/application.log",
            maxBytes=1024 * 1024,
            backupCount=5
        )

        app_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - "
                "%(levelname)s - "
                "%(message)s"
            )
        )

        self.app_logger.addHandler(
            app_handler
        )

        # ---------------------------
        # ERROR LOGGER
        # ---------------------------
        self.error_logger = logging.getLogger(
            "ErrorLogger"
        )

        self.error_logger.setLevel(
            logging.ERROR
        )

        error_handler = RotatingFileHandler(
            "logs/error.log",
            maxBytes=1024 * 1024,
            backupCount=5
        )

        error_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - "
                "%(levelname)s - "
                "%(message)s"
            )
        )

        self.error_logger.addHandler(
            error_handler
        )

        # ---------------------------
        # API LOGGER
        # ---------------------------
        self.api_logger = logging.getLogger(
            "APILogger"
        )

        self.api_logger.setLevel(
            logging.INFO
        )

        api_handler = TimedRotatingFileHandler(
            "logs/api.log",
            when="midnight",
            interval=1,
            backupCount=7
        )

        api_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - "
                "%(levelname)s - "
                "%(message)s"
            )
        )

        self.api_logger.addHandler(
            api_handler
        )

        # ---------------------------
        # AUDIT LOGGER
        # ---------------------------
        self.audit_logger = logging.getLogger(
            "AuditLogger"
        )

        self.audit_logger.setLevel(
            logging.INFO
        )

        audit_handler = TimedRotatingFileHandler(
            "logs/audit.log",
            when="midnight",
            interval=1,
            backupCount=30
        )

        audit_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - "
                "%(levelname)s - "
                "%(message)s"
            )
        )

        self.audit_logger.addHandler(
            audit_handler
        )

        # ---------------------------
        # CONSOLE LOGGER
        # ---------------------------
        console_handler = logging.StreamHandler()

        console_handler.setLevel(
            logging.INFO
        )

        console_handler.setFormatter(
            logging.Formatter(
                "%(levelname)s - %(message)s"
            )
        )

        self.app_logger.addHandler(
            console_handler
        )

    # --------------------------------
    # APPLICATION LOG
    # --------------------------------
    def log_application(
        self,
        message
    ):
        self.app_logger.info(message)

    # --------------------------------
    # ERROR LOG
    # --------------------------------
    def log_error(
        self,
        message
    ):
        self.error_logger.error(message)

    # --------------------------------
    # API LOG
    # --------------------------------
    def log_api(
        self,
        endpoint,
        method,
        status_code
    ):

        self.api_logger.info(
            f"Endpoint={endpoint}, "
            f"Method={method}, "
            f"Status={status_code}"
        )

    # --------------------------------
    # AUDIT LOG
    # --------------------------------
    def log_audit(
        self,
        username,
        action
    ):

        self.audit_logger.info(
            f"User={username}, "
            f"Action={action}"
        )


# ====================================
# DEMONSTRATION
# ====================================
if __name__ == "__main__":

    logger = LoggingFramework()

    # Logging Levels
    logger.log_application(
        "Application started successfully."
    )

    logger.log_api(
        "/customers",
        "GET",
        200
    )

    logger.log_audit(
        "admin",
        "Exported Sales Report"
    )

    try:
        result = 10 / 0

    except Exception as error:

        logger.log_error(
            f"Exception Occurred: {error}"
        )

    print(
        "\nLogs generated successfully."
    )