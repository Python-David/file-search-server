import logging

from project.config.settings import get_settings


def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger with the specified name.

    :param name: The name of the logger.
    :return: Configured logger.
    """
    settings = get_settings()

    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        # Set the log level
        log_level = getattr(logging, settings.log_level.upper(), logging.DEBUG)
        logger.setLevel(log_level)

        # Create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        # Create a formatter that includes timestamps
        formatter = logging.Formatter(settings.log_format, datefmt=settings.log_datefmt)
        ch.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(ch)

    return logger
